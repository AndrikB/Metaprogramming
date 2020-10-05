import config
from Lexer import Token, TokenType, Position


class Formatter:
    newline_token = Token(TokenType.whitespace, '\n')
    space_token = Token(TokenType.whitespace, ' ')

    def __init__(self, tokens, config_file='template.json'):
        self.tokens = tokens
        self.config = config.Config(config_file)
        self.i = 0

    def find_by_value(self, value, _from=0, to=-1):
        if to == -1:
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

    def remove_whitespaces_before_token(self):
        pass

    def remove_whitespaces_after_token(self):
        while self.tokens[self.i + 1].token_type == TokenType.whitespace:
            self.tokens.pop(self.i + 1)

    def replace_tab_to_space(self):
        i = 0
        while i < len(self.tokens):
            token = self.tokens[i]
            if token.value == '\t':
                next_token = self.tokens[i + 1]
                token.value = ' '
                while token.position.column + 1 != next_token.position.column:
                    i += 1
                    token = Token(TokenType.whitespace, ' ', Position(token.position.row, token.position.column + 1))
                    self.tokens.insert(i, token)
            i += 1

    def remove_all_tabs_and_spaces(self):
        i = 0
        while i < len(self.tokens):
            if self.tokens[i].value in (' ', '\t'):
                self.tokens.pop(i)
            else:
                i += 1

    def add_spaces_between_words(self):
        i = 1
        types = (TokenType.keyword, TokenType.identifier, TokenType.number_literal, TokenType.string_literal)
        while i < len(self.tokens):
            if self.tokens[i - 1].token_type in types and self.tokens[i].token_type in types:
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
                        if space_before_generic:
                            self.tokens.insert(i, Formatter.space_token)
                            i += 1

                    elif space_operator:
                        self.tokens.insert(i, Formatter.space_token)
                        self.tokens.insert(i + 2, Formatter.space_token)
                        i += 2
                elif token.value == '>':
                    if count_open > 0:  # is generic
                        count_open -= 1
                        if space_after_generic:
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

        add_spaces_around_angle_brackets(self.config.spaces_around_relational_operators, False, False)  # todo
        # todo add space if generic parameter in method "void foo(List<A>b)"

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
        pass

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
        # fix new lines
        # add tabs
        self.add_spaces_between_words()
        self.add_spaces_before_parentheses()
        self.add_spaces_around_operators()
        self.add_spaces_before_left_brace()
        # self.fix_spaces_and_newlines()
