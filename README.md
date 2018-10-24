[![Build Status](https://travis-ci.org/mvcisback/py-aiger-past-ltl.svg?branch=master)](https://travis-ci.org/mvcisback/py-aiger-past-ltl)
[![codecov](https://codecov.io/gh/mvcisback/py-aiger-past-ltl/branch/master/graph/badge.svg)](https://codecov.io/gh/mvcisback/py-aiger-past-ltl)
[![Updates](https://pyup.io/repos/github/mvcisback/py-aiger-past-ltl/shield.svg)](https://pyup.io/repos/github/mvcisback/py-aiger-past-ltl/)
[![PyPI version](https://badge.fury.io/py/py-aiger-past-ltl.svg)](https://badge.fury.io/py/py-aiger-past-ltl)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# py-aiger-past-ltl


past-ltl -> aiger circuit library.

Builds on the [py-aiger](https://github.com/mvcisback/py-aiger) project.

# TODO
- [ ] Create Railroad diagram of grammar.
- [ ] Document features.

# Usage
```python
import aiger_ptltl as ptltl

print(ptltl.parse('H ((a & P b) -> [~b S c])'))
```
