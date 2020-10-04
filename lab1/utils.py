from pathlib import Path


def getFiles(path):
    result = list(Path(path).rglob("*.[jJ][aA][vV][aA]"))
    print(result)
    return result


def print_to_file(tokens, filename='result.txt'):
    file = open(filename, mode='w')
    for token in tokens:
        file.write(token.value)
    file.close()
