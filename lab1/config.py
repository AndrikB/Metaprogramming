import json


class Config:

    def __init__(self, filename):
        template_file = open(filename)
        template_data = json.loads(template_file.read())

        self.indent_spaces_count = template_data["indent_spaces_count"]
        self.keep_indent_of_empty_line = template_data["keep_indent_of_empty_line"]

        self.label_ident = template_data["label_ident"]
        self.absolute_label_ident = template_data["absolute_label_ident"]
        self.dont_indent_top_level_class_members = template_data["dont_indent_top_level_class_members"]

        # spaces
        spaces = template_data["spaces"]
        if spaces:

            before_parentheses = spaces["before_parentheses"]
            if before_parentheses:
                self.space_before_method_declaration_parentheses = before_parentheses["method_declaration_parentheses"]
                self.space_before_method_call_parentheses = before_parentheses["method_call_parentheses"]
                self.space_before_if_parentheses = before_parentheses["if_parentheses"]
                self.space_before_for_parentheses = before_parentheses["for_parentheses"]
                self.space_before_while_parentheses = before_parentheses["while_parentheses"]
                self.space_before_switch_parentheses = before_parentheses["switch_parentheses"]
                self.space_before_try_parentheses = before_parentheses["try_parentheses"]
                self.space_before_catch_parentheses = before_parentheses["catch_parentheses"]
                self.space_before_synchronized_parentheses = before_parentheses["synchronized_parentheses"]
                self.space_before_annotation_parentheses = before_parentheses["annotation_parentheses"]

            around_operators = spaces["around_operators"]
            if around_operators:
                self.spaces_around_assignment_operators = around_operators["assignment_operators"]
                self.spaces_around_logical_operators = around_operators["logical_operators"]
                self.spaces_around_equality_operators = around_operators["equality_operators"]
                self.spaces_around_relational_operators = around_operators["relational_operators"]
                self.spaces_around_bitwise_operators = around_operators["bitwise_operators"]
                self.spaces_around_additive_operators = around_operators["additive_operators"]
                self.spaces_around_multiplicative_operators = around_operators["multiplicative_operators"]
                self.spaces_around_shift_operators = around_operators["shift_operators"]
                self.spaces_around_unary_operators = around_operators["unary_operators"]
                self.spaces_around_lambda_arrow = around_operators["lambda_arrow"]
                self.spaces_around_method_reference_double_colon = around_operators["method_reference_double_colon"]

