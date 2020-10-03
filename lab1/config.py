import json


class Config:

    def __init__(self, filename):
        template_file = open(filename)
        template_data = json.loads(template_file.read())

        self.use_tab_character = template_data["use_tab_character"]
        self.indent_spaces_count = template_data["indent_spaces_count"]
        self.keep_indent_of_empty_line = template_data["keep_indent_of_empty_line"]

        self.dont_indent_top_level_class_members = template_data["dont_indent_top_level_class_members"]
