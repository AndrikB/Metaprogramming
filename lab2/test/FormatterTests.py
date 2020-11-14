import unittest

from AndrikBJavaCCF.formatter import Formatter
from AndrikBJavaCCF.lexer import Token, TokenType


class MyTestCase(unittest.TestCase):
    formatter = Formatter(())

    def test_to_upper(self):
        cases = (
            ('example', 0, 'Example'), ('example', 2, 'exAmple'), ('exAmple', 2, 'exAmple'), ('example', 6, 'examplE'),
            ('_example', 0, '_example'))
        for testcase in cases:
            self.assertEqual(testcase[2], self.formatter.to_upper(testcase[0], testcase[1]))

    def test_to_lover(self):
        cases = (
            ('EXample', 0, 'eXample'), ('EXAMPLE', 2, 'EXaMPLE'), ('EXaMPLE', 2, 'EXaMPLE'), ('EXAMPLE', 6, 'EXAMPLe'),
            ('_EXAMPLE', 0, '_EXAMPLE'))
        for testcase in cases:
            self.assertEqual(testcase[2], self.formatter.to_lower(testcase[0], testcase[1]))

    def test_replace_underscore_to_uppercase(self):
        cases = (
            ('_example', 'Example'), ('___example', 'Example'), ('_EXAMPLE', 'EXAMPLE'), ('exa___mple', 'exaMple'),
            ('e_xa__mp_le', 'eXaMpLe'), ('example_', 'example'))
        for testcase in cases:
            token = Token(TokenType.identifier, testcase[0])
            self.formatter.replace_underscore_to_uppercase(token)
            self.assertEqual(testcase[1], token.second_value)

    def test_replace_to_camel_case_first_down(self):
        cases = (
            ('example', 'example'), ('_example', 'example'), ('EXAMPLE', 'example'), ('EXA_MPLE', 'exaMple'),
            ('exa_mPle', 'exaMPle'), ('_example_', 'example'))
        for testcase in cases:
            token = Token(TokenType.identifier, testcase[0])
            self.formatter.replace_to_camel_case_first_down(token)
            self.assertEqual(testcase[1], token.second_value)

    def test_replace_to_camel_case_first_up(self):
        cases = (
            ('example', 'Example'), ('_example', 'Example'), ('_EXAMPLE', 'Example'), ('EXA_MPLE', 'ExaMple'),
            ('exa_mPle', 'ExaMPle'), ('_example_', 'Example'))
        for testcase in cases:
            token = Token(TokenType.identifier, testcase[0])
            self.formatter.replace_to_camel_case_first_up(token)
            self.assertEqual(testcase[1], token.second_value)

    def test_replace_to_upper_case(self):
        cases = (
            ('example', 'EXAMPLE'), ('_example_', 'EXAMPLE'), ('EXA_MPLE', 'EXA_MPLE'), ('exa_mPle', 'EXA_M_PLE'))
        for testcase in cases:
            token = Token(TokenType.identifier, testcase[0])
            self.formatter.replace_to_upper_case(token)
            self.assertEqual(testcase[1], token.second_value)

    def test_is_upper_case(self):
        cases_is = ('EXAMPLE', '_E_X_A_M_P_L_E_', '_____EXAMPLE')
        cases_is_not = ('EXaMPLE', '_E_X_a_M_P_L_E_', '_____ExAMPLE', 'eXAMPLE', 'ExAmPlE')
        for testcase in cases_is:
            token = Token(TokenType.identifier, testcase)
            self.assertTrue(self.formatter.is_upper_case(token))
        for testcase in cases_is_not:
            token = Token(TokenType.identifier, testcase)
            self.assertFalse(self.formatter.is_upper_case(token))

    # comments
    def test_fix_documentation_comment(self):
        indent = 0
        cases = (('/**comment*/', '/**\n * comment\n */'),
                 ('/**\t\t\t    \n*first line *continue first line\nsecond line\n ******      third line\t\n\n\t\t  */',
                  '/**\n * first line *continue first line\n * second line\n * *****      third line\n */'))
        for testcase in cases:
            token = Token(TokenType.comment, testcase[0])
            self.formatter.fix_documentation_comment(token, indent)
            print(token)
            self.assertEqual(testcase[1], token.second_value)


if __name__ == '__main__':
    unittest.main()
