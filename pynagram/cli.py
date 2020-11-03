#!/usr/bin/env python
import sys
import click

from pynagram.pynagram import *
# from pynagram.util import write


@click.group()
def cli():
    pass


@cli.command()
@click.option('-d', '--word-list', type=click.Path(exists=True), required=True,
              help='dictionary file')
@click.argument('anagram')
@click.option('-m', '--min-len', type=int, default=None,
              help='minimum word length')
@click.option('-x', '--max-len', type=int, default=None,
              help='maximum word length')
@click.option('-s', '--sep', default='\n',
              help='specify a sentence separator')
def sentence(min_len, max_len, word_list, sep, anagram):
    """
    Try to make a sentence out of the given anagram.
    """
    dictionary = load_dict(word_list, min_len, max_len) if word_list else None
    lines = construct_sentences(anagram, dictionary)
    # write('sentences.txt', '\n'.join(lines))
    # click.echo(f"Sentences: {sep.join(lines)}")
    click.echo(sep.join(lines))


@cli.command()
@click.option('-m', '--min-len', type=int, default=None,
              help='minimum word length')
@click.option('-x', '--max-len', type=int, default=None,
              help='maximum word length')
@click.option('-d', '--word-list', type=click.Path(exists=True), default=None,
              help='dictionary file')
@click.argument('anagram')
def words(min_len, max_len, word_list, anagram):
    """Creates words that are anagrams of the given input"""
    # click.echo(f"main({min_len}, {max_len}, {word_list}, {anagram})")
    if not max_len:
        max_len = len(anagram)
    if not min_len:
        min_len = 1
    elif min_len < 0:
        min_len = max_len
    else:
        min_len = min(min_len, max_len)

    # click.echo(f"main({min_len}, {max_len}, {word_list}, {anagram})")

    dictionary = load_dict(word_list, min_len, max_len) if word_list else None
    anagrams = sorted(get_anagrams(anagram, dictionary, min_len, max_len),
                      key=lambda s: (len(s), s))
    for s in anagrams:
        click.echo(s)
    return 0


if __name__ == "__main__":
    sys.exit(cli())
