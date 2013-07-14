#!/usr/bin/python
# -*- coding: utf-8 -*-

# Greg Schafer

"""
Accepts a text verb list as input on the command line
Fetches all conjugations for each verb from www.conjugation.org
Writes conjugations to output file

Note: Reflexive verbs don't include pronouns (e.g. afeitarse conjugates to
      'afeito' instead of 'me afeito')
"""

import sys # used for argv and stderr
import codecs # used to read utf8 file
import io # used to write windows line endings to output file
from urllib import urlencode
from urllib2 import urlopen
from bs4 import BeautifulSoup

params = {
    #'word': word,
    'B1': 'Conjugate',
    'rb1': 'table',
    'dpresent_indicative': 'yes',
    'dimperfect': 'yes',
    'dpreterite': 'yes',
    'dfuture': 'yes',
    'dconditional': 'yes',
    'dimperative': 'yes',
    'dp_sub': 'yes',
    'di_sub': 'yes',
    'dp_participle': 'yes',
    'rb3': 'yes',
    'rb2': 'ra'
}
# equivalent: req_data = '&'.join([x + '=' + y for x,y in params.iteritems()])
req_data = urlencode(params)

def extract_conjugations(html):
    soup = BeautifulSoup(html)
    conj_dict = {}
    for cell in soup.find_all('td'):
        if cell.contents != []:
            gen = cell.stripped_strings
            tense = gen.next().strip(':').replace(' ', '') # remove spaces
            if tense == 'PastParticiple':
                # conjugation.org puts yo/me pronouns in front of participle
                # sometimes for no good reason -- that's why split[-1]
                conj_dict[tense] = gen.next().split[-1]
            else:
                conj_dict[tense] = [' '.join(conj.split()[1:]) for conj in gen]
    return conj_dict

# encodings from http://www.tutorialspoint.com/html/html_url_encoding.htm
accent_map = {u'á':u'%e1', u'é':u'%e9', u'í':u'%ed', u'ó':u'%f3', u'ú':u'%fa', u'ü':u'%fc', u'ñ':u'%f1'}
def encode_accents(word):
    return ''.join(accent_map.get(x, x) for x in word)
accent_inv = {v:k for k,v in accent_map.items()}
def decode_accents(word):
    return ''.join(accent_inv.get(x, x) for x in word)

def conjugations_for_word(word):
    # conjugation.org can't handle accented characters in request...
    #req_word = fix_bad_words(word)
    #req_word = urllib.quote_plus(req_word) # throws UnicodeWarning =(
    req_word = encode_accents(word)
    data = '%s&word=%s' % (req_data, req_word)
    resp = None
    try:
        resp = urlopen('http://www.conjugation.org/cgi-bin/conj.php', data)
        html = resp.read()
        sys.stderr.write('word %s had response of length %d\n' % (word, len(html)))
        conj_dict = extract_conjugations(html)
        return conj_dict
    finally:
        if resp: resp.close()

def conjugations_for_words(words):
    return {word:conjugations_for_word(word) for word in words}

def get_word_list(fin):
    words = []
    with codecs.open(fin, 'r', 'utf8') as f:
        # ignore empty and commented lines
        words = [line.strip() for line in f \
                 if len(line.strip()) > 0 and not line.startswith("//")]
    return words
    
def add_definitions(conj_dict):
    from definitions import definitions
    for k,v in definitions.iteritems():
        if k in conj_dict:
            conj_dict[k]['def'] = v
    return conj_dict

# words where conjugation.org doesn't recognize the correct verb spelling
bad_words = {'oír': 'oir', 'reírse': 'reirse', 'sonreírse': 'sonreirse'}
# fix_bad_ functions correct errors caused by conjugation.org
def fix_bad_words(word):
    return bad_words.get(word, word)
def fix_bad_conjugations(conj_dict):
    if 'cerrar' in conj_dict:
        conj_dict['cerrar']['PresentIndicative'] = [u'cierro',u'cierras',u'cierra',u'cerramos',u'cerráis',u'cierran']
        conj_dict['cerrar']['PresentSubjunctive'] = [u'cierre',u'cierres',u'cierre',u'cerremos',u'cerréis',u'cierren']
        conj_dict['cerrar']['Imperative'] = [u'cierra',u'cierre',u'cerremos',u'cerrad',u'cierren']
    return conj_dict

def main():
    assert len(sys.argv) == 2, "Expects 1 argument (file of verbs to conjugate)"
    words = get_word_list(sys.argv[1])
    conj_dict = conjugations_for_words(words)
    conj_dict = fix_bad_conjugations(conj_dict)
    conj_dict = add_definitions(conj_dict)

    import json
    txt = json.dumps(conj_dict, sort_keys=True, ensure_ascii=False,
                     indent=4, separators=(',', ': '))
    #print txt
    with io.open('output', 'w', newline='\r\n') as f:
        f.write(txt)
    


if __name__ == '__main__':
    main()
