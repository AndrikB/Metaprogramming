import re
from pathlib import Path

from lexer import TokenType, Token, Position


def get_files_rec(path):
    return list(Path(path).rglob("*.[jJ][aA][vV][aA]"))


def get_files(path):
    return list(Path(path).glob("*.[jJ][aA][vV][aA]"))


def print_files(files):
    for file in files:
        file.print_file()


def format_files(files):
    formatter = Formatter(files)
    formatter.format_files()
    print_files(files)


class_interface_enum = ('class', 'interface', 'enum', '@interface')


class Formatter:

    def __init__(self, files):
        self.files = files

    @staticmethod
    def get_next_no_whitespace_token_id(file, _id):
        while _id + 1 < len(file.tokens):
            _id += 1
            if file.tokens[_id].token_type != TokenType.whitespace:
                return _id
        return -1

    @staticmethod
    def get_prev_no_whitespace_token_id(file, _id):
        while _id < len(file.tokens):
            _id -= 1
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

    @staticmethod
    def insert_into_string(string, i, value):
        if len(string) == i:
            return string + value
        return string[:i] + value + string[i:]

    # replace
    @staticmethod
    def replace_underscore_to_uppercase(token):
        i = 0
        while i < len(token.second_value):
            if token.second_value[i] == '_':
                token.second_value = token.second_value.replace('_', '', 1)
                token.second_value = Formatter.to_upper(token.second_value, i)
            i += 1

    @staticmethod
    def is_camel_case_first_up(token):
        return re.search('^[A-Z][a-zA-Z0-9]*$', token.second_value)

    def replace_to_camel_case_first_up(self, token):
        if Formatter.is_camel_case_first_up(token):
            return

        Formatter.replace_underscore_to_uppercase(token)
        token.second_value = Formatter.to_upper(token.second_value, 0)

        if not Formatter.is_camel_case_first_up(token):
            print(f'wtf in token camel_case_first_up: {token}')

        self.replace_all_tokens_like_this(token)

    @staticmethod
    def is_camel_case_first_down(token):
        return re.search('^[a-z][a-zA-Z0-9]*$', token.second_value)

    def replace_to_camel_case_first_down(self, token):
        if Formatter.is_camel_case_first_down(token):
            return

        Formatter.replace_underscore_to_uppercase(token)
        token.second_value = Formatter.to_lower(token.second_value, 0)

        if not Formatter.is_camel_case_first_down(token):
            print('wtf in token case_first_down: ' + token)

        self.replace_all_tokens_like_this(token)

    @staticmethod
    def is_upper_case(token):
        return re.search('^([A-Z0-9]*_*)*$', token.second_value)

    def replace_to_upper_case(self, token):
        if Formatter.is_upper_case(token):
            return

        token.second_value = Formatter.to_lower(token.second_value, 0)

        i = 1
        while i < len(token.second_value):
            if token.second_value[i].isupper():
                token.second_value = Formatter.to_lower(token.second_value, i)
                token.second_value = Formatter.insert_into_string(token.second_value, i, '_')
            i += 1

        for i in range(len(token.second_value)):
            token.second_value = Formatter.to_upper(token.second_value, i)

        if token.second_value[0] == '_':
            token.second_value = token.second_value[1:]
        if token.second_value[-1] == '_':
            token.second_value = token.second_value[:-1]

        self.replace_all_tokens_like_this(token)

    # fix
    def fix_names(self, file):
        stack = []
        for i in range(len(file.tokens)):
            token = file.tokens[i]

            if token.value in class_interface_enum:
                stack.append(token.value)
                class_id = self.get_next_no_whitespace_token_id(file, i)
                self.replace_to_camel_case_first_up(file.tokens[class_id])

            elif ((len(stack) > 0 and stack[-1] in class_interface_enum) or
                  (len(stack) > 1 and stack[-2] in class_interface_enum and stack[-1] == '{')) and token.value == '<':
                generic_stack = [token]
                while len(generic_stack) != 0:
                    i += 1
                    token = file.tokens[i]
                    if token.value == '>':
                        generic_stack.pop()
                    elif token.value == '<':
                        generic_stack.append(token)
                    elif token.token_type == TokenType.identifier:
                        self.replace_to_camel_case_first_up(token)

            elif token.value == '{':
                stack.append(token.value)
            elif token.value == '}':
                stack.pop()
                if len(stack) > 0 and stack[-1] in class_interface_enum:
                    stack.pop()
            elif token.value == '(':
                stack.append(token.value)
            elif token.value == ')':
                stack.pop()

            if token.token_type == TokenType.identifier:
                next_token = file.tokens[self.get_next_no_whitespace_token_id(file, i)]
                prev_token = file.tokens[self.get_prev_no_whitespace_token_id(file, i)]

                if len(stack) > 1 and stack[-2] in class_interface_enum and stack[-1] == '{':  # in class

                    if next_token.value == '(':  # is method declaration
                        self.replace_to_camel_case_first_down(token)
                    elif next_token.value in (';', '='):  # is variable
                        end_of_search = Formatter.get_previous_token_id_with_such_value(file.tokens, i, ('{', '}', ';'))
                        if Formatter.get_previous_token_id_with_such_value(file.tokens, i, ('final',)) > end_of_search:
                            # final variable
                            self.replace_to_upper_case(token)
                        else:
                            self.replace_to_camel_case_first_down(token)

                elif len(stack) > 1 and next_token.value == '->':  # in lambda
                    self.replace_to_camel_case_first_down(token)

                elif len(stack) > 2 and stack[-2] == '{' and stack[-1] in ('(', '{'):  # in method
                    if stack[-1] == '(':
                        after_tokens = (')', ',')
                    else:
                        after_tokens = (';', '=', ':')

                    if (prev_token.value in ('>', ']',) or prev_token.token_type in (
                            TokenType.identifier, TokenType.keyword)) and \
                            next_token.value in after_tokens:
                        self.replace_to_camel_case_first_down(token)

    @staticmethod
    def insert_new_line(file, index):
        file.tokens.insert(index, Token(TokenType.whitespace, '\n', file.tokens[index].position))

    @staticmethod
    def add_indents(file, index, indent):
        for i in range(indent):
            file.tokens.insert(index, Token(TokenType.whitespace, ' ', file.tokens[index + i].position))

    @staticmethod
    def fix_beginning_comment(file):
        first_token = file.tokens[Formatter.get_next_no_whitespace_token_id(file, -1)]
        if first_token.value[0:2] != '/*':
            new_token = Token(TokenType.comment, '''/*
 * %W% %E% Firstname Lastname
 *
 * Copyright (c) 1995-2020 %your company name%
 *
 * This software is the confidential and proprietary information of 
 * %your company name%.  You shall not
 * disclose such Confidential Information and shall use it only in
 * accordance with the terms of the license agreement you entered into
 * with %your company name%.
 *
 * %your company name% MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY OF
 * THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
 * TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
 * PARTICULAR PURPOSE, OR NON-INFRINGEMENT. SUN SHALL NOT BE LIABLE FOR
 * ANY DAMAGES SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING OR
 * DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.
 */''', Position(1, 1))
            file.tokens.insert(0, new_token)
            Formatter.insert_new_line(file, 1)

    @staticmethod
    def get_first_token_id_of_statement(file, index):
        while True:
            whitespace_id = Formatter.get_previous_token_id_with_such_value(file.tokens, index, ('\n',))
            previous_no_whitespace_token = file.tokens[Formatter.get_prev_no_whitespace_token_id(file, whitespace_id)]
            if not (previous_no_whitespace_token.token_type == TokenType.annotation
                    or previous_no_whitespace_token.value == ')'):
                return Formatter.get_next_no_whitespace_token_id(file, whitespace_id)
            index = whitespace_id

    @staticmethod
    def fix_comment_before_class_declaration(file, class_index):
        class_name = file.tokens[Formatter.get_next_no_whitespace_token_id(file, class_index)].second_value
        class_type = file.tokens[class_index]

        first_token_of_statement_id = Formatter.get_first_token_id_of_statement(file, class_index)
        first_token_of_statement = file.tokens[first_token_of_statement_id]
        indent = first_token_of_statement.position.column - 1

        previous_token = file.tokens[Formatter.get_prev_no_whitespace_token_id(file, first_token_of_statement_id)]
        if previous_token.second_value[0:3] == '/**':
            was_new_line = previous_token.second_value[3] == '\n'  # TODO add for all
            if class_name not in previous_token.second_value:
                new_line = '' if was_new_line else '\n'
                previous_token.second_value = '/**\n' + ' ' * indent + f' * The {class_name} {class_type} provides ' + \
                                              new_line + previous_token.second_value[3:]
            # TODO add fix end of token for all
        else:
            token = Token(TokenType.comment, '', first_token_of_statement.position)
            token.second_value = '/**\n' + ' ' * indent + f' * The {class_name} {class_type} provides \n' + ' ' \
                                 * indent + ' */'
            file.tokens.insert(first_token_of_statement_id, token)
            Formatter.insert_new_line(file, first_token_of_statement_id + 1)
            Formatter.add_indents(file, first_token_of_statement_id + 2, indent)

    @staticmethod
    def fix_comment_before_method_declaration(file, method_name_index):
        pass

    @staticmethod
    def fix_comment_before_field(file, field_name_id):
        field_name = file.tokens[field_name_id]
        first_token_of_statement_id = Formatter.get_first_token_id_of_statement(file, field_name_id)
        first_token_of_statement = file.tokens[first_token_of_statement_id]
        indent = first_token_of_statement.position.column - 1

        previous_token = file.tokens[Formatter.get_prev_no_whitespace_token_id(file, first_token_of_statement_id)]
        pass

    @staticmethod
    def fix_another_comments(file):
        stack = []
        i = 0
        while i < len(file.tokens):
            token = file.tokens[i]
            next_token = file.tokens[Formatter.get_next_no_whitespace_token_id(file, i)]
            if token.value in class_interface_enum and next_token.token_type == TokenType.identifier:
                stack.append(token.value)
                Formatter.fix_comment_before_class_declaration(file, i)

            elif token.value == '{':
                stack.append(token.value)
            elif token.value == '}':
                stack.pop()
                if len(stack) > 0 and stack[-1] in class_interface_enum:
                    stack.pop()
            elif token.value == '(':
                stack.append(token.value)
            elif token.value == ')':
                stack.pop()

            if len(stack) > 1 and stack[-2] in class_interface_enum and stack[-1] == '{':  # in class
                if token.token_type == TokenType.identifier:  # identifier (method name or value)

                    if next_token.token_type == '(':  # method declaration
                        Formatter.fix_comment_before_method_declaration(file, i)
                    elif next_token.value in (';', '='):  # is variable
                        Formatter.fix_comment_before_field(file, i)

            i += 1

    @staticmethod
    def fix_comments(file):
        Formatter.fix_beginning_comment(file)
        Formatter.fix_another_comments(file)

    def format_files(self):
        for file in self.files:
            self.fix_names(file)
            Formatter.fix_comments(file)
