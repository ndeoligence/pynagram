#!/usr/bin/env python
from itertools import combinations, permutations
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


def load_dict(filename, mn=None, mx=None):
    if mn is None:
        mn = 1
    words = []
    with open(filename) as f:
        words += f.read().split('\n')
    wordlist = [s for s in words if (len(s)>=mn and (not mx or len(s) <= mx))]
    # print(f'[debug] <load_dict> Word list size = {len(wordlist)}')
    return wordlist


def find_valid_words(wordlist, candidates):
    dictionary, perms = set(wordlist), set(candidates)
    return dictionary & perms


def get_anagrams(s, dictionary, mn, mx):
    strings = []
    for i in range(mn, mx+1):
        strings += [''.join(e) for e in permutations(s, i)]
    if dictionary is None:
        return strings
    return find_valid_words(dictionary, strings)


def main():
    args = get_args()
    min_len = 1 if not args.min else args.min
    max_len = args.max
    if not max_len or max_len > len(args.anagram):
        max_len = len(args.anagram)
    dictionary = load_dict(args.dict, min_len, max_len) if args.dict else None

    # size = 0
    for s in sorted(get_anagrams(args.anagram, dictionary, min_len, max_len), key=lambda s: (len(s), s)):
        # if size != len(s):
            # size = len(s)
            # print(f'[debug] <main>* * {size} * *')
        print(s)


if __name__ == '__main__':
    main()
