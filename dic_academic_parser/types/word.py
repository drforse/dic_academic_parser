import typing
from dataclasses import dataclass

from . import Dic


@dataclass
class Word:
    name: str
    description: str
    images: typing.List[str]
    plain_html: str
    url: str
    dic: Dic
