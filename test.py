# from ER_apis.test import *
# from ER_datas.test import *
import unittest

class TestForeignTeam(unittest.TestCase):
    def test_true(self):
        self.assertEqual(1,1)
    def test_fail(self):
        self.assertEqual("change",2)

if __name__ == "__main__":
    unittest.main()
