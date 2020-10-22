from lexer import tokenize_file


class File:

    def __init__(self, filename):
        self.filename = filename
        self.tokens = tokenize_file(filename)

    def __repr__(self):
        return self.filename

    def __str__(self):
        return repr(self)
