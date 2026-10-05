"""Local consented WebM recording storage. Chunks are idempotent; only complete uploads play."""
import hashlib
import json
import math
import re
import struct
import live_project

MAX_CHUNK=8*1024*1024
MAX_VIDEO=256*1024*1024

def initialize(db):
    db.executescript('''
      CREATE TABLE IF NOT EXISTS recordings (id TEXT PRIMARY KEY, study TEXT NOT NULL, session TEXT NOT NULL,
        startedAt INTEGER NOT NULL, mime TEXT NOT NULL, duration REAL NOT NULL DEFAULT 0,
        status TEXT NOT NULL DEFAULT 'uploading', chunks INTEGER NOT NULL DEFAULT 0, bytes INTEGER NOT NULL DEFAULT 0,
        interrupted INTEGER NOT NULL DEFAULT 0, media BLOB);
      CREATE TABLE IF NOT EXISTS recording_chunks (recording TEXT NOT NULL, seq INTEGER NOT NULL, data BLOB NOT NULL,
        digest TEXT NOT NULL, PRIMARY KEY(recording,seq));
      CREATE INDEX IF NOT EXISTS recordings_session ON recordings(study,session,startedAt);
    ''')

def metadata(db,session,study='leed-local'):
    return [dict(row) for row in db.execute("SELECT id,session,startedAt,mime,duration,status,chunks,bytes,interrupted FROM recordings WHERE study=? AND session=? ORDER BY startedAt",(study,session))]

def finite(value,low,high):
    if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or not low<=value<=high:raise ValueError('Invalid number')
    return value

def start(db,data,identifier):
    if not isinstance(data,dict) or set(data)!={'id','study','session','startedAt','mime'}:raise ValueError('Invalid recording')
    for key in ('id','study','session'):identifier(data[key])
    config=live_project.settings(db,data['study'])
    if data['mime'] not in ('video/webm','video/webm;codecs=vp8','video/webm;codecs=vp9'):raise ValueError('Invalid recording format')
    finite(data['startedAt'],0,1e14)
    existing=db.execute('SELECT * FROM recordings WHERE id=?',(data['id'],)).fetchone()
    if existing and any(existing[key]!=value for key,value in data.items()):raise ValueError('Conflicting recording')
    if existing:return {'id':data['id']}
    if not config['enabled'] or not config['allowVideo'] or config['recordingMode']!='video':raise ValueError('Recording disabled')
    db.execute('INSERT OR IGNORE INTO recordings(id,study,session,startedAt,mime) VALUES (?,?,?,?,?)',tuple(data[key] for key in ('id','study','session','startedAt','mime')))
    return {'id':data['id']}

def chunk(db,key,seq,body):
    if not 0<=seq<10000 or not 0<len(body)<=MAX_CHUNK:raise ValueError('Invalid chunk')
    record=db.execute('SELECT status,bytes FROM recordings WHERE id=?',(key,)).fetchone()
    if not record:raise ValueError('Unknown recording')
    digest=hashlib.sha256(body).hexdigest()
    previous=db.execute('SELECT digest FROM recording_chunks WHERE recording=? AND seq=?',(key,seq)).fetchone()
    if previous:
        if previous[0]!=digest:raise ValueError('Conflicting chunk')
        return {'accepted':seq}
    if record['status']!='uploading' or record['bytes']+len(body)>MAX_VIDEO:raise ValueError('Recording limit or already finished')
    if seq==0 and not body.startswith(b'\x1aE\xdf\xa3'):raise ValueError('Expected WebM')
    db.execute('INSERT INTO recording_chunks VALUES (?,?,?,?)',(key,seq,body,digest))
    db.execute('UPDATE recordings SET bytes=bytes+?,chunks=chunks+1 WHERE id=?',(len(body),key))
    return {'accepted':seq}

def vint(data,offset,keep_marker=False):
    if offset>=len(data) or data[offset]==0:raise ValueError('Invalid EBML')
    size=1
    while not data[offset]&(1<<(8-size)):size+=1
    if size>8 or offset+size>len(data):raise ValueError('Truncated EBML')
    value=int.from_bytes(data[offset:offset+size],'big')
    return (value if keep_marker else value&((1<<(7*size))-1)),size

def size_bytes(value):
    size=next(i for i in range(1,9) if value<(1<<(7*i))-1)
    return (value|(1<<(7*size))).to_bytes(size,'big')

