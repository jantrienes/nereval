from distutils.core import setup

setup(
    name='nereval',
    version='0.2.2',
    description='Evaluation script for named entity recognition systems based on F1 score.',
    license='MIT',
    py_modules=['nereval'],
    tests_require=[
        'pytest',
        'pytest-cov',
    ]
)
