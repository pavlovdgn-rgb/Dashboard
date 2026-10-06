"""Prepare/publish only this task's files, retaining GitHub history and other remote files.

--prepare clones the current main and creates a reviewable local commit.
--publish pushes that exact commit without force, using GH_TOKEN/GITHUB_TOKEN or
an interactive hidden prompt. Credentials are never written to disk.
"""
import argparse
import getpass
import hashlib
import io
import json
import os
from pathlib import Path
import sys
import uuid

from dulwich import porcelain
from dulwich.repo import Repo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'execution'))
from prepare_gitlab_export import SECRET_PATTERNS, SKIP_DIRS

REMOTE = 'https://github.com/pavlovdgn-rgb/Dashboard.git'
REF = b'refs/heads/main'
STATE = ROOT / '.tmp/vercel-publish/prepared.json'
EXTRA = ['README.md', 'directives/directive_wire.md', '.github/workflows/vercel-edition.yml',
         'execution/prepare_vercel_version.py', 'execution/adapt_vercel_version.py',
         'execution/finish_vercel_wiring.py', 'execution/fix_vercel_build.py',
         'execution/publish_vercel_github.py']


def options(token):
    return {'username':'x-access-token', 'password':token} if token else {}


def sources(token):
    paths = list(EXTRA)
    for directory, children, names in os.walk(ROOT / 'vercel-app'):
        children[:] = sorted(name for name in children if name not in SKIP_DIRS)
        for name in sorted(names):
            file = Path(directory) / name
            if file.is_symlink() or name.endswith(('.pyc', '.tsbuildinfo', '.sqlite3', '.sqlite3-wal', '.sqlite3-shm')):
                continue
            if name.startswith('.env') and name != '.env.example':
                continue
            paths.append(file.relative_to(ROOT).as_posix())
    result = {}
    for relative in paths:
        body = (ROOT / relative).read_bytes()
        if token and token.encode() in body:
            raise RuntimeError('Credential found in source: ' + relative)
        if b'\0' not in body:
            text = body.decode('utf-8', errors='replace')
            if any(pattern.search(text) for pattern in SECRET_PATTERNS.values()):
                raise RuntimeError('Potential secret found in source: ' + relative)
        result[relative] = body
    return result


def prepare(token):
    files = sources(token)
    folder = STATE.parent / ('checkout-' + uuid.uuid4().hex[:12])
    folder.parent.mkdir(parents=True, exist_ok=True)
    log = io.BytesIO()
    repo = porcelain.clone(REMOTE, str(folder), errstream=log, outstream=log, **options(token))
    try:
        repo.refs.set_symbolic_ref(b'HEAD', REF)
        parent = repo.head()
        existing_cloud = folder / 'vercel-app'
        if existing_cloud.exists():
            raise RuntimeError('The remote already contains vercel-app; review it before replacing files.')
        # Root prose must match the previously published base before we replace it.
        # This prevents silently overwriting documentation edited on GitHub meanwhile.
        previous = json.loads((ROOT / '.tmp/github-publish/result.json').read_text(encoding='utf-8'))
        base = repo[previous['commit'].encode()]
        for relative in ('README.md', 'directives/directive_wire.md'):
            from dulwich.object_store import tree_lookup_path
            _, old_id = tree_lookup_path(repo.__getitem__, base.tree, relative.encode())
            if (folder / relative).read_bytes() != repo[old_id].data:
                raise RuntimeError('Remote documentation changed; merge it first: ' + relative)
        for relative, body in files.items():
            target = folder / relative
            if target.is_symlink():
                raise RuntimeError('Refusing symlink: ' + relative)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(body)
        porcelain.add(repo, paths=list(files))
        status = porcelain.status(repo)
        if status.unstaged:
            raise RuntimeError('Unstaged source changes remain')
        identity = repo[parent].author
        commit = porcelain.commit(repo, message=b'Add standalone Vercel dashboard with persistent libSQL storage',
                                  author=identity, committer=identity)
        result = {'repository':REMOTE.removesuffix('.git'), 'branch':'main', 'parent':parent.decode(),
                  'commit':commit.decode(), 'checkout':str(folder), 'files':len(files),
                  'bytes':sum(len(body) for body in files.values()),
                  'staged':{key:len(value) for key,value in status.staged.items()},
                  'source_hashes':{key:hashlib.sha256(value).hexdigest() for key,value in files.items()}}
        STATE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps({key:value for key,value in result.items() if key!='source_hashes'}, ensure_ascii=False))
    finally:
        repo.close()


