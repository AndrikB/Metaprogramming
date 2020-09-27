from pathlib import Path


def getFiles(path):
    result = list(Path(path).rglob("*.[jJ][aA][vV][aA]"))
    print(result)
    return result
