from itertools import permutations
from functools import reduce, partial
import re
from typing import Collection


def find_valid_words(dictionary: Collection[str], candidates: Collection[str]) -> Collection[str]:
    """Finds valid words from 'candidates' as found in
    the given words list.
    dictionary: the list to be used as a dictionary. Only strings in the dictionary are considered valid words
    candidates: strings to be tested for validity
    """
    dictionary, perms = set(dictionary), set(candidates)
    return dictionary & perms


def get_anagrams(string: str, dictionary: Collection[str], mn: int, mx: int) -> Collection[str]:
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
    if not string:
        return set()
    if not mx:
        mx = len(string)
    if not mn:
        mn = mx

    string = re.sub(r'\s+', '', string.lower())
    strings = {''.join(e) for e in reduce(lambda acc, xs: acc | set(xs),
                                          map(partial(permutations, string), range(mn, mx + 1)), set())}
    if not dictionary:
        return strings
    return find_valid_words(dictionary, strings)
