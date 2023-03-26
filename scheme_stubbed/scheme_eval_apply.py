import sys
import os

from pair import *
from scheme_utils import *
from ucb import main, trace

import scheme_forms
import scheme_tokens

##############
# Eval/Apply #
##############


def scheme_eval(expr, env, _=None):  # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in Frame ENV.

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    if expr.rest == nil:
        ## Atomic Expressions
        item = expr.first
        if item.isdigit():
            return int(item)  # Number
        elif item in ['#t', '#f']:
            return item  # Boolean
        elif item[0] == "'":
            return item[1:]  # string
        elif item == 'nil':
            return nil  # empty list
        else:
            return env.lookup(item)  # symbol
    else:
        ## Non-atomic Expressions
        return scheme_apply(expr.first, expr.rest.map(scheme_eval), env)


def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    Frame ENV, the current environment."""
    if procedure in scheme_forms.SPECIAL_FORM_NAMES:
        ## Special Form
        func = scheme_forms.SPECIAL_FORM_FUNC[procedure]
        return func(args, env)
    else:
        pass
        ## Call
        # bulit-in
        
        # user-define
    

def read_line(str):
    lst = scheme_tokens.tokenize_line(str)
    head = Pair('head', nil)
    tmp = head
    for p in lst:
        tmp.rest = Pair(p, nil)
        tmp = tmp.rest
    return head.rest


##################
# Tail Recursion #
##################

# Make classes/functions for creating tail recursive programs here!
# BEGIN Problem EC
"*** YOUR CODE HERE ***"
# END Problem EC


def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not Unevaluated.
    Right now it just calls scheme_apply, but you will need to change this
    if you attempt the extra credit."""
    validate_procedure(procedure)
    # BEGIN
    return val
    # END
