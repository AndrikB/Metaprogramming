import sys

from Lexer import tokenize_file
from parse_dir import getFiles


def print_help():
    print(
        """help message
            todo change
        """
    )


if len(sys.argv) == 1:
    print("Error! Please, write arguments")
else:
    if sys.argv[1] in ('-h', '--help'):
        print_help()
    else:
        tokenize_file(getFiles(".")[0])
