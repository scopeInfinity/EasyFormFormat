import unittest
from unittest import mock

import ui


class TestUI(unittest.TestCase):

    def setUp(self):
        # modifying a private mangled attribute to reset singleton
        ui.UI._UI__instance = None
        self.mock_tk_patch = mock.patch("tkinter.Tk", autospec=True)
        self.mock_tk = self.mock_tk_patch.start()
        self.mock_tk_instance = self.mock_tk.return_value

    def tearDown(self):
        self.mock_tk_patch.stop()

    def test_singleton(self):
        obj1 = ui.UI.getInstance()
        obj2 = ui.UI.getInstance()
        self.assertEqual(id(obj1), id(obj2))
        self.mock_tk.assert_called_once_with()

    def test_constructor_exception(self):
        with self.assertRaises(AttributeError):
            ui.UI()
        self.mock_tk.assert_not_called()

    @mock.patch("tkinter.Button")
    def test_start(self, fake_button):
        obj = ui.UI.getInstance()
        obj.start()
        self.mock_tk.assert_called_once_with()
        self.mock_tk_instance.mainloop.assert_called_once_with()

    @mock.patch("tkinter.Button")
    def test_draw_buttons(self, fake_button):
        obj = ui.UI.getInstance()
        obj.draw()
        self.mock_tk.assert_called_once_with()
        fake_button.assert_called_once_with(self.mock_tk_instance, text='Open File', command=obj.handler.open_file)


if __name__ == '__main__':
    unittest.main()