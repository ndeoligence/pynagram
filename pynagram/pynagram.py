from itertools import permutations
from functools import reduce, partial
import re
from typing import Collection, Tuple

from pynagram.util import WordList, log

_word_list = None


def find_valid_words(dictionary: Collection[str], candidates: Collection[str]) -> Collection[str]:
    """Finds valid words from 'candidates' as found in
    the given words list.
    dictionary: the list to be used as a dictionary. Only strings in the dictionary are considered valid words
    candidates: strings to be tested for validity
    """
    dictionary, perms = set(dictionary), set(candidates)
    return dictionary & perms


def _remove_chars(string, chars):
    for k in chars:
        string = string.replace(k, '', 1)
    return string


# @log
def _const_sentences(string: str, words_list: Collection[str]) -> Tuple[bool, Collection[str]]:
    if not string:
        return True, []
    words = sorted(get_anagrams(string, words_list, 1, len(string)), key=lambda s: (len(s), s))
    # click.secho(f"words = {words}", fg='green')
    if len(words) == 0:
        return False, []

    acc = []
    for w in words:
        flag, tails = _const_sentences(_remove_chars(string, w), words_list)
        if flag:
            acc += [f"{w} {tail}" for tail in tails] if tails else [w]

    return len(acc) > 0, acc


# @log
# @timed
def construct_sentences(string: str, words_list: Collection[str]) -> Collection[str]:
    if not words_list:
        raise ValueError('Word list required for creating sentences')
    _, sentences = _const_sentences(string, words_list)
    return sentences


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


# @log
def load_dict(filename, mn=None, mx=None):
    """
    Loads words from a dictionary (word list)
    filename: the path to the word list - mandatory
    mn: minimum length of words to be imported
    mx: the maximum length of imported words
    """
    global _word_list
    if not _word_list:
        if mn is None:
            mn = 1
        words = []
        with open(filename) as f:
            words += f.read().split('\n')
        words_list = [s for s in words if (not mx and mn <= len(s)
                                           or mn <= len(s) <= mx)]
        # click.echo(f'[debug] <load_dict> Word list size = {len(words_list)}')
        _word_list = WordList(words_list)
    return _word_list


def is_word(string: str, words: Collection[str]) -> bool:
    return string in words
