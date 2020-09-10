from dataclasses import dataclass
from . import Dic


@dataclass
class SearchResult:
    id: int
    word: str
    short_description: str
    dic: Dic
