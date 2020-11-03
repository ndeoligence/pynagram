from typing import Collection, List, Tuple
from string import digits

from pynagram.pynagram import find_valid_words, load_dict
# from pynagram.util import log

NUM_PAD = {
    0: ' ',
    1: '.', 2: 'abc', 3: 'def',
    4: 'ghi', 5: 'jkl', 6: 'mno',
    7: 'pqrs', 8: 'tuv', 9: 'wxyz',
}


def fn(code: int, n: int) -> str:
    """
    Converts an encoded key-press into a character.
    Uses modulus operator to make n numbers wrap-around

    eg, fn (7, 3) -> 'r'
    """
    if code in (0, 1):
        return NUM_PAD[code] * n
    xs = NUM_PAD[code]
    return xs[(n - 1) % len(xs)]


def type_seq(instr: Collection[Tuple[int, int]]) -> str:
    """
    Converts a sequence of number presses into actual characters.
    eg, fn [(8,2), (7,4)] -> 'us'
    """
    return ''.join([fn(c, n) for c, n in instr])


def _word_cons(ws: List[str]) -> Collection[str]:
    if not ws:
        return []
    elif len(ws) == 1:
        return list(ws[0])

    ys = []
    tails = _word_cons(ws[1:])
    for k in ws[0]:
        for w in tails:
            ys.append(k + w)
    return ys


# @log
def word_cons(ws: List[str]) -> Collection[str]:
    """
    eg, fn ['mno', 'tuv', 'pqrs', 'pqrs'] -> ['mtpp', 'mtpq', 'mtpr', ..., 'ovss']
    """
    return _word_cons(ws)


# @log
def dict_options(ins: str) -> List[str]:
    """
    Converts a key-press into possible characters
    eg: fn '6877' -> ['mno', 'tuv', 'pqrs', 'pqrs']
    """
    return [NUM_PAD[int(c)] for c in ins]


def parse(nums: str) -> Collection[Tuple[int, int]]:
    """
    Input: a sequence of numbers
    Output: A collection of tuples (x,n) | x was pressed n times, n > 0 & len(xs) <= len(nums)
    eg, fn '66688777' -> [(6,3), (8,2), (7,3)]
    """
    prev = None
    xs = []
    for num in nums:
        cur = digits.index(num)
        if cur == prev:
            _, count = xs.pop()
            xs.append((cur, count + 1))
        else:
            xs.append((cur, 1))
        prev = cur
    return xs


def proc(ins: str, atc: bool, word_list: Collection[str] = None) -> Collection[str]:
    # print(f"proc: ins='{ins}', atc='{atc}'")
    if atc:
        if '0' in ins:
            ins = ins.split('0')[0]
        opts = dict_options(ins)
        # print(f"opts.len = {len(opts)}")
        # if len(opts) > 0: print(f"opts#1 = {opts[0]}")
        ws = word_cons(opts)
        # print(f"word-cons.len = {len(ws)}")
        # if len(ws) > 0: print(f"opt-cons#1 = {ws[0]}")
        valid_words = find_valid_words(word_list, ws)
        # print(f"valid-words.len = {len(valid_words)}")
        return valid_words
    else:
        codes = parse(ins)
        return [type_seq(codes)]


def main():
    invals = '84732804703837994373'.split('0')
    for inval in invals:
        print('\n'.join(proc(inval, True, load_dict)))


if __name__ == '__main__':
    main()
