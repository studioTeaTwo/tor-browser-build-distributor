#!/usr/bin/env python3
from pathlib import Path
import re
import sys
import shutil


PAGE_NAME = 'offline-docs'
STATIC_PATH = 'chrome://browser/content/manual/static'

if len(sys.argv) < 3:
    print(f'Usage: {sys.argv[0]} lektor-out-directory target-directory')
    sys.exit(1)

source = Path(sys.argv[1])
target = Path(sys.argv[2])
if not target.exists():
    target.mkdir(exist_ok=True)

static_re = re.compile('"(?:../)*static/([^"]+)"')
link_re = re.compile('href="../([^"]+)"')


def clean_urls(match):
    m = re.match(r'(?:../)?([^/#]+)[/]?[#]?(.*)', match.group(1))
    slug = m.group(1)
    if m.group(2):
        anchor = '_' + m.group(2)
    else:
        anchor = ''
    return f'href="#{slug}{anchor}"'


htmls = source.rglob(f'{PAGE_NAME}/index.html')
for page in htmls:
    with page.open(encoding='utf8') as f:
        contents = f.read()
    contents = static_re.sub(f'"{STATIC_PATH}/\\1"', contents)
    contents = link_re.sub(clean_urls, contents)

    rel = page.relative_to(source)
    dest_name = str(list(rel.parents)[-2].name)
    if dest_name == PAGE_NAME:
        dest_name = 'en'
    dest_name += '.html'
    with (target / dest_name).open('w', encoding='utf8') as f:
        f.write(contents)

shutil.rmtree(target / 'static', ignore_errors=True)
shutil.copytree(source / 'static', target / 'static')
