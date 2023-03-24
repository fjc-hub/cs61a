import sys
import os

from pair import *
from scheme_utils import *
from ucb import main, trace

import scheme_forms

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
    if expr[0] != '(':
        ## Atomic Expressions
        if expr.isdigit():
            return int(expr)  # Number
        elif expr in ['#t', '#f']:
            return expr  # Boolean
        elif expr[0] == "'":
            return expr[1:]  # string
        elif expr == 'nil':
            return nil  # empty list
        else:
            return env.lookup(expr)  # symbol
    else:
        ## Non-atomic Expressions
        arr = expr[1:-1].split(' ')
        return scheme_apply(arr[0], arr[1:], env)


def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    Frame ENV, the current environment."""
    

def read_line(str):
    


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
