import hypothesis.strategies as st
from hypothesis import given
from hypothesis_cfg import ContextFreeGrammarStrategy

from aiger_ptltl.ptltl import parse

GRAMMAR = {
    'phi': (
        ('Unary', 'phi'),
        ('(', 'phi', 'Binary', 'phi', ')'),
        ('[', 'phi', ' S ', 'phi', ']'),
        ('AP', ),
    ),
    'Unary': (('~', ), ('P',), ('H',), ('Z', )),
    'Interval': (('', ), ('[1, 3]', )),
    'Binary': (
        (' | ', ), (' & ', ), (' -> ', ),
    ),
    'AP': (('ap1', ), ('ap2', ), ('ap3', ), ('ap4', ), ('ap5', )),
}

PTLTL_STRATEGY = st.builds(
    lambda term: parse(''.join(term)),
    ContextFreeGrammarStrategy(GRAMMAR, max_length=14, start='phi')
)


TRUE = {'ap1': True, 'ap2': True, 'ap3': True, 'ap4': True, 'ap5': True}
VALUE_STRATEGY = st.fixed_dictionaries({
    'ap1': st.booleans(),
    'ap2': st.booleans(),
    'ap3': st.booleans(),
    'ap4': st.booleans(),
    'ap5': st.booleans(),
})
TRACE_STRATEGY = st.lists(VALUE_STRATEGY, min_size=1)


@given(PTLTL_STRATEGY, VALUE_STRATEGY)
def test_smoke_value_eval(expr, val):
    res = expr(val)
    assert isinstance(res, bool)


@given(PTLTL_STRATEGY, PTLTL_STRATEGY, TRACE_STRATEGY)
def test_hist_identity(expr1, expr2, trc):
    expr3 = expr1.historically() & expr2.historically()
    expr4 = (expr1 & expr2).historically()
    assert expr3(trc) == expr4(trc)


@given(PTLTL_STRATEGY, PTLTL_STRATEGY, TRACE_STRATEGY)
def test_past_identity(expr1, expr2, trc):
    expr3 = expr1.once() | expr2.once()
    expr4 = (expr1 | expr2).once()
    assert expr3(trc) == expr4(trc)


@given(PTLTL_STRATEGY, TRACE_STRATEGY)
def test_since_to_once_reduction(expr, trc):
    expr2 = expr.once()
    expr3 = parse('TRUE').since(expr)
    assert expr2(trc) == expr3(trc)


@given(PTLTL_STRATEGY, TRACE_STRATEGY)
def test_false_since(expr, trc):
    expr2 = parse('FALSE').since(expr)
    assert expr2(trc) == expr(trc)
