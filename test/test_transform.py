import unittest
from transform import Transform
from mock import MagicMock

class Mytest(unittest.TestCase):
    def setUp(self):
        self.transform = Transform()

    def tearDown(self):
        pass

    def testFormat(self):
        exp = "3+2-6/1*4"
        self.assertEqual(self.transform.format(exp), exp)
        exp = "-3+2-6/1*4"
        self.assertEqual(self.transform.format(exp), "0-3+2-6/1*4")
        exp = "-3+(-2-6/1*4)"
        self.assertEqual(self.transform.format(exp), "0-3+(0-2-6/1*4)")
        exp = "+3+2-6/1*4"
        self.assertEqual(self.transform.format(exp), "0+3+2-6/1*4")
        exp = "+3+(+2-6/1*4)"
        self.assertEqual(self.transform.format(exp), "0+3+(0+2-6/1*4)")

    def testIsNum(self):
        num = "1"
        self.assertTrue(self.transform.isnum(num))
        num = "a"
        self.assertFalse(self.transform.isnum(num))

    def testIsOp(self):
        for op in ['+', '-', '*', '/', '(', ')']:
            self.assertTrue(self.transform.isop(op))
        op = "123"
        self.assertFalse(self.transform.isop(op))

    def testGetLevel(self):
        for e in ['+', '-']:
            self.assertEqual(self.transform.getlevel(e), 1)
        for e in ['*', '/']:
            self.assertEqual(self.transform.getlevel(e), 2)
        for e in ['(', ')']:
            self.assertEqual(self.transform.getlevel(e), 3)
        e = "123"
        self.assertEqual(self.transform.getlevel(e), None)

    def testCompare(self):
        self.transform.get_level = MagicMock()
        self.transform.compare(2, 1)
        self.assertTrue(self.transform.get_level.is_called)

    def testOrStack(self):
        self.transform.or_stack("1")
        self.assertEqual(self.transform.orstack, ["1"])
        self.transform.or_stack("(")
        self.assertEqual(self.transform.orstack, ["1", "("])
        self.transform.or_stack("2")
        self.assertEqual(self.transform.orstack, ["1", "(", "2"])
        self.transform.or_stack(")")
        self.assertEqual(self.transform.orstack, ["1"])
        self.assertEqual(self.transform.odlist, ["2"])
        self.transform.or_stack("+")
        self.assertEqual(self.transform.orstack, ["1", "+"])
        self.transform.or_stack("3")
        self.assertEqual(self.transform.orstack, ["1", "3"])
        self.assertEqual(self.transform.odlist, ["2", "+"])

    def testIfToPf(self):
        self.transform.format = MagicMock()
        self.transform.isnum = MagicMock()
        self.transform.isop = MagicMock()
        exp = "3+2-5*0"
        self.transform.format.return_value = exp
        self.transform.isnum.return_value = True
        self.transform.isop.return_value = False
        self.assertEqual(self.transform.iftopf(exp), "3+2-5*0")
        self.transform.odlist = []
        self.transform.orstack = []
        self.transform.isnum.return_value = False
        self.transform.isop.return_value = True
        self.transform.or_stack = MagicMock()
        self.assertEqual(self.transform.iftopf(exp), "")
        self.assertTrue(self.transform.or_stack.is_called)

if __name__ == "__main__":
    unittest.main()
