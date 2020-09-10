import typing
from dataclasses import dataclass


@dataclass
class Word:
    name: str
    description: str
    images: typing.List[str]
    plain_html: str
