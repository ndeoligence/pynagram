from itertools import permutations
from functools import reduce, partial
import re


def load_dict(filename, mn=None, mx=None):
    """Loads words from a dictionary (word list)
    filename: the path to the word list - mandatory
    mn: minimum length of words to be imported
    mx: the maximum length of imported words
    """
    if mn is None:
        mn = 1
    words = []
    with open(filename) as f:
        words += f.read().split('\n')
    words_list = [s for s in words if (not mx and mn <= len(s) or mn <= len(s) <= mx)]
    # print(f'[debug] <load_dict> Word list size = {len(words_list)}')
    return words_list


def find_valid_words(word_list, candidates):
    """Finds valid words from 'candidates' as found in
    the given wordlist.
    wordlist: the list to be used as a dictionary. Only words in the dictionary are considered valid words
    candidates: strings to be tested for validity
    """
    dictionary, perms = set(word_list), set(candidates)
    return dictionary & perms


def get_anagrams(s, dictionary, mn, mx):
    """Generates all anagrams of the string s using the provided dictionary,
    whose lengths are >= mn and <= mx.

    Thus the function returns all w such that w is in dictionary
    and mn <= len(w) <= mx.

    If no dictionary is given, then a list of permuted strings will be returned

    s: the string to be used to generate anagrams
    dictionary: the dictionary to be used to determine valid words
    mn: the minimum length of words to be returned
    mx: the maximum length of words to be returned
    """
    if not s:
        return set()

    s = re.sub(r'\s+', '', s.lower())
    # strings = set()
    # for i in range(mn, mx + 1):
    #     strings |= {''.join(e) for e in permutations(s, i)}
    strings = {''.join(e) for e in reduce(lambda acc, xs: acc | set(xs),
                                          map(partial(permutations, s), range(mn, mx + 1)), set())}
    if not dictionary:
        return strings
    return find_valid_words(dictionary, strings)
