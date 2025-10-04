import os
import sys
from types import SimpleNamespace as simple
from time import sleep as zzz
from typing import Any, Literal
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

def clear(Maybe: bool = True):
    if Maybe:
        os.system('cls')

def rel(Maybe: bool = True):
    if Maybe:
        clear()
        os.execv(sys.executable, [sys.executable] + sys.argv)

def css_list_squash(css: list[str]) -> str:
    return nil.join([part.replace(newl, nil) for part in css])

class App:
    def __init__(self, f: str | Any) -> None:
        self.ID = f.removesuffix('.txt')
        self.props = []

        with open(os.path.join('APPS', f), 'r') as f:
            self.props = f.read().splitlines()

        if self.props == []:
            self.props = [f'content: APPID;']

        self.props = [prop.replace('APPID', f'var(--{self.ID})') for prop in self.props]
    
    def __str__(self) -> str:
        prop_count = len(self.props)

        r = f""".Links a:nth-child({app_order[self.ID]}) i img[src]
{{
{indent if prop_count > 1 else nil}{newl + indent.join(self.props)}
}}"""
        
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

with open('app_order.json', 'r') as f:
    app_order = json.load(f)

for appfile in os.listdir('APPS'):
    style.apps.append(f"{App(appfile)}")

with open('style.css', 'r+') as f:
    f.seek(0)
    f.truncate()
    f.write((newl * 2).join([base_header, css_list_squash(style.apps)]))