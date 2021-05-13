class TrieError(Exception):
    pass


class InvalidWildCardExpressionError(TrieError):

    def __init__(self, expr, message):
        self.expr = expr
        self.message = message

    def __str__(self):
        return repr(': '.join([self.message, self.expr]))
