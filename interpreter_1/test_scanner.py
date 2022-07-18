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

if __name__ == '__main__':
    unittest.main()
