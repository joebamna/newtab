import os, sys
from types import SimpleNamespace as simple
from time import sleep as zzz
from typing import Any, Literal, SupportsIndex
import json
import tomllib as tom

pjoin = os.path.join

os.chdir(os.path.dirname(os.path.abspath(__file__)))

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

repo = 'https://joebamna.github.io/newtab/'

def toml_get(filen: str) -> dict:
    with open(filen, 'rb') as t:
        return tom.load(t)

def css_str(kv: dict[str, str]) -> str:
    return semi.join([f'{k}: {v}' for k, v in kv.items()])

class App:
    def __init__(self, lid: str, data) -> None:
        self.ID: str = lid
        self.href: str = data['href']
        self.img: str = self.parse_img(lid, data['img'])
        self.props: dict = {
            'content': f'url("{self.img}")',
            'image-rendering': 'auto'
        } | data.get('props', {})
    
    def build(self) -> str:
        return nil.join([
            f'.Links > a[href="{self.href}"] > i > img[src]',
            newl, '{', css_str(self.props), '}', (newl * 2)
        ])

    @classmethod
    def parse_img(cls, lid: str, value: str) -> str:
        if value.startswith('http'):
            return value
        # ^ url

        # file extension
        if value.startswith(dot):
            value = lid + value
        
        # file
        return repo + value

base_header = f'@import url("{repo}style_base.css");'

appdata: dict = toml_get('apps.toml')
styleapps: list[App] = sorted(
    [
        App(k, v)
        for k, v in
        appdata.items()
    ],
    key=lambda a: a.ID
)

with open('style.css', 'r+') as f:
    f.seek(0)
    f.truncate()
    f.write((newl * 2).join([
        base_header,
        nil.join([a.build() for a in styleapps])
    ]).removesuffix(newl))

print('DONE')