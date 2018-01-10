import unittest
import re
import os
from app import load_dict, get_anagrams


class AppTest(unittest.TestCase):
    def setUp(self):
        self.filename = 'dict.dat'
        self.words = [
            'matthew', 'mark', 'luke', 'john', 'timothy', 'titus', 'philemon', 'james', 'peter', 'jude'
        ]
        f = open(self.filename, 'w')
        for s in self.words:
            f.write(f'{s}\n')
        f.close()
        with open(self.filename, 'r') as f:
            self.assertSetEqual({s for s in re.split(r'\n', f.read()) if len(s) > 0}, set(self.words))

    def test_dict_load(self):
        self.assertListEqual(self.words, load_dict(self.filename))

    def test_dict_min(self):
        self.assertListEqual([w for w in self.words if len(w) >= 5], load_dict(self.filename, 5))

    def test_dict_max(self):
        self.assertListEqual([w for w in self.words if len(w) <= 4], load_dict(self.filename, None, 4))

    def test_dict_min_max(self):
        self.assertListEqual([w for w in self.words if (5 <= len(w) <= 6)], load_dict(self.filename, 5, 6))

    def test_get_anagrams(self):
        self.assertIn('matthew', get_anagrams('wehtamt', self.words, 6, 7))

    def tearDown(self):
        os.remove(self.filename)


if __name__ == '__main__':
    unittest.main()
