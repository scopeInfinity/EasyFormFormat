import unittest

import ui

class TestUI(unittest.TestCase):

    def test_singleton(self):
        obj1 = ui.UI.getInstance()
        obj2 = ui.UI.getInstance()
        self.assertEqual(id(obj1), id(obj2))

        with self.assertRaises(AttributeError):
            ui.UI()


if __name__ == '__main__':
    unittest.main()