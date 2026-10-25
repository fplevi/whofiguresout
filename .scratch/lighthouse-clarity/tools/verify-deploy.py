"""Confere se produção serve os mesmos bytes que o commit (blobs do git) para HTML/CSS/JS e mídia.
Uso: python verify-deploy.py <commit> <baseUrl>"""
import hashlib, subprocess, sys, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor
commit, base = sys.argv[1], sys.argv[2].rstrip('/')
files = subprocess.run(['git', '-c', 'core.quotepath=off', 'ls-tree', '-r', '--name-only', commit, '--', 'index.html', 'case-studies', 'assets'],
                       capture_output=True, text=True, check=True).stdout.split('\n')
files = [f for f in files if f and not f.endswith(('.md', '.txt'))]
def blob(f):
    return subprocess.run(['git', 'cat-file', 'blob', f'{commit}:{f}'], capture_output=True, check=True).stdout
def check(f):
    url = base + '/' + urllib.parse.quote(f)
    try:
        req = urllib.request.Request(url, headers={'Cache-Control': 'no-cache', 'User-Agent': 'verify-deploy'})
        got = urllib.request.urlopen(req, timeout=60).read()
    except Exception as e:
        return f, f'ERRO {e}'
    return f, 'ok' if hashlib.sha1(got).digest() == hashlib.sha1(blob(f)).digest() else 'DIFERENTE'
with ThreadPoolExecutor(8) as ex:
    res = list(ex.map(check, files))
bad = [r for r in res if r[1] != 'ok']
for f, s in bad: print(s, f)
print(f'{len(res) - len(bad)}/{len(res)} arquivos idênticos ao commit {commit}')
