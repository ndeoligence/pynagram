#!/usr/bin/env python
from itertools import combinations, permutations
import argparse
from utils import *


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


def main():
    args = get_args()
    min_len = 1 if not args.min else args.min
    max_len = args.max
    if not max_len or max_len > len(args.anagram):
        max_len = len(args.anagram)
    dictionary = load_dict(args.dict, min_len, max_len) if args.dict else None

    anagrams = sorted(get_anagrams(args.anagram, dictionary, min_len, max_len), key=lambda s: (len(s), s))
    for s in anagrams:
        print(s)


if __name__ == '__main__':
    main()
