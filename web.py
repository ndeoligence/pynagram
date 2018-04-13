#!/usr/bin/env python
from flask import Flask, render_template, request
import logging as log
from utils import *

log.basicConfig(level=log.DEBUG)

log.debug("Caching word list: crosswd.txt")
dictionary = load_dict('crosswd.txt')
log.debug(f"Loaded {len(dictionary)} words.")


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/anagram', methods=['POST'])
def anagram():
    string = request.form.get('input')
    log.info(f"input = [{string}]")
    string_len = len(string)
    anagrams = sorted(get_anagrams(string, dictionary, 1, string_len), key=lambda w: (len(w), w))
    log.debug(f"Anagram [{string}] has {len(anagrams)} anagrams")
    return render_template('anagram.html', **{'words':anagrams, 'string': string})


app.run(host='localhost', port=8000, debug=True)
