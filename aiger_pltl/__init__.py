from uuid import uuid1

import funcy as fn
from aiger.common import AAG, Header, and_gate, or_gate, bit_flipper
from parsimonious import Grammar, NodeVisitor


PLTL_GRAMMAR = Grammar(u'''
phi =  wsince / or / and / implies / hist / past / vyest / neg / AP
or = "(" _ phi _ "|" _ phi _ ")"
implies = "(" _ phi _ "->" _ phi _ ")"
and = "(" _ phi _ "&" _ phi _ ")"
hist = "H" _ phi
past = "P" _ phi
vyest = "Z" _ phi
wsince = "[" _ phi _ "M" _ phi _ "]"
neg = "~" _ phi

_ = ~r" "*
AP = ~r"[a-zA-z]" ~r"[a-zA-Z\d]*"
EOL = "\\n"
''')


class PLTLVisitor(NodeVisitor):
    def generic_visit(self, _, children):
        return children

    def visit_phi(self, _, children):
        return children[0]

    def visit_AP(self, node, _):
        return atomic_pred(node.text, node.text)

    def visit_and(self, _, children):
        _, _, left, _, _, _, right, _, _ = children
        combined = left | right
        return combined >> and_gate(combined.outputs, str(uuid1()))

    def visit_or(self, _, children):
        _, _, left, _, _, _, right, _, _ = children
        combined = left | right
        return combined >> or_gate(combined.outputs, str(uuid1()))

    def visit_neg(self, _, children):
        _, _, phi = children
        return phi >> bit_flipper(phi.outputs)

    def visit_hist(self, _, children):
        _, _, phi = children
        (out,) = phi.outputs.keys()
        return phi >> historically(out, str(uuid1()))

    def visit_past(self, _, children):
        _, _, phi = children
        (out,) = phi.outputs.keys()
        return phi >> past(out, str(uuid1()))

    def visit_vyest(self, _, children):
        _, _, phi = children
        (out,) = phi.outputs.keys()
        return phi >> vyesterday(out, str(uuid1()))

    def visit_wsince(self, _, children):
        _, _, left, _, _, _, right, _, _ = children
        (a,) = left.outputs.keys()
        (b,) = right.outputs.keys()
        
        return (left | right) >> weak_since(a, b, str(uuid1()))

    def visit_implies(self, _, children):
        _, _, left, _, _, _, right, _, _ = children
        (a,) = left.outputs.keys()
        (b,) = right.outputs.keys()
        
        return (left | right) >> implies(a, b, str(uuid1()))


def parse(pltl_str: str):
    return PLTLVisitor().visit(PLTL_GRAMMAR.parse(pltl_str))


def atomic_pred(a, out):
        return AAG(
        header=Header(1, 1, 0, 1, 0),
        inputs={a: 2},
        outputs={out: 2},
        latches={},
        gates=[],
        comments=['']
    )


def weak_since(a, b, out, latch_name=None):
    if latch_name is None:
        latch_name = f'l{uuid1()}'

    return AAG(
        header=Header(10, 2, 1, 1, 2),
        inputs={a: 2, b: 4},
        outputs={out: 10},
        latches={latch_name: [8, 7, 1]},
        gates=[[10, 2, 8], [6, 5, 11]],
        comments=['']
    )


def past(a, out, latch_name=None):
    if latch_name is None:
        latch_name = f'l{uuid1()}'

    return AAG(
        header=Header(3, 1, 1, 1, 1),
        inputs={a: 2},
        outputs={out: 5},
        latches={latch_name: [6, 5, 0]},
        gates=[[4, 3, 7]],
        comments=['']
    )


def historically(a, out, latch_name=None):
    if latch_name is None:
        latch_name = f'l{uuid1()}'

    return AAG(
        header=Header(3, 1, 1, 1, 1),
        inputs={a: 2},
        outputs={out: 4},
        latches={latch_name: [6, 4, 1]},
        gates=[[4, 2, 6]],
        comments=['']
    )


def implies(a, b, out):
    return AAG(
        header=Header(3, 2, 0, 1, 1),
        inputs={a: 2, b: 4},
        outputs={out: 7},
        latches={},
        gates=[[6, 2, 5]],
        comments=['']
    )


def vyesterday(a, out, latch_name=None):
    if latch_name is None:
        latch_name = f'l{uuid1()}'

    return AAG(
        header=Header(2, 1, 1, 1, 0),
        inputs={a: 2},
        outputs={out: 4},
        latches={latch_name: [4, 2, 1]},
        gates=[],
        comments=['']
    )