def webm_duration(data,duration):
    """MediaRecorder WebM lacks Duration. Add it to Segment/Info for finite seekable playback.
    Chromium's streaming output has no SeekHead/Cues offsets to invalidate; reject those variants.
    Duration is expressed in TimestampScale units (Matroska Info specification).
    """
    offset=0
    while offset<len(data):
        tag,n=vint(data,offset,True);size,k=vint(data,offset+n);begin=offset+n+k
        if tag==0x18538067:break
        offset=begin+size
    else:raise ValueError('Missing WebM segment')
    segment=offset;segment_begin=begin;segment_size=size;segment_k=k;segment_n=n
    offset=begin
    while offset<len(data):
        tag,n=vint(data,offset,True);size,k=vint(data,offset+n);begin=offset+n+k;end=begin+size
        if tag in (0x114D9B74,0x1C53BB6B):raise ValueError('Unexpected indexed WebM')
        if tag==0x1549A966:
            pos=begin;scale=1000000;parts=[]
            while pos<end:
                child,cn=vint(data,pos,True);length,ck=vint(data,pos+cn);body=pos+cn+ck;next_pos=body+length
                if next_pos>end:raise ValueError('Invalid WebM info')
                if child==0x2AD7B1:scale=int.from_bytes(data[body:next_pos],'big')
                if child!=0x4489:parts.append(data[pos:next_pos])
                pos=next_pos
            if not scale:raise ValueError('Invalid timestamp scale')
            info=b''.join(parts)+b'\x44\x89\x88'+struct.pack('>d',duration*1e9/scale)
            replacement=data[offset:offset+n]+size_bytes(len(info))+info
            tail=data[segment_begin:offset]+replacement+data[end:]
            # Streaming segments use the all-ones unknown size. Finite ones must be corrected.
            prefix=data[:segment+segment_n]
            header=data[segment+segment_n:segment_begin] if segment_size==(1<<(7*segment_k))-1 else size_bytes(len(tail))
            return prefix+header+tail
        if tag==0x1F43B675:break
        offset=end
    raise ValueError('Missing WebM info')

def finish(db,data,identifier):
    if not isinstance(data,dict) or set(data)!={'id','chunks','duration','interrupted'}:raise ValueError('Invalid completion')
    key=identifier(data['id']);duration=finite(data['duration'],.01,1900)
    count=data['chunks']
    if type(count) is not int or not 1<=count<=10000 or not isinstance(data['interrupted'],bool):raise ValueError('Invalid completion')
    record=db.execute('SELECT * FROM recordings WHERE id=?',(key,)).fetchone()
    if not record:raise ValueError('Unknown recording')
    if record['status']=='ready':
        if record['chunks']!=count or record['duration']!=duration:raise ValueError('Conflicting completion')
        return {'id':key,'status':'ready'}
    pieces=db.execute('SELECT seq,data FROM recording_chunks WHERE recording=? ORDER BY seq',(key,)).fetchall()
    if [p['seq'] for p in pieces]!=list(range(count)):raise ValueError('Missing chunks')
    media=webm_duration(b''.join(p['data'] for p in pieces),duration)
    db.execute("UPDATE recordings SET status='ready',duration=?,interrupted=?,media=? WHERE id=?",(duration,int(data['interrupted']),media,key))
    # Keep hashes to acknowledge retries without duplicating the video storage.
    db.execute("UPDATE recording_chunks SET data=x'' WHERE recording=?",(key,))
    return {'id':key,'status':'ready'}

def media(db,key,range_header,study='leed-local'):
    row=db.execute("SELECT length(media) size FROM recordings WHERE id=? AND study=? AND status='ready'",(key,study)).fetchone()
    if not row:return 404,{},b''
    size=row['size'];start=0;end=size-1;status=200
    if range_header:
        match=re.fullmatch(r'bytes=(\d*)-(\d*)',range_header)
        if not match or not any(match.groups()):return 416,{'Content-Range':f'bytes */{size}'},b''
        first,last=match.groups()
        if first:start=int(first);end=min(int(last),end) if last else end
        else:start=max(0,size-int(last))
        if start>end:return 416,{'Content-Range':f'bytes */{size}'},b''
        status=206
    data=db.execute('SELECT substr(media,?,?) FROM recordings WHERE id=?',(start+1,end-start+1,key)).fetchone()[0]
    headers={'Content-Type':'video/webm','Accept-Ranges':'bytes'}
    if status==206:headers['Content-Range']=f'bytes {start}-{end}/{size}'
    return status,headers,data
