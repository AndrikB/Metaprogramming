def tokenize_file(file_name):
    file = open(file_name)
    return Lexer(file.read()).tokenize_text()


class TokenType:
    whitespace, \
    comment, \
    keyword, \
    separator, \
    operator, \
    identifer, \
    number_literal, \
    string_literal, \
    char_literal, \
    error, \
    *_ = range(20)


class Position:
    def __init__(self, row, column):
        self.row = row
        self.column = column


class Token:
    def __init__(self, token_type, value, position=None):
        self.token_type = token_type
        self.value = value
        self.position = position

    def __repr__(self):
        if self.token_type == TokenType.whitespace:
            return f'{self.token_type}: {ord(self.value)}'
        return f'{self.token_type}, {self.value}'

    def __str__(self):
        return repr(self)


class Lexer:

    def __init__(self, text):
        self.text = text
        self.len = len(text)
        #
        self.curr_line = 1
        self.curr_pos_in_line = 1  # start of token
        self.i = 0
        self.tokens = []

    def new_line(self):
        pass

    def add_token(self, token_type, value):
        self.tokens.append(Token(token_type, value, Position(self.curr_line, self.curr_pos_in_line)))

    def tokenize_text(self):
        while self.i < self.len:
            c = self.text[self.i]

            if c.isspace():
                self.add_space(c)
                continue

            c_next = None
            start_symbols = c

            if self.i + 1 < self.len:
                c_next = self.text[self.i + 1]
                start_symbols = c + c_next

            if start_symbols == "//":
                self.add_single_line_comment()
            elif start_symbols == "/*":
                self.add_multi_line_comment()
            else:
                self.i += 1

        return self.tokens

    def add_space(self, c):
        self.tokens.append(Token(TokenType.whitespace, c))
        self.i += 1
        if c == '\n':
            self.curr_line += 1
            self.curr_pos_in_line = 1
        elif c == ' ':
            self.curr_pos_in_line += 1
        elif c == '\t':
            self.curr_pos_in_line += 4 - (self.curr_pos_in_line % 4)

    def add_single_line_comment(self):
        i = self.text.find('\n', self.i + 2)
        if i == -1:
            i = self.len

        comment = self.text[self.i: i]
        self.add_token(TokenType.comment, comment)

        # we dont need to change current pos in line
        self.i = i  # because /n will be added in next iter

    def add_multi_line_comment(self):
        i = self.text.find('*/', self.i + 2)
        if i != -1:
            i += 2
        else:  # not ended comment
            comment = self.text[self.i: self.len]
            self.add_token(TokenType.comment, comment)
            self.i = self.len
            return

        comment = self.text[self.i: i]
        self.add_token(TokenType.comment, comment)

        start_of_line = self.text.rfind('\n', self.i, i)
        if start_of_line != -1:
            self.curr_line += self.text.count('\n', self.i, i)  # at less one
            self.curr_pos_in_line = i - start_of_line

        self.i = i
