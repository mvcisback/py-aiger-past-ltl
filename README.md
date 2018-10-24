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
