import sys

from Formatter import format_tokens
from Lexer import tokenize_file
from logs import write_logs
from utils import get_files, print_to_file


def print_help():
    print(
        """
***************** examples *****************

python main.py --verify -(p|d|f) /..
python main.py -v -(p|d|f) /..
python main.py --format template_name -(p|d|f) /..
python main.py -f template_name -(p|d|f) /..
python main.py --help
python main.py -h

where :

-p - project
-d - directory
-f - file
/.. - path to project, directory or file
        """
    )


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
            files = get_files(path)
        else:
            files = [path]

        for file in files:
            tokens = tokenize_file(file)
            new_tokens = format_tokens(tokens.copy(), config_file)
            if mode == '-f':
                print_to_file(new_tokens, file)
            else:
                write_logs(tokens, new_tokens, file)
