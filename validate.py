#!/usr/bin/env python3
"""Static checks for the site. Usage: python3 tools/validate.py   (exit code 1 on any error)

Checks: broken local links/assets/anchors, duplicate ids, missing <title>/description/h1/lang,
sitemap.xml coverage, and files listed in the service worker precache.
"""
import json, os, re, sys
from html.parser import HTMLParser
from urllib.parse import unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', '.github', 'tools', 'docs', 'node_modules'}
errors, warnings = [], []


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.ids, self.tags = [], [], set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.add(tag)
        for k in ('href', 'src'):
            if a.get(k):
                self.refs.append(a[k])
        if a.get('id'):
            self.ids.append(a['id'])


def pages():
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in files:
            if f.endswith('.html'):
                yield os.path.join(d, f)


parsed = {}
for path in pages():
    rel = os.path.relpath(path, ROOT).replace(os.sep, '/')
    text = open(path, encoding='utf8').read()
    p = Page()
    p.feed(text)
    parsed[rel] = p
    for needle, label in (('<title>', 'title'), ('name="description"', 'meta description'), ('lang="ar"', 'html lang')):
        if needle not in text:
            errors.append(f'{rel}: missing {label}')
    if rel != '404.html' and '<h1' not in text:
        errors.append(f'{rel}: missing <h1>')
    dup = {i for i in p.ids if p.ids.count(i) > 1}
    if dup:
        errors.append(f'{rel}: duplicate ids {sorted(dup)}')

for rel, p in parsed.items():
    if rel == '404.html':
        continue  # uses absolute GitHub Pages paths by design
    base = os.path.dirname(rel)
    for ref in p.refs:
        if re.match(r'^(https?:|mailto:|tel:|data:|javascript:)', ref):
            continue
        target, _, frag = ref.partition('#')
        target = unquote(target.split('?')[0])
        if not target:
            if frag and frag not in p.ids:
                errors.append(f'{rel}: missing anchor #{frag}')
            continue
        full = os.path.normpath(os.path.join(ROOT, base, target))
        if not os.path.exists(full):
            errors.append(f'{rel}: broken reference {ref}')
        elif frag and full.endswith('.html'):
            other = parsed.get(os.path.relpath(full, ROOT).replace(os.sep, '/'))
            if other and frag not in other.ids:
                errors.append(f'{rel}: missing anchor {ref}')

# sitemap coverage
sm = open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf8').read()
for rel in parsed:
    if rel in ('404.html', 'offline.html', 'sitemap.html'):
        continue
    if rel != 'index.html' and '/' + rel + '<' not in sm:
        errors.append(f'sitemap.xml: missing {rel}')

# service worker precache
sw = open(os.path.join(ROOT, 'sw.js'), encoding='utf8').read()
m = re.search(r'const PRECACHE = (\[.*?\]);', sw, re.S)
for item in json.loads(m.group(1)):
    if item != './' and not os.path.exists(os.path.join(ROOT, item)):
        errors.append(f'sw.js: precache entry not found {item}')

# manifest
man = json.load(open(os.path.join(ROOT, 'manifest.webmanifest'), encoding='utf8'))
for icon in man['icons']:
    if not os.path.exists(os.path.join(ROOT, icon['src'])):
        errors.append(f'manifest: missing icon {icon["src"]}')

print(f'{len(parsed)} pages checked')
for w in warnings:
    print('WARN ', w)
for e in errors:
    print('ERROR', e)
print('OK' if not errors else f'{len(errors)} error(s)')
sys.exit(1 if errors else 0)
