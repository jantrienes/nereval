from distutils.core import setup

setup(
    name='muceval',
    version='0.2.2',
    description='MUC-like evaluation script for named entity recognition systems.',
    license='MIT',
    py_modules=['muceval'],
    tests_require=[
        'pytest',
        'pytest-cov',
    ]
)
