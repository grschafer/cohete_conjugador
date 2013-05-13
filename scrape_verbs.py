#!/usr/bin/python

from itertools import izip_longest
from urllib2 import urlopen
from bs4 import BeautifulSoup
import re

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
scrape_regex = re.compile(r'Present\s+Indicative:\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)Imperfect:\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)Preterite:\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)Future:\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)Conditional:\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)Imperative:\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)Present Subjunctive:\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)Imperfect Subjunctive:\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)')
regex2 = re.compile(r'(?:([A-Z].*?):\s+((?:[^A-Z]+\s*)+))+$', flags=re.UNICODE | re.MULTILINE)

soup = None

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

def extract_conjugations(html):
    global soup
    soup = BeautifulSoup(html)
    text = soup.get_text()
    #result = scrape_regex.search(text)
    result = regex2.search(text)
    conjs = result.groups()
    print conjs
    grouped_conjs = list(grouper(conjs, 6))
    print grouped_conjs
    


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
    


if __name__ == '__main__':
    main()
