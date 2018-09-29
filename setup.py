from setuptools import find_packages, setup

setup(
    name='py-aiger-pltl',
    version='0.1',
    description='TODO',
    url='https://github.com/mvcisback/py-aiger-past-ltl',
    author='Marcell Vazquez-Chanlatte',
    author_email='marcell.vc@eecs.berkeley.edu',
    license='MIT',
    install_requires=[
        'parsimonious',
        'funcy',
        'py-aiger',
        'lenses',
        'hypothesis',
    ],
    packages=find_packages(),
)
