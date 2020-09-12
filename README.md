# dic_academic_parser
dic.academic.ru parser using BeautifulSoup4

###example:
```
from parser import Parser


results = Parser.search_all('слово')
for result in results:
    p = Parser(result.dic)
    word = p.get_word(result.id)
    print(word.dic.title)
    print(word.name)
    print(word.description)
    print(word.url)
```


