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
    IMG='$img',
    APP='$id'
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

def dict_replace(kv: dict[str, str], old: str, new: str, count: SupportsIndex = -1, /) -> dict[str, str]:
    return {k: v.replace(old, new, count) for k, v in kv.items()}

def css_str(kv: dict[str, str]) -> str:
    r = []

    for k, v in kv.items():
        r.append(f'{k}: {v}')

    return semi.join(r)


class App:
    def __init__(self, ID: str, data) -> None:
        self.ID = ID
        self.href = data['href']
        self.props = data.get('props', {'content': cssIDs.IMG})

        self.props = dict_replace(self.props, cssIDs.IMG, f"var(--{cssIDs.APP})")
        self.props = dict_replace(self.props, cssIDs.APP, self.ID)

        # self.ID = f.removesuffix('.txt')
        # self.props = []

        # with open(os.path.join('APPS', f), 'r') as f:
        #     self.props = f.read().splitlines()

        # #file is empty
        # if self.props == []:
        #     self.props = [cssIDs.APPIMG]

        # #the 'content: var(--AppID)' placeholder
        # self.props = list_replace(self.props, cssIDs.APPIMG, f'content: {cssIDs.APP}')

        # #the AppID placeholder
        # self.props = list_replace(self.props, cssIDs.APP, f'var(--{self.ID})')
    
    def __str__(self) -> str:
        r = f'.Links > a[href="{self.href}"] > i > img[src]'
        p = css_str(self.props)

        # if False:
        #     p = p.replace(semi, semi + newl + indent)

        # r += f'{newl}{{{p}{newl}}}{newl}'

        r += f'{{{p}}}'
        return r + newl

base_header = '@import url("https://joebamna.github.io/newtab/style_base.css");'

style = simple(
    base = nil,
    apps = []
)
with open('style_base.css', 'r') as f:
    style.base = f.read()

with open('apps.json', 'r') as f:
    appdata = json.load(f)

for k, v in appdata.items():
    style.apps.append(App(k, v))

style.apps = sorted(style.apps, key=lambda a: a.ID)

with open('style.css', 'r+') as f:
    f.seek(0)
    f.truncate()
    f.write((newl * 2).join([base_header, nil.join([str(a) for a in style.apps])]))

print(newl+'DONE')