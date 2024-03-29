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
    if expr is None:
        return None  # scheme_atomp(None) = False ?
    ## AtomicExpression
    elif scheme_atomp(expr):
        if self_evaluating(expr):
            if scheme_stringp(expr):
                return expr[1:]
            return expr
        else:
            if not scheme_symbolp(expr):
                raise SchemeError(f'unknown atomic but non self-evaluating expr: {expr}')
            return env.lookup(expr)
    elif scheme_listp(expr):
        ## SpecialForm
        if expr.first in scheme_forms.SPECIAL_FORM_NAMES:
            func = scheme_forms.SPECIAL_FORM_FUNC[expr.first]
            ret = func(expr.rest, env)
            # recognize tail call function
            if expr.first == 'define':
                tmp = env.lookup(ret)
                if isinstance(tmp, Procedure) and is_tail_call(ret, tmp):
                    env.define(ret, Unevaluated(tmp.formals, tmp.body, env))
            return ret
        ## CallExpression
        operator = None
        if isinstance(expr.first, Pair):
            operator = scheme_eval(expr.first, env)  # operator maybe a lambda/regular-procedure/mu
        else:
            operator = env.lookup(expr.first)  # look up Procedure in Symbol-Table-Hierachy
        validate_procedure(operator)
        operands = expr.rest.map(lambda x: scheme_eval(x, env))
        return complete_apply(operator, operands, env)  # return scheme_apply(operator, operands, env)
    else:
        raise SchemeError("unknown expr in scheme_eval")



# Get result of CallExpression:
#   1.Built-in Procedure(primitive-procedure, no new Frame/Env)  
#   2.User-defined Procedure
def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list/Pair LinkedList) in
    Frame ENV, the current environment."""
    validate_procedure(procedure)
    ## Built-in Procedure
    if isinstance(procedure, BuiltinProcedure):
        params = []
        while args != nil:
            params.append(args.first)
            args = args.rest
        if procedure.need_env:
            params.append(env)
        try:
            return procedure.py_func(*params)
        except TypeError:
            raise SchemeError('incorrect number of arguments')
    ## User-defined Procedure
    call_frame = None
    if isinstance(procedure, LambdaProcedure):
        call_frame = Frame(procedure.env)
    elif isinstance(procedure, MuProcedure):
        call_frame = env
    else:
        raise TypeError(f"unimplemented procedure: {procedure}")
    assign_args_to_params(call_frame, args, procedure.formals)
    return scheme_forms.begin_eval(procedure.body, call_frame)


# binding arguments to parameters of a function in Frame env
def assign_args_to_params(env, args, params):
    while params != nil and args != nil:  # set argument to Frame
        env.define(params.first, args.first)
        params, args = params.rest, args.rest
    if not (params == nil and args == nil):
        raise SchemeError(f"apply invalid number of arguments to {params}, {args}")
    

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
class Unevaluated:
    """An expression and an environment in which it is to be evaluated."""

    def __init__(self, expr, env):
        """Expression EXPR to be evaluated in Frame ENV."""
        self.expr = expr
        self.env = env


# END Problem EC


def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not Unevaluated.
    Right now it just calls scheme_apply, but you will need to change this
    if you attempt the extra credit."""
    validate_procedure(procedure)
    # BEGIN
    val = scheme_apply(procedure, args, env)
    if isinstance(val, Unevaluated):
        return scheme_eval(val.expr, val.env)
    return val
    # END


def optimize_tail_calls(unoptimized_scheme_eval):
    """Return a properly tail recursive version of an eval function."""
    def optimized_eval(expr, env, tail=False):
        """Evaluate Scheme expression EXPR in Frame ENV. If TAIL,
        return an Unevaluated containing an expression for further evaluation.
        """
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            return Unevaluated(expr, env)

        result = Unevaluated(expr, env)

        # BEGIN PROBLEM EC
        "*** YOUR CODE HERE ***"
        while (isinstance(result, Unevaluated)):
            result = unoptimized_scheme_eval(result.expr, result.env)
        return result
        # END PROBLEM EC
    return optimized_eval


################################################################
# Uncomment the following line to apply tail call optimization #
################################################################

scheme_eval = optimize_tail_calls(scheme_eval)
