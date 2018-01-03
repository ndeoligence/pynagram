#!/home/monde/anaconda3/envs/py36/bin/python
import sys
from my_text_utils import permute
from itertools import combinations
import argparse


def get_args():
    """Initializes the arguments we want from the user.
    Returns the parsed arguments."""
    parser = argparse.ArgumentParser(description='Creates words that are anagrams of the given input')
    parser.add_argument('anagram', help='the anagram to use', type=str)
    parser.add_argument('-m', '--min', help='minimum word length', type=int)
    parser.add_argument('-x', '--max', help='maximum word length', type=int)
    parser.add_argument('-d', '--dict', help='dictionary file name', type=str) # a positional argument.
    # parser.add_argument('-o', '--outfile', help='print output to this file instead of stdout', type=str) # an optional argument
    return parser.parse_args()


def load_dict(filename, min=None, max=None):
    if min is None:
        min = 1
    words = []
    with open(filename) as f:
        words += f.read().split('\n')
    # print(f'Word list size = {len(wordlist)}')
    return [s for s in words if (len(s)>=min and (not max or len(s) <= max))]


def find_valid_words(wordlist, candidates):
    dictionary, perms = set(wordlist), set(candidates)
    return dictionary & perms


def to_sorted_strings(rows):
    """Transforms a list of lists of chars
    into a list of words. So the inner lists of chars get transformed to strings.
    """
    return sorted([''.join(r) for r in rows])


def get_anagrams(s, dictionary=None):
    strings = to_sorted_strings(permute(list(s)))
    if dictionary is None:
        return strings
    return find_valid_words(dictionary, strings)


def main():
    args = get_args()
    min_len = 1 if not args.min else args.min
    max_len = args.max
    dictionary = load_dict(args.dict, min_len, max_len) if args.dict else None
    if not max_len:
        max_len = max(dictionary, key=len)

    for s in get_anagrams(args.anagram, dictionary):
        print(s)


if __name__ == '__main__':
    main()
