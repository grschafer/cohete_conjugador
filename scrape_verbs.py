#!/usr/bin/python

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

def extract_conjugations(html):
    soup = BeautifulSoup(html)
    conj_dict = {}
    for cell in soup.find_all('td'):
        if cell.contents != []:
            gen = cell.stripped_strings
            tense = gen.next().strip(':')
            conj_dict[tense] = [conj for conj in gen]
    return conj_dict

def conjugations_for_word(word):
    data = '%s&word=%s' % (req_data, word)
    resp = None
    try:
        resp = urlopen('http://www.conjugation.org/cgi-bin/conj.php', data)
        html = resp.read()
        print 'word %s had response of length %d' % (word, len(html))
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
    

# TODO: output to a file for parsing by actionscript... (json?)
def main():
    assert len(sys.argv) == 2, "Expects 1 argument (file of verbs to conjugate)"
    words = get_word_list(sys.argv[1])
    conjs = conjugations_for_words(words)
    import json
    #print json.dumps(conjs)
    from pprint import pprint
    pprint(conjs)
    


if __name__ == '__main__':
    main()
