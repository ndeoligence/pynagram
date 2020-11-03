from functools import wraps
import time
from typing import List
import click


def is_iter(obj):
    try:
        return obj is not str and iter(obj)
    except TypeError:
        return False


def stringify(*args, **kwargs):
    mystr = lambda o: f"(len={len(o)}){str(o[:10] + (['...'] if len(o) > 10 else []))}" if isinstance(o, list) else str(o)
    xs = [mystr(e) for e in args] + [f"{k}={v}" for k, v in kwargs.items()]
    return ', '.join(xs)


def log(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        click.secho(f"[debug] {fn.__name__}({stringify(*args, **kwargs)})", fg='cyan')
        val = fn(*args, **kwargs)
        click.secho(f"[debug] {fn.__name__} -> {stringify(val)}", fg='green')
        return val

    return wrapper


def prettify(sec):
    sec = round(sec)
    hrs = sec // 3600
    sec %= 3600
    mins = sec // 60
    sec %= 60
    fmt = f"{hrs}h " if hrs else ''
    fmt += f"{mins}m " if mins else ''
    return f"{fmt}{sec}s"


def timed(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        startd = time.time()
        val = fn(*args, **kwargs)
        ttl = time.time() - startd
        click.secho(f"[debug] Runtime [{fn.__name__}({stringify(*args, **kwargs)})]: "
                    f"{round(ttl, 2)}s ({prettify(ttl)})", fg='magenta')
        return val

    return wrapper


def f2i(f, mx=10):
    return int(f * mx)


def sample_data(size: int = None) -> List:
    xs: List
    with open('nums.dat', 'r') as f:
        text = f.read()
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if size:
            lines = lines[:size]
    xs = [f2i(float(x.strip()), mx=len(lines)) for x in lines if x]
    return xs


def swap(xs: List, i: int, j: int) -> None:
    tmp = xs[i]
    xs[i] = xs[j]
    xs[j] = tmp


def write(path, contents):
    with open(path, 'w') as f:
        f.write(contents)


def minimax(min_len, max_len, upper_bound):
    if not max_len:
        max_len = upper_bound
    if not min_len:
        min_len = 1
    elif min_len < 0:
        min_len = max_len
    else:
        min_len = min(min_len, max_len)
    return min_len, max_len


class WordList(list):
    def __init__(self, *args, **kwargs):
        super(WordList, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "WordList(size={0:,})".format(len(self))
