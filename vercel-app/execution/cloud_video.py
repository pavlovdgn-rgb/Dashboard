"""Bounded video chunks and HTTP byte ranges for serverless request/response limits."""
import hashlib
import re
import session_video as original

MAX_CHUNK = 256 * 1024
MAX_RESPONSE = 1024 * 1024


def chunk(db, key, seq, body):
    if type(seq) is not int or not 0 <= seq < 10000 or not 0 < len(body) <= MAX_CHUNK:
        raise ValueError('Invalid video chunk')
    record = db.execute('SELECT status,bytes FROM recordings WHERE id=?', (key,)).fetchone()
    if not record:
        raise ValueError('Unknown recording')
    digest = hashlib.sha256(body).hexdigest()
    previous = db.execute('SELECT digest FROM recording_chunks WHERE recording=? AND seq=?', (key, seq)).fetchone()
    if previous:
        if previous[0] != digest:
            raise ValueError('Conflicting chunk')
        return {'accepted': seq}
    if record['status'] != 'uploading' or record['bytes'] + len(body) > original.MAX_VIDEO:
        raise ValueError('Recording finished or too large')
    if seq == 0 and not body.startswith(b'\x1aE\xdf\xa3'):
        raise ValueError('Expected WebM')
    db.execute('INSERT INTO recording_chunks VALUES (?,?,?,?)', (key, seq, body, digest))
    db.execute('UPDATE recordings SET bytes=bytes+?,chunks=chunks+1 WHERE id=?', (len(body), key))
    return {'accepted': seq}


def finish(db, data, identifier):
    if not isinstance(data, dict) or set(data) != {'id', 'chunks', 'duration', 'interrupted'}:
        raise ValueError('Invalid completion')
    key = identifier(data['id'])
    duration = original.finite(data['duration'], .01, 1900)
    count = data['chunks']
    if type(count) is not int or not 1 <= count <= 10000 or not isinstance(data['interrupted'], bool):
        raise ValueError('Invalid completion')
    record = db.execute('SELECT status,chunks,duration,interrupted FROM recordings WHERE id=?', (key,)).fetchone()
    if not record:
        raise ValueError('Unknown recording')
    if record['status'] == 'ready':
        if (record['chunks'], record['duration'], bool(record['interrupted'])) != (count, duration, data['interrupted']):
            raise ValueError('Conflicting completion')
        return {'id': key, 'status': 'ready'}
    sequences = db.execute('SELECT seq FROM recording_chunks WHERE recording=? ORDER BY seq', (key,)).fetchall()
    if [item[0] for item in sequences] != list(range(count)):
        raise ValueError('Missing chunks')
    first = db.execute('SELECT data FROM recording_chunks WHERE recording=? AND seq=0', (key,)).fetchone()[0]
    # Browser MediaRecorder uses an unknown-length Segment. Only its first chunk needs
    # the Duration element; all later chunks remain byte-for-byte unchanged.
    offset = 0
    while offset < len(first):
        tag, n = original.vint(first, offset, True)
        size, k = original.vint(first, offset + n)
        if tag == 0x18538067:
            if count > 1 and size != (1 << (7 * k)) - 1:
                raise ValueError('Expected streaming WebM segment')
            break
        offset += n + k + size
    patched = original.webm_duration(first, duration)
    db.execute('UPDATE recording_chunks SET data=? WHERE recording=? AND seq=0', (patched, key))
    db.execute("UPDATE recordings SET status='ready',duration=?,interrupted=?,bytes=bytes+? WHERE id=?",
               (duration, int(data['interrupted']), len(patched) - len(first), key))
    return {'id': key, 'status': 'ready'}


def media(db, key, range_header, study='leed-local'):
    record = db.execute("SELECT bytes FROM recordings WHERE id=? AND study=? AND status='ready'", (key, study)).fetchone()
    if not record:
        return 404, {}, b''
    size = record[0]
    start, end = 0, size - 1
    if range_header:
        match = re.fullmatch(r'bytes=(\d*)-(\d*)', range_header)
        if not match or not any(match.groups()):
            return 416, {'Content-Range': f'bytes */{size}'}, b''
        first, last = match.groups()
        if first:
            start = int(first)
            end = min(end, int(last)) if last else end
        else:
            start = max(0, size - int(last))
        if start > end or start >= size:
            return 416, {'Content-Range': f'bytes */{size}'}, b''
    elif size > MAX_RESPONSE:
        return 400, {'Content-Type': 'text/plain'}, b'Use HTTP Range requests to retrieve this recording.'
    end = min(end, start + MAX_RESPONSE - 1)
    sizes = db.execute('SELECT seq,length(data) size FROM recording_chunks WHERE recording=? ORDER BY seq', (key,)).fetchall()
    offset, parts = 0, []
    for part in sizes:
        next_offset = offset + part['size']
        if offset <= end and next_offset > start:
            low, high = max(start - offset, 0), min(end - offset + 1, part['size'])
            parts.append(db.execute('SELECT substr(data,?,?) FROM recording_chunks WHERE recording=? AND seq=?',
                                    (low + 1, high - low, key, part['seq'])).fetchone()[0])
        offset = next_offset
        if offset > end:
            break
    headers = {'Content-Type': 'video/webm', 'Accept-Ranges': 'bytes'}
    if range_header:
        headers['Content-Range'] = f'bytes {start}-{end}/{size}'
    return 206 if range_header else 200, headers, b''.join(parts)
