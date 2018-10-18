from uuid import uuid1

import aiger
import funcy as fn
from lenses import bind

from parsimonious import Grammar, NodeVisitor
import hypothesis.strategies as st
from hypothesis_cfg import ContextFreeGrammarStrategy


PLTL_GRAMMAR = Grammar(u'''
phi =  since / wsince / or / and / implies / hist / past / vyest / neg / AP
or = "(" _ phi _ "|" _ phi _ ")"
implies = "(" _ phi _ "->" _ phi _ ")"
and = "(" _ phi _ "&" _ phi _ ")"
hist = "H" _ phi
past = "P" _ phi
vyest = "Z" _ phi
since = "[" _ phi _ "S" _ phi _ "]"
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
        return aiger.atom(node.text)

    def visit_and(self, _, children):
        return children[2] & children[6]

    def visit_or(self, _, children):
        return children[2] | children[6]

    def visit_neg(self, _, children):
        return ~children[2]

    def visit_implies(self, _, children):
        return children[2].implies(children[6])

    def visit_vyest(self, _, children):
        return vyest(children[2])

    def visit_hist(self, _, children):
        return historically(children[2])

    def visit_past(self, _, children):
        return once(children[2])
    
    def visit_wsince(self, _, children):
        return weak_since(children[2], children[6])

    def visit_since(self, _, children):
        return since(children[2], children[6])


def vyest_monitor(name):
    return aiger.delay(
        inputs=[name],
        initials=[True],
        latches=[aiger.common._fresh()],
        outputs=[aiger.common._fresh()]
    )


def vyest(expr):
    return aiger.BoolExpr(expr.aig >> vyest_monitor(expr.output))


def hist_monitor(name):
    out = aiger.common._fresh()
    return aiger.and_gate([name, 'tmp'], out).feedback(
        inputs=['tmp'],
        outputs=[out],
        latches=[aiger.common._fresh()],
        initials=[True],
        keep_outputs=True
    )


def historically(expr):
    return aiger.BoolExpr(expr.aig >> hist_monitor(expr.output))


def past_monitor(name):
    out = aiger.common._fresh()
    return aiger.or_gate([name, 'tmp'], out).feedback(
        inputs=['tmp'],
        outputs=[out],
        latches=[aiger.common._fresh()],
        initials=[False],
        keep_outputs=True
    )


def since_monitor(left, right):
    circ = aiger.and_gate([left, 'active'], 'active')
    circ >>= aiger.or_gate([right, 'active'], 'tmp')
    return circ.feedback(
        inputs=['active'],
        outputs=['tmp'],
        latches=[aiger.common._fresh()],
        initials=[True],
        keep_outputs=True,
    )


def since(left, right):
    monitor = since_monitor(left.output, right.output)
    return aiger.BoolExpr((left.aig | right.aig) >> monitor)


def weak_since(left, right):
    return since(left, right) | historically(~right)


def once(expr):
    return aiger.BoolExpr(expr.aig >> past_monitor(expr.output))


def parse(pltl_str: str, output=None):
    expr = PLTLVisitor().visit(PLTL_GRAMMAR.parse(pltl_str))
    aig = expr.aig.evolve(comments=(pltl_str,))
    if output is not None:
        aig = aig['o', {expr.output: output}]

    return type(expr)(aig)
