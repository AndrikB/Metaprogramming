from os import remove
from os.path import basename, dirname, join

from .lexer import tokenize_file


class File:

    def __init__(self, filename):
        self.filename = filename
        self.tokens = tokenize_file(filename)
        self.new_filename = basename(filename)

    def __repr__(self):
        return self.filename

    def __str__(self):
        return str(self.filename)

    def print_file(self):
        remove(self.filename)
        print(dirname(self.filename))
        print(self.new_filename)
        file = open(join(dirname(self.filename), self.new_filename), mode="w", encoding='utf-8')
        for token in self.tokens:
            file.write(token.second_value)
