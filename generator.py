import os
import sys
from types import SimpleNamespace as simple
from time import sleep as zzz
from typing import Any, Literal, SupportsIndex
import json

nil = ''
sp = ' '
bsl = '\\'
fsl = '/'
star = '*'
dot = '.'
back = (dot * 2) + (bsl * 2)
newl = '\n'
cret = '\r'
slot = '{}'
colon = ':'
semi = ';'
question = '?'
hshtg = '#'
dash = '-'
yes = '✓'
no = '✕'
na = 'N/A'
indent = (sp * 4)

cssIDs = simple(
    CONTENT='$content',
    APP='$appid'
)

def clear(Maybe: bool = True):
    if Maybe:
        os.system('cls')

def rel(Maybe: bool = True):
    if Maybe:
        clear()
        os.execv(sys.executable, [sys.executable] + sys.argv)

def css_list_squash(css: list[str]) -> str:
    return newl.join([part.replace(newl, nil) for part in css])

def list_replace(parts: list[str], old: str, new: str, count: SupportsIndex = -1, /) -> list[str]:
    return [part.replace(old, new, count) for part in parts]

class App:
    def __init__(self, f: str | Any) -> None:
        self.ID = f.removesuffix('.txt')
        self.props = []

        with open(os.path.join('APPS', f), 'r') as f:
            self.props = f.read().splitlines()

        #file is empty
        if self.props == []:
            self.props = [cssIDs.CONTENT]

        #the 'content: var(--AppID)' placeholder
        self.props = list_replace(self.props, cssIDs.CONTENT, f'content: {cssIDs.APP}')

        #the AppID placeholder
        self.props = list_replace(self.props, cssIDs.APP, f'var(--{self.ID})')
    
    def __str__(self) -> str:
        prop_count = len(self.props)

        r = f""".Links > a[href="{app_href[self.ID]}"] > i > img[src]
{{{nil.join(self.props)}}}"""
        
        if prop_count == 0:
            r = r.replace(newl, nil)
        
        return r

base_header = '@import url("https://joebamna.github.io/newtab/style_base.css");'

style = simple(
    base = nil,
    apps = []
)
with open('style_base.css', 'r') as f:
    style.base = f.read()

with open('app_href.json', 'r') as f:
    app_href = json.load(f)

for appfile in os.listdir('APPS'):
    style.apps.append(App(appfile))

style.apps = sorted(style.apps, key=lambda a: a.ID)

with open('style.css', 'r+') as f:
    f.seek(0)
    f.truncate()
    f.write((newl * 2).join([base_header, css_list_squash([f"{a}" for a in style.apps])]))