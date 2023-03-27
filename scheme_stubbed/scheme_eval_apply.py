import sys
import os

from pair import *
from scheme_utils import *
from ucb import main, trace

import scheme_forms
import scheme_tokens
import scheme_builtins

##############
# Eval/Apply #
##############

# Syntax Analysis:
# parentheses are ignored by cs61a's tokenizer, but it's still listed in Syntax Analysis.
# (x) represents optional element.
# x* represents one or more element.
# x? represents zero or one element.
# 
#   1.Expression -> '(' Procedure (Expression)* ')' | Atom
#   2.Atom -> integer | float | string | scheme-list | symbol
#   3.SpecialForm -> define_SF | if_SF | cond_SF | and_SF | or_SF | let_SF | begin_SF |
#                   lambda_SF | quote_SF | quasiquote_SF | unquote_SF | mu_SF
#   remainded syntax analysis of SpecialForm are listed in scheme_forms.py file
#   

# Get result of Expression
#   1.Atomic-Expression(primitive-value)
#   2.Special-Form
#   3.Call-Expression
def scheme_eval(expr, env, _=None):  # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in Frame ENV.

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    if isinstance(expr, (int, float, nil, str)):
        ## Atomic Expressions
        if not isinstance(expr, str):
            return expr
        else:
            if expr[0] == "'":
                return expr[1:]  # string
            elif expr in ['#t', '#f']:
                return expr  # Boolean
            else:
                return env.lookup(expr)  # symbol
    elif isinstance(expr, Pair):
        ## Call-Expression
        if expr.first not in scheme_forms.SPECIAL_FORM_NAMES:
            arguments = expr.rest.map(lambda x: scheme_eval(x, env))
            return scheme_apply(expr.first, arguments, env)
        ## Special-Form
        if expr.first == ''
        func = scheme_forms.SPECIAL_FORM_FUNC[expr.first]
        return func(args, env)
    else:
        raise TypeError("unknown expr in scheme_eval")

# Get result of:
#   1.Built-in Procedure(primitive-procedure)  
#   2.User-defined Procedure
def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    Frame ENV, the current environment."""
    if procedure in scheme_forms.SPECIAL_FORM_NAMES:
        ## Special Form
        func = scheme_forms.SPECIAL_FORM_FUNC[procedure]
        return func(args, env)
    else:
        ## Call
        arg_list = args.flatmap(lambda x: scheme_eval(x, env))
        # bulit-in procedure
        for built_func in scheme_builtins.BUILTINS:
            if built_func[0] == procedure:
                return built_func[1]()
        # user-define procedure
        pass
    

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
