import unittest
from unittest.mock import patch

from src.console.console_interface import play_console_type

arr1 = ['Y']
for i in range(10):
    for j in range(1, 11):
        arr1.append(chr(i + ord('A')) + str(j))
arr2 = ['N', 'A11', '123', '1', "54366"]
for i in range(10):
    for j in range(1, 11):
        arr2.append(chr(i + ord('A')) + str(j))
arr1.append('exit')
arr2.append('exit')


class TestYourFunction(unittest.TestCase):
    @patch('builtins.input', side_effect=arr1)
    def test_your_function_1(self, mock_input):
        play_console_type()
        self.assertTrue(mock_input.called)
