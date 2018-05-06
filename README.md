# py-aiger-past-ltl
past-ltl -> aiger circuit library.

Builds on the [py-aiger](https://github.com/mvcisback/py-aiger) project.

# Usage
```python
In [1]: from aiger_pltl import parse

# a implies b
In [2]: parse("(a -> b)")
Out[2]: AAG(header=Header(max_var_index=5, num_inputs=2, num_latches=0, num_outputs=1, num_ands=1), inputs={'a': 2, 'b': 4}, outputs={'ec6ae198-5152-11e8-bc0d-7c7a919e7753': 11}, latches={}, gates=[[10, 2, 5]], comments=[''])

# a or b
In [3]: parse("(a | b)")
Out[3]: AAG(header=Header(max_var_index=7, num_inputs=2, num_latches=0, num_outputs=1, num_ands=1), inputs={'a': 2, 'b': 4}, outputs={'ee0a93a4-5152-11e8-bc0d-7c7a919e7753': 15}, latches={}, gates=[[14, 3, 5]], comments=[''])

#  Historically, yellow implies that not blue since brown or always not blue.
In [4]: parse("H(yellow -> [~blue M brown])")
Out[4]: AAG(header=Header(max_var_index=14, num_inputs=3, num_latches=2, num_outputs=1, num_ands=4), inputs={'yellow': 2, 'blue': 4, 'brown': 6}, outputs={'fa1ebbfc-5152-11e8-bc0d-7c7a919e7753': 26}, latches={'lfa1e9a0a-5152-11e8-bc0d-7c7a919e7753': [14, 13, 1], 'lfa1ebda0-5152-11e8-bc0d-7c7a919e7753': [28, 26, 1]}, gates=[[16, 5, 14], [12, 7, 17], [22, 2, 17], [26, 23, 28]], comments=[''])
```
