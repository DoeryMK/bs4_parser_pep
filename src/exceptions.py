class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""
    pass


class ParserFindDocURLsException(Exception):
    """Вызывается, когда парсер не может найти в тегах нужный блок
    с урлами на документацию."""
    pass
