import sys

from Formatter import format_tokens
from Lexer import tokenize_file
from logs import write_logs
from utils import getFiles, print_to_file


def print_help():
    print(
        """
ILang SLangFormatter --verify -(p|d|f) /..
ILang SLangFormatter -v -(p|d|f) /..
ILang SLangFormatter --format template name -(p|d|f) /..
ILang SLangFormatter -f template name -(p|d|f) /..
ILang SLangFormatter --help
ILang SLangFormatter -h
ILang - implementation language
SLang - source language
-p - project
-d - directory
-f - file
/.. - path to project, directory or file
        """
    )


# config = Config("template.json")
# print(config)
#
# tokens = tokenize_file("test.txt")
# formatter = Formatter(tokens)
# formatter.format()
# print("-------------------------")
# print_to_file(formatter.tokens)

print(len(sys.argv))
print(sys.argv)

if len(sys.argv) == 1:
    print("Error! Please, write arguments", '\n')
    print_help()
else:
    if sys.argv[1] in ('-h', '--help'):
        print_help()
    elif len(sys.argv) not in (4, 5):
        print("Error! Please, write arguments", '\n')
        print_help()
    else:
        mode = sys.argv[1]
        if len(mode) > 2:
            mode = mode[1:3]

        config_file = "template.json"
        inc = 0
        if len(sys.argv) == 5:
            config_file = sys.argv[2]
            inc = 1

        p_d_f = sys.argv[2 + inc]
        path = sys.argv[3 + inc]

        if p_d_f in ('-p', '-d'):
            files = getFiles(path)
        else:
            files = [path]

        for file in files:
            tokens = tokenize_file(file)
            new_tokens = format_tokens(tokens.copy(), config_file)
            if mode == '-f':
                print_to_file(new_tokens, file)
            else:
                write_logs(tokens, new_tokens, file)
