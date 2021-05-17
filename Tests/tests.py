import unittest
import main

class TestArithmetic(unittest.TestCase):

    def test_sum(self):
        text = '2+2'
        result , error = main.run('<STDIN>',text)
        self.assertEqual(str(result), "४")

    def test_sub(self):
        text = '8-4'
        result , error = main.run('<STDIN>',text)
        self.assertEqual(str(result), "४")

    def test_mul(self):
        text = '2*2'
        result , error = main.run('<STDIN>',text)
        self.assertEqual(str(result), "४")

    def test_div(self):
        text = '8/2'
        result , error = main.run('<STDIN>',text)
        self.assertEqual(str(result), "४")
        
    def test_div_float(self):
        text = '22/7'
        result , error = main.run('<STDIN>',text)
        self.assertEqual(str(result), "३.१४२८५७१४२८५७१४३")


if __name__ == '__main__':
    unittest.main()