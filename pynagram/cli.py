#!/usr/bin/env python
import sys
import click

from pynagram.pynagram import *
from pynagram import numpad_kb
# from pynagram.util import write
from pynagram.util import minimax


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
    min_len, max_len = minimax(min_len, max_len, len(anagram))

    # click.echo(f"main({min_len}, {max_len}, {word_list}, {anagram})")

    dictionary = load_dict(word_list, min_len, max_len) if word_list else None
    anagrams = sorted(get_anagrams(anagram, dictionary, min_len, max_len),
                      key=lambda s: (len(s), s))
    for s in anagrams:
        click.echo(s)
    return 0


@cli.command()
@click.option('-m', '--min-len', type=int, default=None,
              help='minimum word length')
@click.option('-x', '--max-len', type=int, default=None,
              help='maximum word length')
@click.option('-d', '--word-list', type=click.Path(exists=True), default=None,
              help='dictionary file')
@click.option('-p', '--pred', is_flag=True, default=False,
              help='enable predictive text')
@click.option('-s', '--sep', default='\n',
              help='Sentence separator')
@click.argument('seq')
def numpad(pred, word_list, min_len, max_len, sep, seq):
    if pred and len(seq) > 10:
        click.echo("Input sequence is too long")
        return 1
    min_len, max_len = minimax(min_len, max_len, len(seq))
    dictionary = load_dict(word_list, min_len, max_len) if word_list else None
    ws = numpad_kb.proc(seq, pred, dictionary)
    click.echo(sep.join(ws))


if __name__ == "__main__":
    sys.exit(cli())
