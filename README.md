# py-aiger-past-ltl

Library for generating (p)ast (t)ense (l)inear (t)emporal (l)ogic
monitors as aiger circuits. Builds on the [py-aiger](https://github.com/mvcisback/py-aiger) project.

[![Build Status](https://cloud.drone.io/api/badges/mvcisback/py-aiger-past-ltl/status.svg)](https://cloud.drone.io/mvcisback/py-aiger-past-ltl)
[![codecov](https://codecov.io/gh/mvcisback/py-aiger-past-ltl/branch/master/graph/badge.svg)](https://codecov.io/gh/mvcisback/py-aiger-past-ltl)
[![PyPI version](https://badge.fury.io/py/py-aiger-ptltl.svg)](https://badge.fury.io/py/py-aiger-ptltl)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-generate-toc again -->
**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)

<!-- markdown-toc end -->


# Installation

If you just need to use `aiger_ptltl`, you can just run:

`$ pip install py-aiger-ptltl`

For developers, note that this project uses the
[poetry](https://poetry.eustace.io/) python package/dependency
management tool. Please familarize yourself with it and then
run:

`$ poetry install`

# Usage

The primary entry point for using `aiger_ptltl` is the `PTLTLExpr`
class which is a simple extension of `aiger.BoolExpr` to support the
temporal operators, historically, past (once), (variant) yesterday,
and since.

```python
import aiger_ptltl as ptltl

# Atomic Propositions
x = ptltl.atom('x')
y = ptltl.atom('y')
z = ptltl.atom('z')

# Propositional logic
expr1 = ~x
expr2 = x & (y | z)
expr3 = (x & y) | ~z
expr4 = ~(x & y & z)

# Temporal Logic
expr5 = x.historically()  #  (H x) ≡ x has held for all previous cycles (inclusive).
expr6 = x.once()  #  (P x) ≡ x once held in a past cycle (inclusive).
expr7 = x.vyest()  #  (Z x) ≡ x held in the previous cycle (true at time = 0).
expr8 = x.since(y)  #  [x S y] ≡ x has held since the cycle after y last held.

# Composition
expr9 = expr7.since(expr8.vyest().vyest())
```
