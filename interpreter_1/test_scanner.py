import unittest
from scanner import Scanner
import io

class ScannerTest(unittest.TestCase):
    def test_plus(self):
        file_content = '+'
        scanner = Scanner(file_content)
        tokens = scanner.scan_tokens()
        self.assertEqual(tokens[0].type, 'PLUS')
        self.assertEqual(tokens[-1].type, 'EOF')

    def test_comment(self):
        file_content = '//'
        scanner = Scanner(file_content)
        tokens = scanner.scan_tokens()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[-1].type, 'EOF')

    def test_single_and_comment(self):
        file_content = '''
        +
        // ignore
        +
        '''
        scanner = Scanner(file_content)
        tokens = scanner.scan_tokens()
        self.assertEqual(len(tokens), 3)
        self.assertEqual(tokens[0].type, 'PLUS')
        self.assertEqual(tokens[1].type, 'PLUS')
        self.assertEqual(tokens[-1].type, 'EOF')

    def test_single_operators(self):
        file_content = '!*+-/=<>'
        scanner = Scanner(file_content)
        tokens = scanner.scan_tokens()
        self.assertEqual(len(tokens), 9) # <<< 8 operators and eof

    def test_two_char_operators(self):
        file_content = '<= >= =='
        scanner = Scanner(file_content)
        tokens = scanner.scan_tokens()
        self.assertEqual(len(tokens), 4) # <<< 3 operators and eof

    def test_invalid_token(self):
        file_content = '@' # <<< invalid token
        scanner = Scanner(file_content)
        tokens = scanner.scan_tokens()
        print(tokens)
        self.assertEqual(len(tokens), 1)


if __name__ == '__main__':
    unittest.main()
