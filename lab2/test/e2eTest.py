import unittest

from AndrikBJavaCCF.file import File
from AndrikBJavaCCF.formatter import Formatter
from AndrikBJavaCCF.lexer import TokenType

filenames = (
    ('Test1Before.java', 'Test1After.java'), ('Test2Before.java', 'Test2After.java'),
    ('Test3Before.java', 'Test3After.java'))

files = []
for filename_before, filename_after in filenames:
    files.append((File('cases/' + filename_before), File('cases/' + filename_after)))


class MyTestCase(unittest.TestCase):

    def test_single_file(self):
        for file_before, file_after in files:
            formatter = Formatter((file_before,))
            formatter.format_files()
            i = j = 0
            while i < len(file_before.tokens) and j < len(file_after.tokens):
                token_before = file_before.tokens[i]
                token_after = file_after.tokens[j]

                if token_after.token_type == TokenType.whitespace:
                    i += 1
                if token_before.token_type == TokenType.whitespace:
                    j += 1

                self.assertEqual(token_before.second_value, token_after.second_value,
                                 f'error in files {file_before.filename} -> {file_after.filename}\n'
                                 f'tokens {token_before} -> {token_after}')
                i += 1
                j += 1


if __name__ == '__main__':
    unittest.main()
