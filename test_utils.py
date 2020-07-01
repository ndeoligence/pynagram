#!/usr/bin/env python
import unittest
from utils import get_anagrams


def sort_list(items):
    return sorted(items, key=lambda x: (len(x), x))


class AppTest(unittest.TestCase):

    def setUp(self):
        self.filename = 'dict.dat'
        self.words = [
            'matthew', 'mark', 'luke', 'john', 'timothy', 'titus', 'philemon', 'james', 'peter', 'jude'
        ]

    def test_get_anagrams(self):
        self.assertIn('matthew', get_anagrams('wehtamt', self.words, 6, 7))

    def test_get_anagrams_empty(self):
        self.assertListEqual(list(), sort_list(list(get_anagrams(None, self.words, 6, 7))))
        self.assertListEqual(list(), sort_list(list(get_anagrams('', self.words, 6, 7))))

    def test_get_anagrams_no_dict(self):
        self.assertListEqual([
            'a', 'b', 'c',
            'ab', 'ac', 'ba', 'bc', 'ca', 'cb',
            'abc', 'acb', 'bac', 'bca', 'cab', 'cba'
        ], sort_list(list(get_anagrams('abc', None, 1, 3))))


if __name__ == '__main__':
    unittest.main()
