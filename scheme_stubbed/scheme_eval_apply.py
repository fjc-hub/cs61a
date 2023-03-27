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
#   1.Expression -> CallExpression | Atomic | SpecialForm
#   2.CallExpression -> '(' identifier (Expression)* ')'
#   3.Identifier: 标识符, differ from built-in keyword
#   4.Keyword: 关键字, built-in procedure's name and special form's name
#   4.Atomic -> integer | float | string | scheme-list | symbol
#   5.SpecialForm -> define_SF | if_SF | cond_SF | and_SF | or_SF | let_SF | begin_SF |
#                   lambda_SF | quote_SF | quasiquote_SF | unquote_SF | mu_SF
#   remainded syntax analysis of SpecialForm are listed in scheme_forms.py file
#   

KEYWORDS = scheme_builtins.BUILTINS[:]  # copying after BUILTINS inited by decorator?

# Get result of Expression
#   1.AtomicExpression(primitive-value)
#   2.SpecialForm
#   3.CallExpression
def scheme_eval(expr, env, _=None):  # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in Frame ENV.

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    print("DEBUG:", expr, type(expr)) 
    if isinstance(expr, (int, float, type(nil), str)):
        ## AtomicExpression
        if not isinstance(expr, str):
            return expr
        else:
            if expr in KEYWORDS:
                return f"[{expr}]"
            elif expr[0] == "'":
                return expr[1:]  # string
            elif expr in ['#t', '#f']:
                return expr  # Boolean
            else:
                return env.lookup(expr)  # symbol
    elif isinstance(expr, Pair):
        ## SpecialForm
        if expr.first in scheme_forms.SPECIAL_FORM_NAMES:
            func = scheme_forms.SPECIAL_FORM_FUNC[expr.first]
            return func(expr.rest, env)
        ## CallExpression
        arguments = expr.rest.map(lambda x: scheme_eval(x, env))
        return scheme_apply(expr.first, arguments, env)
    else:
        raise SchemeError("unknown expr in scheme_eval")

# Get result of CallExpression:
#   1.Built-in Procedure(primitive-procedure, no new Frame/Env)  
#   2.User-defined Procedure
def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list/Pair LinkList) in
    Frame ENV, the current environment."""
    ## Built-in Procedure
    for built_func in scheme_builtins.BUILTINS:
        if built_func[0] == procedure:
            params = args.flatmap(lambda x:x)
            if len(params) == 0:
                return built_func[1]()
            elif len(params) == 1:
                return built_func[1](params[0])
            elif len(params) == 2:
                return built_func[1](params[0], params[1])
            elif len(params) == 3:
                return built_func[1](params[0], params[1], params[2])
            else:
                return built_func[1](params)
    ## User-defined Procedure
    proc = env.lookup(procedure)
    return scheme_eval(proc, Frame(env))


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
