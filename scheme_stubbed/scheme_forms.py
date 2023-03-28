from scheme_eval_apply import *
from scheme_utils import *
from scheme_classes import *
from scheme_builtins import *

#################
# Special Forms #
#################

"""
How you implement special forms is up to you. We recommend you encapsulate the
logic for each special form separately somehow, which you can do here.
"""

SPECIAL_FORM_NAMES = []
SPECIAL_FORM_FUNC = {}

def special_form(name):
    def add(f):
        SPECIAL_FORM_FUNC[name] = f
        SPECIAL_FORM_NAMES.append(name)
    return add

'''
Syntax:
    1. <x> refers to a required element x that can be vary
    2. [x] refers to an optional element x

args is scheme list(Pair list, actually)
'''

# define_SF -> '(' 'define' Identifier Expression ')' | 
#               '(' 'define' '(' Identifier (Identifier)* ')' (Expression)* ')'
@special_form("define")
def define_eval(args, env):
    validate_form(args, 2)
    if scheme_symbolp(args.first):
        # binding value to symbol
        identifier = args.first
        validate_identifier(identifier)
        env.define(identifier, scheme_eval(args.rest.first, env))
        return identifier
    else:
        # binding procedure to symbol
        func_sign = args.first
        validate_form(func_sign, 1)  # there must be at least one Pair
        identifier = func_sign.first
        params = func_sign.flatmap(lambda x:x.first)
        body = args.rest
        procedure = LambdaProcedure(params, body, env)
        env.define(identifier, procedure)
        return identifier


@special_form("if")
def if_eval(args, env):
    # (if <predicate> <consequent> [alternative])
    if scheme_eval(args[0], env) == '#t':
        return scheme_eval(args[1], env)
    else:
        return scheme_eval(args[2], env)


@special_form("cond")
def cond_eval(args, env):
    # (cond <clause> ...)
    # <clause> -> (<test> [expression] ...) | (else [expression] ...)
    for clause in args:
        arr = clause[1:-1].split(' ')
        if arr[0] == 'else':
            return scheme_eval(arr[1:], env)
        else:
            if scheme_eval(arr[0], env) == '#t':
                return scheme_eval(arr[1:], env)


@special_form("and")
def and_eval(args, env):
    # (and [test] ...)
    if all([test == '#t' for test in args]):
        return '#t'
    return '#f'


@special_form("or")
def or_eval(args, env):
    # (or [test] ...)
    if any([test == '#t' for test in args]):
        return '#t'
    return '#f'


@special_form("let")
def let_eval(args, env):
    # (let ([binding] ...) <body> ...)
    # [binding] -> (<name> <expression>)
    if args[0][0] == args[0][1] and args[0][1] == '(':
        # binding
        pass

# begin_SF -> '(' 'begin' (Expression)* ')'
@special_form("begin")
def begin_eval(args, env):
    ret = None
    for expr in args.flatmap(lambda x:x.first):
        ret = scheme_eval(expr, env)
    return ret


@special_form("lambda")
def lambda_eval(args, env):
    pass


@special_form("quote")
def quote_eval(args, env):
    validate_form(args, 1, 1)
    return args.first


@special_form("quasiquote")
def quasiquote_eval(args, env):
    pass


@special_form("unquote")
def unquote_eval(args, env):
    pass


@special_form("mu")
def mu_eval(args, env):
    pass
