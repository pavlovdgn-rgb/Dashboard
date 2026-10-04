"""Publish the reviewed source inventory, preserving remote history.

Credential is entered with getpass and kept in process memory only. Git metadata
is kept in a separate temporary checkout; no global Git settings are changed.
"""
import getpass
import hashlib
import io
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'.tmp/github-tools'))
from dulwich import porcelain
from dulwich.ignore import IgnoreFilterManager

REMOTE = 'https://github.com/pavlovdgn-rgb/Dashboard.git'
API = 'https://api.github.com'
PROJECT = '/repos/pavlovdgn-rgb/Dashboard'


def run(token):
    def api(path):
        request = Request(API+path, headers={'Authorization': 'Bearer '+token,
            'Accept': 'application/vnd.github+json', 'User-Agent': 'UX-Lab-source-publisher'})
        with urlopen(request, timeout=45) as response:
            return json.load(response)

    user = api('/user')
    metadata = api(PROJECT)
    if not metadata.get('permissions', {}).get('push'):
        raise RuntimeError('Token does not have push access to the requested repository')
    branch = metadata['default_branch']
    folder = ROOT/'.tmp/github-publish'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    folder.mkdir(parents=True)
    checkout = folder/'repository'
    output = io.BytesIO()
    repo = porcelain.clone(REMOTE, str(checkout), username='x-access-token', password=token,
                           errstream=output, outstream=output)
    ref = ('refs/heads/'+branch).encode()
    repo.refs.set_symbolic_ref(b'HEAD', ref)
    parent = repo.refs.read_ref(ref)
    existing = sorted(str(p.relative_to(checkout)).replace('\\','/') for p in checkout.iterdir() if p.name != '.git')
    print(json.dumps({'repository':metadata['html_url'],'private':metadata['private'],
        'branch':branch,'parent':parent.decode() if parent else None,'root_files':existing,
        'checkout':str(checkout),'authenticated_user':user['login']},ensure_ascii=False),flush=True)
    print('Waiting for PREPARE.', flush=True)
    if input().strip() != 'PREPARE':
        return
    report = json.loads((ROOT/'.tmp/gitlab-export/manifest.json').read_text(encoding='utf-8'))
    if report['potential_secrets']:
        raise RuntimeError('Preflight found potential credentials; inspect locations before publishing')
    paths = []
    for item in report['files']:
        relative = Path(item['path'])
        source = ROOT/relative
        data = source.read_bytes()
        if hashlib.sha256(data).hexdigest() != item['sha256']:
            raise RuntimeError('File changed after preflight: '+item['path'])
        if token.encode() in data:
            raise RuntimeError('Credential found in source inventory')
        destination = checkout/relative
        if destination.is_symlink() or any(p.is_symlink() for p in destination.parents if p != checkout.parent):
            raise RuntimeError('Refusing to overwrite a symlink: '+item['path'])
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        paths.append(item['path'])
    ignore = IgnoreFilterManager.from_repo(repo)
    excluded = [path for path in paths if ignore.is_ignored(path)]
    if excluded:
        raise RuntimeError('Inventory contains Git-ignored files: '+json.dumps(excluded[:20]))
    added, skipped = porcelain.add(repo, paths=[str(checkout/path) for path in paths])
    if skipped:
        raise RuntimeError('Git skipped files: '+str(len(skipped)))
    status = porcelain.status(repo)
    summary = {key:len(value) for key,value in status.staged.items()}
    print(json.dumps({'source_files':len(paths),'staged':summary,'unstaged':len(status.unstaged),
                      'remote_only_files_preserved':True},ensure_ascii=False),flush=True)
    print('Waiting for PUBLISH.',flush=True)
    if input().strip() != 'PUBLISH':
        return
    if any(summary.values()):
        identity = f"{user['login']} <{user['id']}+{user['login']}@users.noreply.github.com>".encode()
        commit = porcelain.commit(repo, message=b'Import UX-Lab dashboard, research tools and design documentation',
                                  author=identity, committer=identity)
        # No force: fail if the branch moved while this import was prepared.
        result = porcelain.push(repo, REMOTE, refspecs=[ref], force=False,
                                username='x-access-token', password=token, outstream=output, errstream=output)
        if result.ref_status and any(value is not None for value in result.ref_status.values()):
            raise RuntimeError('Remote rejected update: '+str(result.ref_status))
    else:
        commit = repo.head()
    remote_head = api(PROJECT+'/git/ref/heads/'+branch)['object']['sha']
    if remote_head != commit.decode():
        raise RuntimeError('Remote head does not match the prepared commit')
    tree = api(PROJECT+'/git/trees/'+commit.decode()+'?recursive=1')
    remote_paths = {row['path'] for row in tree['tree'] if row['type']=='blob'}
    if tree.get('truncated') or not set(paths).issubset(remote_paths):
        raise RuntimeError('Remote tree verification failed')
    outcome = {'repository':metadata['html_url'],'branch':branch,'commit':commit.decode(),
               'commit_url':metadata['html_url']+'/commit/'+commit.decode(),
               'verified_source_files':len(paths),'remote_files':len(remote_paths),'checkout':str(checkout)}
    (ROOT/'.tmp/github-publish/result.json').write_text(json.dumps(outcome,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(outcome,ensure_ascii=False),flush=True)
    repo.close()


if __name__ == '__main__':
    secret = getpass.getpass('GitHub token (hidden): ')
    try:
        run(secret)
    except Exception as error:
        print('ERROR: '+str(error).replace(secret,'[REDACTED]'),flush=True)
        sys.exit(1)
    finally:
        secret = None
