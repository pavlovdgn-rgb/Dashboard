"""Inventory source files before GitLab import, without copying private local state.

This is a preflight inventory, not a replacement for Git's ignore engine.
Before staging, compare it with `git ls-files --others --exclude-standard`.
Only potential secret locations are reported, never their contents.
"""
import fnmatch
import hashlib
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {'.git', '.tmp', '.local', 'node_modules', 'dist', 'dist-ssr',
             'storybook-static', '__pycache__', 'playwright-report', 'test-results',
             '.vercel', '.idea', '.vscode'}
SKIP_FILES = ['.env', '.env.*', 'credentials.json', 'token.json', '*.sqlite',
              '*.sqlite3', '*.sqlite3-*', '*.sqlite-*', '*.pem', '*.key',
              '*.pyc', '*.pyo', '*.log', '*.tsbuildinfo', '.DS_Store', '*.local']
SECRET_PATTERNS = {
    'private-key': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'gitlab-token': re.compile(r'glpat-[A-Za-z0-9_-]{20,}'),
    'github-token': re.compile(r'(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})'),
    'openai-token': re.compile(r'\bsk-(?:proj-)?[A-Za-z0-9_-]{40,}'),
    'aws-access-key': re.compile(r'\bAKIA[A-Z0-9]{16}\b'),
}


def main():
    files, findings = [], []
    for directory, children, names in os.walk(ROOT, followlinks=False):
        children[:] = sorted(name for name in children if name not in SKIP_DIRS
                             and not (Path(directory)/name).is_symlink())
        for name in sorted(names):
            if name not in ('.env.example', '.env.sample') and any(fnmatch.fnmatch(name, p) for p in SKIP_FILES):
                continue
            path = Path(directory)/name
            if path.is_symlink():
                continue
            relative = path.relative_to(ROOT).as_posix()
            data = path.read_bytes()
            files.append({'path': relative, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
            if b'\0' not in data and len(data) < 10_000_000:
                content = data.decode('utf-8', errors='replace')
                for kind, pattern in SECRET_PATTERNS.items():
                    for match in pattern.finditer(content):
                        findings.append({'path': relative, 'line': content.count('\n', 0, match.start())+1, 'kind': kind})
    report = {'files': files, 'total_files': len(files), 'total_bytes': sum(f['bytes'] for f in files),
              'large_files': [f for f in files if f['bytes'] > 10_000_000], 'potential_secrets': findings}
    output = ROOT/'.tmp/gitlab-export/manifest.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k != 'files'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
