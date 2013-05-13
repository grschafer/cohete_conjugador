#!/usr/bin/python

from collections import defaultdict
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
    conj_dict = defaultdict(list)
    for cell in soup.find_all('td'):
        if cell.contents != []:
            gen = cell.stripped_strings
            tense = gen.next().strip(':')
            for line in gen:
                conj_dict[tense].append(line)
    return conj_dict

def conjugations_for_word(word):
    data = '%s&word=%s' % (req_data, word)
    print data
    try:
        resp = urlopen('http://www.conjugation.org/cgi-bin/conj.php', data)
        html = resp.read()
        print 'word %s had response of length %d' % (word, len(html))
        conj_dict = extract_conjugations(html)
        return conj_dict
    finally:
        if resp: resp.close()

def main():
    conj_dict = conjugations_for_word('estar')
    print conj_dict
    


if __name__ == '__main__':
    main()
