import unittest
import main

class TestVariable(unittest.TestCase):

    def test_sum_var(self):
        text = '2+(var a=2)'
        result , error = main.run('<STDIN>',text)
        self.assertEqual(str(result), "४")

        text = 'var b=2'
        result , error = main.run('<STDIN>',text)

        text = 'b+a'
        result , error = main.run('<STDIN>',text)
        self.assertEqual(str(result), "४")

    def test_sub_var(self):
        text = '8-(var a=4)'
        result , error = main.run('<STDIN>',text)
        self.assertEqual(str(result), "४")

        text = 'var b=8'
        result , error = main.run('<STDIN>',text)

        text = 'b-a'
        result , error = main.run('<STDIN>',text)
        self.assertEqual(str(result), "४")

    def test_mul_var(self):
        text = '2*(var a=2)'
        result , error = main.run('<STDIN>',text)
        self.assertEqual(str(result), "४")

        text = 'var b=2'
        result , error = main.run('<STDIN>',text)

        text = 'b*a'
        result , error = main.run('<STDIN>',text)
        self.assertEqual(str(result), "४")

    def test_div_var(self):
        text = '8/(var a=2)'
        result , error = main.run('<STDIN>',text)
        self.assertEqual(str(result), "४")

        text = 'var b=8'
        result , error = main.run('<STDIN>',text)

        text = 'b/a'
        result , error = main.run('<STDIN>',text)
        self.assertEqual(str(result), "४")

        
    def test_div_var_float(self):
        text = '22/(var a=7)'
        result , error = main.run('<STDIN>',text)
        self.assertEqual(str(result), "३.१४२८५७१४२८५७१४३")

        text = 'var b=22'
        result , error = main.run('<STDIN>',text)

        text = 'b/a'
        result , error = main.run('<STDIN>',text)
        self.assertEqual(str(result), "३.१४२८५७१४२८५७१४३")