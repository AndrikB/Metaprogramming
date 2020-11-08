import sys

from .file import File
from .formatter import format_files, get_files, get_files_rec

__version__ = "0.1.1"


def print_help():
    print(
        """
***************** examples *****************
name --verify -(p|d|f) /..
name -v -(p|d|f) /..
name --fix -(p|d|f) /..
name -f  -(p|d|f) /..
name --help
name -h
where :
-p - project
-d - directory
-f - file
/.. - path to project, directory or file
        """
    )


def main():
    if len(sys.argv) == 1:
        print("Error! Please, write arguments", '\n')
        print_help()
    else:
        if sys.argv[1] in ('-h', '--help'):
            print_help()
        elif len(sys.argv) != 4:
            print("Error! Please, write arguments\n")
            print_help()
        else:
            mode = sys.argv[1]
            if len(mode) > 2:
                mode = mode[1:3]

            p_d_f = sys.argv[2]
            path = sys.argv[3]

            if p_d_f == '-p':
                files = get_files_rec(path)
            elif p_d_f == '-d':
                files = get_files(path)
            else:
                files = [path]

            for i in range(len(files)):
                files[i] = File(files[i])

            format_files(files)
