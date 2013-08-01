# Thanks
#  http://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/

from setuptools import setup

setup(
    name = 'ConjugationScraper',
    version = '0.1',
    packages = ['scraper'],
    package_data = {
        '': ['*.txt'],
    },
    install_requires = [
        'beautifulsoup4'
    ],
    
    author = 'Greg Schafer',
    author_email = 'grschafer@gmail.com',
    description = 'Scrapes Spanish verb conjugations from conjugation.org',
    license = 'MIT',
    url = 'https://github.com/grschafer/cohete_conjugador',
    classifiers = [
        'Private :: Do Not Upload'
    ],

)