def prepare_update(paths, message, token):
    """Commit an explicit small update on top of the last verified publication."""
    state = json.loads(STATE.read_text(encoding='utf-8'))
    if not state.get('published'):
        raise RuntimeError('Publish or review the pending commit before preparing another update')
    current = porcelain.ls_remote(REMOTE, **options(token)).refs.get(REF, b'').decode()
    if current != state['commit']:
        raise RuntimeError('GitHub main moved; review and merge the new remote changes first')
    files = {}
    for relative in paths:
        path = Path(relative)
        source = (ROOT / path).resolve()
        if path.is_absolute() or not source.is_relative_to(ROOT) or (ROOT / path).is_symlink():
            raise RuntimeError('Source must be a regular workspace file')
        if not (relative.startswith(('src/', 'vercel-app/src/', 'vercel-app/participant/src/', 'vercel-app/api/', 'vercel-app/execution/', 'vercel-app/tests/'))
                or relative in ('execution/publish_vercel_github.py', 'directives/directive_wire.md',
                                'execution/study_task_plan.py', 'execution/check_success_criteria.py',
                                'execution/check_success_criteria.mjs', 'execution/check_multi_task.mjs',
                                'execution/check_criteria_journey.mjs',
                                'execution/check_session_snapshots.mjs',
                                'integrations/Leed-generation/src/ux-lab/RecordingControls.tsx',
                                'integrations/Leed-generation/src/ux-lab/task.ts',
                                'integrations/Leed-generation/src/ux-lab/StudyTask.tsx',
                                'integrations/Leed-generation/src/ux-lab/install.ts')):
            raise RuntimeError('Small updates are restricted to app source and this publisher')
        body = source.read_bytes()
        decoded = body.decode('utf-8')
        if (token and token in decoded) or any(pattern.search(decoded) for pattern in SECRET_PATTERNS.values()):
            raise RuntimeError('Potential credential in source: ' + relative)
        files[relative] = body
    with Repo(state['checkout']) as repo:
        status = porcelain.status(repo)
        if repo.head().decode() != current or status.unstaged or any(status.staged.values()):
            raise RuntimeError('The publication checkout has unreviewed changes')
        for relative, body in files.items():
            target = Path(state['checkout']) / relative
            if target.is_symlink():
                raise RuntimeError('Refusing symlink: ' + relative)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(body)
        porcelain.add(repo, paths=list(files))
        status = porcelain.status(repo)
        if status.unstaged or not any(status.staged.values()):
            raise RuntimeError('Expected a fully staged source update')
        identity = repo[repo.head()].author
        commit = porcelain.commit(repo, message=message.encode(), author=identity, committer=identity)
        state.update(parent=current, commit=commit.decode(), published=False, files=len(files),
                     bytes=sum(map(len, files.values())),
                     source_hashes={key:hashlib.sha256(value).hexdigest() for key,value in files.items()},
                     staged={key:len(value) for key,value in status.staged.items()})
        state.pop('commit_url', None)
        STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps({'commit':state['commit'], 'parent':current, 'staged':state['staged']}))


def publish(token):
    state = json.loads(STATE.read_text(encoding='utf-8'))
    with Repo(state['checkout']) as repo:
        if repo.head().decode() != state['commit']:
            raise RuntimeError('Prepared commit changed')
        current = porcelain.ls_remote(REMOTE, **options(token)).refs
        if current.get(REF, b'').decode() != state['parent']:
            raise RuntimeError('GitHub main moved; merge before publishing, never force push')
        result = porcelain.push(repo, REMOTE, refspecs=[REF], force=False, outstream=io.BytesIO(), errstream=io.BytesIO(), **options(token))
        if result.ref_status and any(value for value in result.ref_status.values()):
            raise RuntimeError('GitHub rejected the update')
        actual = porcelain.ls_remote(REMOTE, **options(token)).refs.get(REF, b'').decode()
        if actual != state['commit']:
            raise RuntimeError('GitHub head verification failed')
        state['published'] = True
        state['commit_url'] = state['repository'] + '/commit/' + actual
        STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps({'published':True, 'commit_url':state['commit_url']}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--prepare', action='store_true')
    action.add_argument('--prepare-update', nargs='+', metavar='PATH')
    action.add_argument('--publish', action='store_true')
    parser.add_argument('--message', default='Polish dashboard controls and layout')
    args = parser.parse_args()
    secret = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN') or ''
    if args.publish and not secret:
        secret = getpass.getpass('GitHub token (hidden): ')
    try:
        if args.prepare_update:
            prepare_update(args.prepare_update, args.message, secret)
        else:
            (prepare if args.prepare else publish)(secret)
    except Exception as error:
        message = str(error)
        if secret:
            message = message.replace(secret, '[REDACTED]')
        print('ERROR: ' + message)
        sys.exit(1)
