from setuptools import find_packages, setup

DESC = 'Library for generating (p)ast (t)ense (l)inear (t)emporal
(l)ogic monitors as aiger circuits.'

setup(
    name='py-aiger-ptltl',
    version='0.0.0',
    description=DESC,
    url='https://github.com/mvcisback/py-aiger-past-ltl',
    author='Marcell Vazquez-Chanlatte',
    author_email='marcell.vc@eecs.berkeley.edu',
    license='MIT',
    install_requires=[
        'parsimonious',
        'funcy',
        'py-aiger',
        'lenses',
    ],
    packages=find_packages(),
)
