#!/usr/bin/env python
""" Test for nokaut_api"""
import os
import sys
import unittest
sys.path.append(os.path.abspath('../'))
from lib.nokaut_api import nokaut_api, poss_parameters, main


class NokautTest(unittest.TestCase):
    """Class for testing nokaut_api"""
    def test_nokaut_key_true(self):
        """Test if nokaut_api is giving good resoults"""
        tests = [
            ('macbook', 'a8839b1180ea00fa1cf7c6b74ca01bb5'),
            ('canon450', 'a8839b1180ea00fa1cf7c6b74ca01bb5'),
            ('wiedzmin', 'a8839b1180ea00fa1cf7c6b74ca01bb5'),
        ]
        for name, key in tests:
            resoult = nokaut_api(name, key)
            self.assertTrue(bool(resoult))

    def test_nokaut_key_false(self):
        """Check if nokaut_api gives Flase when are bad dates"""
        tests = [
            ('macbook', 'a8839b1180ea0fa1cf7c6b74ca01bb'),
            ('canon450', 'a8839b1180ea00fa1c7c6b74ca01bb'),
            ('toshiba', '8839b1180ea00fa1cf7c6b74ca01bb'),
        ]
        for name, key in tests:
            self.assertFalse(nokaut_api(name, key))

    def test_nokaut_possition_true(self):
        """Testing if it gives good output"""
        sys.argv[1:] = ["-h"]
        self.assertTrue(bool(main()))
        sys.argv[1:] = [
            "--name", "macbook", "--key", 'a8839b1180ea00fa1cf7c6b74ca01bb5'
        ]
        self.assertTrue((bool(poss_parameters())))
        self.assertTrue((bool(main())))

    def test_nokaut_possition_false(self):
        """Testing unknown options"""
        sys.argv[1:] = ["--csad"]
        self.assertTrue(bool(main()))


if __name__ == '__main__':
    unittest.main()
