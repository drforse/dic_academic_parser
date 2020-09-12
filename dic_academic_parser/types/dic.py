import logging


class Dic:
    def __init__(self, id: str, dic_type: str, title: str = '', **kwargs):
        if kwargs.get('name'):
            self.id: str = kwargs.get('name')
            logging.warning('Dic init: name parameter is deprecated, use id instead')
        self.id: str = id
        self.dic_type: str = dic_type
        self.title: str = title

    @property
    def name(self):
        logging.warning('Dic.name is deprecated, use Dic.id instead')
        return self.id

    def get_title(self):
        if not self.title:
            from ..parser import Parser
            title = Parser.get_dic_title(self)
            self.title = title
        return self.title
