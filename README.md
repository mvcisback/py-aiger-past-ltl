# py-aiger-past-ltl

Library for generating (p)ast (t)ense (l)inear (t)emporal (l)ogic
monitors as aiger circuits. Builds on the [py-aiger](https://github.com/mvcisback/py-aiger) project.

[![Build Status](https://cloud.drone.io/api/badges/mvcisback/py-aiger-past-ltl/status.svg)](https://cloud.drone.io/mvcisback/py-aiger-past-ltl)
[![codecov](https://codecov.io/gh/mvcisback/py-aiger-past-ltl/branch/master/graph/badge.svg)](https://codecov.io/gh/mvcisback/py-aiger-past-ltl)
[![PyPI version](https://badge.fury.io/py/py-aiger-ptltl.svg)](https://badge.fury.io/py/py-aiger-ptltl)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Installation

If you just need to use `aiger_ptltl`, you can just run:

`$ pip install py-aiger-ptltl`

For developers, note that this project uses the
[poetry](https://poetry.eustace.io/) python package/dependency
management tool. Please familarize yourself with it and then
run:

`$ poetry install`

# Usage

`aiger_ptltl` has two complementary API's. The first, called the
Parser API, implements a small domain specific language for specifying
past tense temporal logic monitors. The second api, called the
Function API, is an embededded domain specific language centered
around `aiger_ptltl.PTLTLExpr` objects. 

We start by importing the `aiger_ptltl` module.

```python
import aiger_ptltl as ptltl
```

## Parser API

The Parser API centers around the `parse` function.

It supports simple propositional logic, `TRUE, FALSE, ~ _, (_ & _), (_
| _), (_ -> _)`, as well as four temporal operators, `H _, P _, Z _, [_ S _]`, which denote historically, past (once), weak yesterday, and since.


Atomic propositions can be created as any alphanumeric string starting
with a letter. For example 'a' and 'Fo000bar1' are allowed while
'1asd' and 'foo_bar' are disallowed as names for atom propositions.

```python

print(ptltl.parse('H ((a & P b) -> [~b S c])'))
```
