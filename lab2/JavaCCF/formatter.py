import re
from pathlib import Path

from lexer import TokenType


def get_files_rec(path):
    return list(Path(path).rglob("*.[jJ][aA][vV][aA]"))


def get_files(path):
    return list(Path(path).glob("*.[jJ][aA][vV][aA]"))


def format_files(files):
    formatter = Formatter(files)
    formatter.format_files()


class_interface_enum = ('class', 'interface', 'enum')


class Formatter:

    def __init__(self, files):
        self.files = files

    @staticmethod
    def get_next_no_whitespace_token_id(file, _id):
        while _id < len(file.tokens):
            _id += 1
            if file.tokens[_id].token_type != TokenType.whitespace:
                return _id
        return -1

    @staticmethod
    def get_previous_token_id_with_such_value(tokens, i, values):
        while i > 0:
            i -= 1
            if tokens[i].value in values:
                return i
        return -1

    def replace_all_tokens_like_this(self, token):
        print(token)
        for file in self.files:
            for file_token in file.tokens:
                if file_token.value == token.value:
                    file_token.second_value = token.second_value

    @staticmethod
    def to_upper(string, i):
        if len(string) == i:
            return string
        return string[:i] + string[i].upper() + string[i + 1:]

    @staticmethod
    def to_lower(string, i):
        if len(string) == i:
            return string
        return string[:i] + string[i].lower() + string[i + 1:]

    # replace
    @staticmethod
    def replace_underscore_to_uppercase(token):
        i = 0
        while i < len(token.second_value):
            if token.second_value[i] == '_':
                token.second_value = token.second_value.replace('_', '', 1)
                token.second_value = Formatter.to_upper(token.second_value, i)
            i += 1

    def replace_to_camel_case_first_up(self, token):
        def is_camel_case_first_up():
            return re.search('^[A-Z][a-zA-Z0-9]*$', token.second_value)

        if is_camel_case_first_up():
            return

        Formatter.replace_underscore_to_uppercase(token)
        token.second_value = Formatter.to_upper(token.second_value, 0)

        if not is_camel_case_first_up():
            print(f'wtf in token camel_case_first_up: {token}')

        self.replace_all_tokens_like_this(token)

    def replace_to_camel_case_first_down(self, token):

        def is_camel_case_first_down():
            return re.search('^[a-z][a-zA-Z0-9]*$', token.second_value)

        if is_camel_case_first_down():
            return

        Formatter.replace_underscore_to_uppercase(token)
        token.second_value = Formatter.to_lower(token.second_value, 0)

        if not is_camel_case_first_down():
            print('wtf in token case_first_down: ' + token)

        self.replace_all_tokens_like_this(token)

    def replace_to_upper_case(self, token):
        pass

    # fix
    def fix_names(self, file):
        stack = []
        for i in range(len(file.tokens)):
            token = file.tokens[i]

            if token.value in class_interface_enum:
                stack.append(token.value)
                class_id = self.get_next_no_whitespace_token_id(file, i)
                self.replace_to_camel_case_first_up(file.tokens[class_id])

            elif token.value == '{':
                stack.append(token.value)
            elif token.value == '}':
                stack.pop()
                if len(stack) > 0 and stack[-1] in class_interface_enum:
                    stack.pop()

            if token.token_type == TokenType.identifier and \
                    len(stack) > 1 and stack[-2] in class_interface_enum and stack[-1] == '{':  # in class
                next_token = file.tokens[self.get_next_no_whitespace_token_id(file, i)]

                if next_token.value == '(':  # is method declaration
                    self.replace_to_camel_case_first_down(token)
                elif next_token.value in (';', '='):  # is variable
                    end_of_search = Formatter.get_previous_token_id_with_such_value(file.tokens, i, ('{', '}', ';'))
                    if Formatter.get_previous_token_id_with_such_value(file.tokens, i, ('final',)) > end_of_search:
                        # final variable
                        self.replace_to_upper_case(token)
                    else:
                        self.replace_to_camel_case_first_down(token)

    def format_files(self):
        for file in self.files:
            self.fix_names(file)
