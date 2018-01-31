import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='nereval',
    version='0.2.3',
    author='Jan Trienes',
    author_email='jan.trienes@googlemail.com',
    url='https://github.com/jantrienes/nereval',
    description='Evaluation script for named entity recognition systems based on F1 score.',
    long_description=read('README.rst'),
    keywords=['ner', 'nlp', 'evaluation', 'f1_score', 'f1', 'linguistics', 'machine_learning'],
    license='MIT',
    py_modules=['nereval'],
    tests_require=[
        'pytest',
        'pytest-cov',
    ]
)
