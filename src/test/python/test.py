import unittest

def add(x,y):
    return x + y

class MyTest(unittest.TestCase):
    def test(self):
        self.assertEqual(add(3,4), 7)

if __name__ == '__main__':
    unittest.main()
