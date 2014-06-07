#!/usr/bin/env python
""" Test for nokaut_api"""
import os
import sys
import unittest
sys.path.append(os.path.abspath('../'))
from lib.allegro_api import (
    allegro_api,
    poss_parameters
)


class AllegroTest(unittest.TestCase):
    """Class for testing nokaut_api"""
    def test_allegro_api_true(self):
        """Test if nokaut_api is giving good resoults"""
        tests = ['macbook', 'canon450', 'toshiba']
        for name in tests:
            resoult = allegro_api(name)
            self.assertTrue(bool(resoult))

    def test_allegro_key_false(self):
        """Check if nokaut_api gives false when are bad dates"""
        tests = ['madscboosaadsdk', 'canodasdasdn4sadsa50', 'toshdasdaibddas']
        for name in tests:
            self.assertFalse(allegro_api(name))

    def test_allegro_possition_true(self):
        """Testing if it gives good output"""
        sys.argv[1:] = ["-h"]
        self.assertTrue(bool(poss_parameters()))
        sys.argv[1:] = ["--name", "macbook"]
        self.assertTrue((bool(poss_parameters())))

    def test_allegro_possition_false(self):
        """Testing unknown options"""
        sys.argv[1:] = ["--csad"]
        self.assertTrue(bool(poss_parameters()))


if __name__ == '__main__':
    unittest.main()
