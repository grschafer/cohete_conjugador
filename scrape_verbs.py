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

import sys
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
    'rb3': 'no',
    'rb2': 'ra'
}
req_data = '&'.join([x + '=' + y for x,y in params.iteritems()])
bad_words = {'oír': 'oir', 'reírse': 'reirse', 'sonreírse': 'sonreirse'}
# encodings from http://www.tutorialspoint.com/html/html_url_encoding.htm

def extract_conjugations(html):
    soup = BeautifulSoup(html)
    conj_dict = {}
    for cell in soup.find_all('td'):
        if cell.contents != []:
            gen = cell.stripped_strings
            tense = gen.next().strip(':').replace(' ', '') # remove spaces
            conj_dict[tense] = [conj for conj in gen]
    return conj_dict

def encode_accents(word):
    return word.replace('á', '%e1').replace('é', '%e9').replace('í', '%ed').replace('ó', '%f3').replace('ú', '%fa').replace('ü', '%fc').replace('ñ', '%f1')

def conjugations_for_word(word):
    # conjugation.org can't handle accented characters in request...
    req_word = fix_bad_words(word)
    req_word = encode_accents(req_word)
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
    conjs = {}
    for word in words:
        conjs[word] = conjugations_for_word(word)
    return conjs
    

def get_word_list(fin):
    words = []
    with open(fin, 'r') as f:
        # ignore empty and commented lines
        words = [line.strip() for line in f \
                 if len(line.strip()) > 2 and not line.startswith("//")]
    return words
    
# fix_bad_ functions correct errors caused by conjugation.org
def fix_bad_words(word):
    if word == 'oír': word = 'oir'
    if word == 'reírse': word = 'reirse'
    if word == 'sonreírse': word = 'sonreirse'
    return word
def fix_bad_conjugations(conj_dict):
    if 'cerrar' in conj_dict:
        conj_dict['cerrar']['PresentIndicative'] = [u'cierro',u'cierras',u'cierra',u'cerramos',u'cerráis',u'cierran']
        conj_dict['cerrar']['PresentSubjunctive'] = [u'cierre',u'cierres',u'cierre',u'cerremos',u'cerréis',u'cierren']
        conj_dict['cerrar']['Indicative'] = [u'cierra',u'cierre',u'cerremos',u'cerrad',u'cierren']
    return conj_dict

# TODO: output to a file for parsing by actionscript... (json?)
def main():
    assert len(sys.argv) == 2, "Expects 1 argument (file of verbs to conjugate)"
    words = get_word_list(sys.argv[1])
    conj_dict = conjugations_for_words(words)
    conj_dict = fix_bad_conjugations(conj_dict)
    #print conj_dict
    import json
    txt = json.dumps(conj_dict, sort_keys=True,
                     indent=4, separators=(',', ': '))
    print txt
    


if __name__ == '__main__':
    main()
