#!/usr/bin/env python
from flask import Flask, render_template, request, Response
import logging as log
import json

MAX_INPUT_LEN = 10

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


@app.route(r'/api/<instr>')
def api(instr):
    log.info(f"input = [{instr}]")
    instr_len = len(instr)
    if (instr_len > MAX_INPUT_LEN):
        return Response(json.dumps({'string': instr, 'anagrams': [],
            'error': f'Input string too long. Max length allowed = {MAX_INPUT_LEN}'}),
            status=200, mimetype='application/json')
    anagrams = sorted(get_anagrams(instr, dictionary, 1, instr_len), key=lambda w: (len(w), w))
    log.debug(f"Anagram [{instr}] has {len(anagrams)} anagrams")
    response = Response(json.dumps({'string': instr, 'anagrams': anagrams}), status=200, mimetype='application/json')
    return response


if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)
