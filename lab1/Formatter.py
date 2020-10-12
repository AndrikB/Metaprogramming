import config
from Lexer import Token, TokenType, Position


def format_tokens(tokens, config_file):
    formatter = Formatter(tokens, config_file)
    formatter.format()
    return formatter.tokens


def replace_tab_to_space(tokens):
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.value == '\t':
            next_token = tokens[i + 1]
            token.value = ' '
            while token.position.column + 1 != next_token.position.column:
                i += 1
                token = Token(TokenType.whitespace, ' ', Position(token.position.row, token.position.column + 1))
                tokens.insert(i, token)
        i += 1


class Formatter:
    newline_token = Token(TokenType.whitespace, '\n')
    space_token = Token(TokenType.whitespace, ' ')
    other_tokens_in_stack = ('if', 'else', 'for', 'while', 'do', 'switch', 'try')  # todo add another if need

    def __init__(self, tokens, config_file='template.json'):
        self.tokens = tokens
        self.config = config.Config(config_file)
        self.i = 0

    def find_by_value(self, value, _from=0, to=-1):
        if to == -1:
            to = len(self.tokens)
        if to > len(self.tokens):
            to = len(self.tokens)
        while _from < to:
            if self.tokens[_from].value == value:
                return _from
            _from += 1
        return -1

    def find_by_type(self, token_type, _from=0, to=-1):
        if to == -1:
            to = len(self.tokens)
        while _from < to:
            if self.tokens[_from].token_type == token_type:
                return _from
            _from += 1
        return -1

    def get_next_no_whitespace_token_id(self, _id):
        while _id < len(self.tokens):
            _id += 1
            if self.tokens[_id].token_type != TokenType.whitespace:
                return _id
        return -1

    def get_prev_no_whitespace_token_id(self, _id):
        while _id > 0:
            _id -= 1
            if self.tokens[_id].token_type != TokenType.whitespace:
                return _id
        return -1

    def remove_whitespaces_before_token(self):
        pass

    def remove_whitespaces_after_token(self):
        while self.tokens[self.i + 1].token_type == TokenType.whitespace:
            self.tokens.pop(self.i + 1)

    def remove_all_tabs_and_spaces(self):
        i = 0
        while i < len(self.tokens):
            if self.tokens[i].value in (' ', '\t'):
                self.tokens.pop(i)
            else:
                i += 1

    def keep_maximum_new_lines(self, _max, pos):
        while self.tokens[pos].value == '\n':
            if _max == 0:
                self.tokens.pop(pos)
            else:
                _max -= 1
                pos += 1

    def fix_new_lines(self):
        i = 1
        stack = []
        was_annotation = False

        def add_new_line_if_missing(position):
            if self.tokens[position].value != '\n':
                self.tokens.insert(position, Formatter.newline_token)

        while i < len(self.tokens) - 1:
            prev_token = self.tokens[i - 1]
            token = self.tokens[i]
            next_token = self.tokens[i + 1]

            if token.value in self.other_tokens_in_stack:
                stack.append(token.value)

            if was_annotation and token.value != '(' and stack[len(stack) - 1][0] == '@':
                add_new_line_if_missing(i)
                self.keep_maximum_new_lines(1, i)
                stack.pop()
                was_annotation = False
                continue

            if token.value == '{':
                stack.append(token.value)
                if prev_token.value not in ('(', ']', '='):
                    add_new_line_if_missing(i + 1)

            elif token.value == '}':
                while stack.pop() != '{':
                    pass

                if next_token.value == 'else' and not self.config.else_on_new_line or \
                        (next_token.value == 'while' and not self.config.while_on_new_line and
                         len(stack) > 1 and stack[len(stack) - 1] == 'do') or \
                        next_token.value == 'catch' and not self.config.catch_on_new_line or \
                        next_token.value == 'finally' and not self.config.finally_on_new_line:
                    i += 1
                    if len(stack) > 1 and stack[len(stack) - 1] in self.other_tokens_in_stack:
                        stack.pop()  # 'if', 'class', 'for', method, ...
                    stack.append(next_token.value)

                else:
                    if len(stack) > 1 and stack[len(stack) - 1] in self.other_tokens_in_stack:
                        stack.pop()  # 'if', 'class', 'for', method, ...

                    if next_token.value not in (';', ')'):
                        add_new_line_if_missing(i + 1)

            elif token.value == ';':
                if not (len(stack) > 1 and stack[len(stack) - 1] == '('):
                    add_new_line_if_missing(i + 1)
                else:
                    pass
                    # stack.pop()

            elif token.value == ':' and \
                    (self.tokens[i - 2].value == 'case' or self.tokens[i - 1].value == 'default'):
                if next_token.value != '{':
                    add_new_line_if_missing(i + 1)
                    i += 1

            elif token.value == '\n':
                if len(stack) > 0 and stack[len(stack) - 1] in self.other_tokens_in_stack:
                    stack.pop()
                elif not (prev_token.value in (')', ';', '{', '}', '\n') or
                          (len(stack) > 1 and stack[len(stack) - 1] in self.other_tokens_in_stack) or
                          prev_token.token_type in (TokenType.annotation, TokenType.comment)):
                    self.tokens.pop(i)
                    i -= 1

            elif token.value == '(':
                stack.append(token.value)
            elif token.value == ')':
                while stack.pop() != '(':
                    pass

            elif token.token_type == TokenType.identifier and \
                    len(stack) > 1 and stack[len(stack) - 1] in ('for', 'while', 'do', 'if', 'else'):
                add_new_line_if_missing(i)
                stack.pop()

            elif token.token_type == TokenType.annotation:
                was_annotation = True
                stack.append(token.value)

            i += 1
        pass

    def add_tabs(self):
        indent = 0
        temp_indent = 0
        case_indent = 0
        need_indent = False
        i = 1

        def add_tabs():
            nonlocal indent
            nonlocal temp_indent
            nonlocal case_indent
            nonlocal i
            nonlocal need_indent
            for l_i in range(indent + temp_indent + case_indent):
                self.tokens.insert(i, Formatter.space_token)
                i += 1
            temp_indent = 0
            need_indent = False

        stack = []
        while i < len(self.tokens):
            token = self.tokens[i]
            # prev_token = self.tokens[i - 1]
            # next_token = self.tokens[i - 1]

            if need_indent and token.value not in ('}', 'case'):
                if not ('switch' in stack and token.value == 'default'):
                    add_tabs()

            if token.value in self.other_tokens_in_stack:
                # if len(stack) > 0 and stack[len(stack) - 1] not in self.other_tokens_in_stack:
                stack.append(token.value)

            elif token.value == '{':
                case_indent = 0  # it may be when 'case 0: { some code }
                stack.append(token.value)
                indent += self.config.indent_spaces_count

            elif token.value == '}':
                while stack.pop() != '{':
                    pass
                if len(stack) > 1 and stack[len(stack) - 1] in self.other_tokens_in_stack:
                    stack.pop()  # 'if', 'class', 'for', method, ...
                indent -= self.config.indent_spaces_count
                case_indent = 0  # it may be when 'case 0: { some code }
                if need_indent:
                    add_tabs()

            elif token.value == 'case' or ('switch' in stack and token.value == 'default'):
                case_indent = 0
                add_tabs()
                case_indent = self.config.indent_spaces_count

            elif token.value == '\n':
                need_indent = True
                if len(stack) > 1 and stack[len(stack) - 1] in self.other_tokens_in_stack:
                    temp_indent += self.config.indent_spaces_count
                    stack.pop()
                elif self.tokens[i - 1].value == ')' and self.tokens[i + 1].value == '.':
                    temp_indent += self.config.continuation_indent_spaces_count

            elif token.value == ';':
                if len(stack) > 1 and stack[len(stack) - 1] in self.other_tokens_in_stack:
                    stack.pop()
                temp_indent = 0

            i += 1

    def add_spaces_between_words(self):
        i = 1
        types = (TokenType.keyword, TokenType.identifier, TokenType.number_literal, TokenType.string_literal)
        while i < len(self.tokens):
            if (self.tokens[i - 1].token_type in types or self.tokens[i - 1].value == ']') \
                    and self.tokens[i].token_type in types:
                self.tokens.insert(i, Formatter.space_token)
                i += 1
            i += 1

    def add_spaces_around_operators(self):
        def add_spaces_around_operator(operators, space):
            if not space:
                return
            i = 0
            while i < len(self.tokens):
                if self.tokens[i].value in operators:
                    self.tokens.insert(i, Formatter.space_token)
                    self.tokens.insert(i + 2, Formatter.space_token)
                    i += 2
                i += 1

        def add_spaces_around_plus_and_minus(space_additive, space_unary):

            def is_unary_operator(operator_id):
                operator_id -= 1
                while self.tokens[operator_id].value == ' ':
                    operator_id -= 1
                token = self.tokens[operator_id]
                if token.token_type != TokenType.operator:  # ex: a + b
                    return False
                if token.value in ('++', '--'):  # ex a++ + b
                    return False
                return True

            operators = ('-', '+')
            i = 0
            if space_additive:
                while i < len(self.tokens):
                    if self.tokens[i].value in operators and not is_unary_operator(i):
                        self.tokens.insert(i, Formatter.space_token)
                        self.tokens.insert(i + 2, Formatter.space_token)
                        i += 2
                    i += 1

            i = 0
            if space_unary:
                while i < len(self.tokens):
                    if self.tokens[i].value in operators and is_unary_operator(i):
                        self.tokens.insert(i, Formatter.space_token)
                        self.tokens.insert(i + 2, Formatter.space_token)
                        i += 2
                    i += 1

        def add_spaces_around_angle_brackets(space_operator, space_before_generic, space_after_generic):
            if (not space_operator) and (not space_before_generic) and (not space_after_generic):
                return

            def is_generic(angle_open_id):
                angle_open_id += 1
                while self.tokens[angle_open_id].token_type == TokenType.whitespace:
                    angle_open_id += 1
                c = self.tokens[angle_open_id].value[0]
                return c.isalpha() and c.isupper() or c in ('?', '>')

            i = 0
            count_open = 0

            while i < len(self.tokens):
                token = self.tokens[i]
                if token.value == '<':
                    if is_generic(i):
                        count_open += 1
                        if space_before_generic or self.tokens[i - 1].token_type == TokenType.keyword:
                            self.tokens.insert(i, Formatter.space_token)
                            i += 1

                    elif space_operator:
                        self.tokens.insert(i, Formatter.space_token)
                        self.tokens.insert(i + 2, Formatter.space_token)
                        i += 2
                elif token.value == '>':
                    if count_open > 0:  # is generic
                        count_open -= 1
                        if count_open == 0:
                            if space_after_generic:
                                self.tokens.insert(i + 1, Formatter.space_token)
                                i += 1
                            elif self.tokens[i + 1].token_type == TokenType.identifier and \
                                    self.tokens[i + 2].value != '(':
                                self.tokens.insert(i + 1, Formatter.space_token)
                                i += 1
                    elif space_operator:
                        self.tokens.insert(i, Formatter.space_token)
                        self.tokens.insert(i + 2, Formatter.space_token)
                        i += 2
                i += 1

        add_spaces_around_operator(
            ('=', '+=', '-=', '>>>=', '>>=', '<<=', '%=', '^=', '|=', '&=', '/=', '*=', '-=', '+='),
            self.config.spaces_around_assignment_operators)
        add_spaces_around_operator(('&&', '||'), self.config.spaces_around_logical_operators)
        add_spaces_around_operator(('==', '!='), self.config.spaces_around_equality_operators)
        add_spaces_around_operator(('>=', '<='), self.config.spaces_around_relational_operators)

        add_spaces_around_angle_brackets(self.config.spaces_around_relational_operators,
                                         self.config.space_before_opening_angle_bracket,
                                         self.config.space_after_opening_angle_bracket)

        add_spaces_around_operator(('&', '|', '^'), self.config.spaces_around_bitwise_operators)  # T extend A & B ?

        add_spaces_around_plus_and_minus(self.config.spaces_around_additive_operators,
                                         self.config.spaces_around_unary_operators)

        add_spaces_around_operator(('*', '/', '%'), self.config.spaces_around_multiplicative_operators)
        add_spaces_around_operator(('>>>', '>>', '<<'), self.config.spaces_around_shift_operators)
        add_spaces_around_operator(('!', '++', '--'), self.config.spaces_around_unary_operators)
        add_spaces_around_operator(('->', ''), self.config.spaces_around_lambda_arrow)
        add_spaces_around_operator('::', self.config.spaces_around_method_reference_double_colon)

    def add_spaces_before_parentheses(self):
        def add_space_after_word_before_bracket(word, space):
            if not space:
                return
            i = 0
            while i + 1 < len(self.tokens):
                if self.tokens[i].value == word and self.tokens[i + 1].value == '(':
                    self.tokens.insert(i + 1, Formatter.space_token)
                    i += 1
                i += 1

        def add_space_after_method(space_declaration, space_call):
            if (not space_declaration) and (not space_call):
                return
            i = 0

            def is_method_declaration(index):
                index -= 1
                while index >= 0 and self.tokens[index].token_type == TokenType.whitespace:
                    index -= 1
                if index == -1:
                    return False

                if self.tokens[index].token_type in (TokenType.identifier, TokenType.keyword):
                    return True
                else:
                    return False

            while i + 1 < len(self.tokens):
                if self.tokens[i].token_type == TokenType.identifier and \
                        self.tokens[i + 1].value == '(':  # is method
                    if is_method_declaration(i):
                        if space_declaration:
                            self.tokens.insert(i + 1, Formatter.space_token)
                            i += 1
                    else:
                        if space_call:
                            self.tokens.insert(i + 1, Formatter.space_token)
                            i += 1
                i += 1

        def add_space_after_annotation_before_parentheses(space):
            if not space:
                return
            i = 0
            while i + 1 < len(self.tokens):
                if self.tokens[i].token_type == TokenType.annotation and self.tokens[i + 1].value == '(':
                    self.tokens.insert(i + 1, Formatter.space_token)
                    i += 1
                i += 1

        add_space_after_method(self.config.space_before_method_declaration_parentheses,
                               self.config.space_before_method_call_parentheses)
        add_space_after_word_before_bracket('if', self.config.space_before_if_parentheses)
        add_space_after_word_before_bracket('for', self.config.space_before_for_parentheses)
        add_space_after_word_before_bracket('while', self.config.space_before_while_parentheses)
        add_space_after_word_before_bracket('switch', self.config.space_before_switch_parentheses)
        add_space_after_word_before_bracket('try', self.config.space_before_try_parentheses)
        add_space_after_word_before_bracket('catch', self.config.space_before_catch_parentheses)
        add_space_after_word_before_bracket('synchronized', self.config.space_before_synchronized_parentheses)
        add_space_after_annotation_before_parentheses(self.config.space_before_annotation_parentheses)

    def add_spaces_before_left_brace(self):

        def add_space_before_left_brace_after_keyword_and_spaces(keyword, space):
            if not space:
                return

            def insert_space_before_first_brace(index):
                index += 1
                count_bracket = 0
                while index < len(self.tokens):
                    token = self.tokens[index]
                    if token.value == 'if':  # for '} else if() {'
                        return
                    if token.value == '\n':
                        return
                    if token.value == '(':
                        count_bracket += 1
                    elif token.value == ')':
                        count_bracket -= 1
                        if count_bracket == -1:
                            return
                    elif count_bracket == 0 and token.value == '{':
                        self.tokens.insert(index, Formatter.space_token)
                        return
                    index += 1

            i = 0
            while i < len(self.tokens):
                if self.tokens[i].value == keyword:
                    insert_space_before_first_brace(i)
                i += 1

        def add_space_before_left_brace_after_method_declaration(space):
            if not space:
                return
            i = 0
            while i < len(self.tokens):
                if self.tokens[i].token_type == TokenType.identifier:
                    next_id = self.get_next_no_whitespace_token_id(i)
                    if next_id == -1:
                        return
                    if self.tokens[next_id].value == '(':
                        next_id = self.find_by_value(')', next_id)
                        if self.tokens[next_id + 1].value == '{':
                            self.tokens.insert(next_id + 1, Formatter.space_token)
                i += 1

        add_space_before_left_brace_after_keyword_and_spaces('class', self.config.space_before_class_left_brace)
        add_space_before_left_brace_after_method_declaration(self.config.space_before_method_left_brace)
        add_space_before_left_brace_after_keyword_and_spaces('if', self.config.space_before_if_left_brace)
        add_space_before_left_brace_after_keyword_and_spaces('else', self.config.space_before_else_left_brace)
        add_space_before_left_brace_after_keyword_and_spaces('for', self.config.space_before_for_left_brace)
        add_space_before_left_brace_after_keyword_and_spaces('while', self.config.space_before_while_left_brace)
        add_space_before_left_brace_after_keyword_and_spaces('do', self.config.space_before_do_left_brace)
        add_space_before_left_brace_after_keyword_and_spaces('switch', self.config.space_before_switch_left_brace)
        add_space_before_left_brace_after_keyword_and_spaces('case', self.config.space_before_switch_left_brace)
        add_space_before_left_brace_after_keyword_and_spaces('try', self.config.space_before_try_left_brace)
        add_space_before_left_brace_after_keyword_and_spaces('catch', self.config.space_before_catch_left_brace)
        add_space_before_left_brace_after_keyword_and_spaces('finally', self.config.space_before_finally_left_brace)
        add_space_before_left_brace_after_keyword_and_spaces('synchronized',
                                                             self.config.space_before_synchronized_left_brace)

    def add_spaces_before_keywords(self):
        def add_space_between_brace_and_keyword(keyword, space):
            if not space:
                return
            i = 1

            while i < len(self.tokens):
                if self.tokens[i].value == keyword and self.tokens[i - 1].value == '}':
                    self.tokens.insert(i, Formatter.space_token)
                    i += 1
                i += 1

        add_space_between_brace_and_keyword('else', self.config.space_before_else_keyword)
        add_space_between_brace_and_keyword('while', self.config.space_before_while_keyword)
        add_space_between_brace_and_keyword('catch', self.config.space_before_catch_keyword)
        add_space_between_brace_and_keyword('finally', self.config.space_before_finally_keyword)

    def add_spaces_in_ternary(self):
        i = 0

        def insert_space_if_true(position, condition):
            if condition:
                self.tokens.insert(position, Formatter.space_token)

        while i < len(self.tokens):
            if self.tokens[i].value == '?':  # may be start of ternary
                colon = self.find_by_value(':', i, i + 10)
                if colon != -1:  # it is real ternary
                    insert_space_if_true(colon + 1, self.config.space_in_ternary_after_colon)
                    insert_space_if_true(colon, self.config.space_in_ternary_before_colon)
                    insert_space_if_true(i + 1, self.config.space_in_ternary_after_question)
                    insert_space_if_true(i, self.config.space_in_ternary_before_question)
                    i += 1
            i += 1

    def add_other_spaces(self):

        def add_space_after_type_cast():
            if not self.config.space_after_type_cast:
                return
            l_i = 1
            while l_i < len(self.tokens):
                if self.tokens[l_i].value == '(' and \
                        self.tokens[self.get_prev_no_whitespace_token_id(l_i)].token_type \
                        not in (TokenType.identifier, TokenType.keyword) and \
                        self.tokens[l_i + 1].token_type in (TokenType.keyword, TokenType.identifier):  # (ident
                    if self.tokens[l_i + 2].value == ')':
                        l_i += 3
                        self.tokens.insert(l_i, Formatter.space_token)
                    elif self.tokens[l_i + 2].value == '[' and self.tokens[l_i + 3].value == ']' \
                            and self.tokens[l_i + 4].value == ')':
                        l_i += 5
                        self.tokens.insert(l_i, Formatter.space_token)
                    elif self.tokens[l_i + 2].value == '<':
                        stack = ['(', '<']
                        l_i += 2
                        while len(stack) != 0:
                            l_i += 1
                            l_value = self.tokens[l_i].value
                            if l_value in ('[', '<'):
                                stack.append(l_value)
                            elif l_value == ']':
                                if stack[len(stack) - 1] == '[':
                                    stack.pop()
                                else:
                                    break
                            elif l_value == '>':
                                if stack[len(stack) - 1] == '<':
                                    stack.pop()
                                else:
                                    break
                            elif l_value == ')':
                                if stack[len(stack) - 1] == '(':
                                    stack.pop()
                                else:
                                    break
                            if len(stack) == 0:
                                self.tokens.insert(l_i + 1, Formatter.space_token)
                                break

                l_i += 1

        add_space_after_type_cast()
        was_for_try = False
        count_bracket = 0
        i = 0
        while i < len(self.tokens):
            value = self.tokens[i].value
            if value == ',':
                if self.config.space_before_comma:
                    self.tokens.insert(i, Formatter.space_token)
                    i += 1
                if self.config.space_after_comma:
                    i += 1
                    self.tokens.insert(i, Formatter.space_token)
            elif value in ('for', 'try'):
                was_for_try = True
            elif value == '(' and was_for_try:
                count_bracket += 1
            elif value == ')' and was_for_try:
                count_bracket -= 1
                if count_bracket == 0:
                    was_for_try = False
            elif value == ';' and was_for_try:
                if self.config.space_before_for_semicolon:
                    self.tokens.insert(i, Formatter.space_token)
                    i += 1
                if self.config.space_after_for_semicolon:
                    i += 1
                    self.tokens.insert(i, Formatter.space_token)
            elif value == ':' and was_for_try:
                if self.config.space_around_colon_in_foreach:
                    self.tokens.insert(i, Formatter.space_token)
                    self.tokens.insert(i + 2, Formatter.space_token)
                    i += 2
            i += 1

    def fix_spaces_and_newlines(self):
        ident = 0
        self.i = 0

        def add_spaces():
            whitespace = Token(TokenType.whitespace, ' ')
            for i in range(ident):
                self.tokens.insert(self.i, whitespace)
                self.i += 1

        while self.i < len(self.tokens):
            token = self.tokens[self.i]
            if token.value == '{':
                ident += self.config.indent_spaces_count
                self.i += 1
                add_spaces()

            elif token.value == ';':
                self.i += 1
                add_spaces()
            elif token.value == '{':
                ident += self.config.indent_spaces_count
                self.i += 1
                add_spaces()
            else:
                self.i += 1

    def format(self):
        self.remove_all_tabs_and_spaces()
        self.fix_new_lines()
        # add tabs
        self.add_tabs()
        self.add_spaces_between_words()
        self.add_spaces_before_parentheses()
        self.add_spaces_around_operators()
        self.add_spaces_before_left_brace()
        self.add_spaces_before_keywords()
        self.add_spaces_in_ternary()
        self.add_other_spaces()
        # self.fix_spaces_and_newlines()
