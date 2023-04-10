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
        return f  # must return raw function, otherwise, raw function will be assigned as None
    return add

'''
args is scheme list(Pair list, actually)
'''

# define_SF -> '(' 'define' Identifier Expression ')' | 
#               '(' 'define' '(' Identifier (Identifier)* ')' (Expression)+ ')'
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
        params = func_sign.rest
        validate_formals(params)
        body = args.rest
        procedure = LambdaProcedure(params, body, env)
        env.define(identifier, procedure)
        return identifier


# is_SF -> '(' 'if' Expression Expression (Expression)? ')'
@special_form("if")
def if_eval(args, env):
    validate_form(args, 2)
    flag = scheme_eval(args.first, env)
    if is_scheme_true(flag):
        return scheme_eval(args.rest.first, env, True)
    if args.rest.rest == nil:
        return None
    return scheme_eval(args.rest.rest.first, env, True)


# cond_SF -> '(' 'cond' (cond_clause)+ (cond_else)* ')'
#   cond_clause -> '(' Expression (Expression)* ')'
#   cond_else -> '(' 'else' (Expression)* ')'
@special_form("cond")
def cond_eval(args, env):
    validate_form(args, 1)
    while args != nil:
        clause = args.first
        validate_form(clause, 1)
        flag = False
        if clause.first == 'else':
            flag = True
        else:
            flag = scheme_eval(clause.first, env)
        if is_scheme_true(flag):
            if clause.rest == nil:
                return flag
            return begin_eval(clause.rest, env)
        args = args.rest
    return None


# and_SF -> '(' 'and' (Atomic)* ')'
@special_form("and")
def and_eval(args, env):
    val = True
    while args != nil:
        if not isinstance(args, Pair):
            raise SchemeError("invalid expressions in and: {args}")
        val = scheme_eval(args.first, env)
        if is_scheme_false(val):
            return val
        args = args.rest
    return val


# or_SF -> '(' 'or' (Atomic)* ')'
@special_form("or")
def or_eval(args, env):
    val = False
    while args != nil:
        if not isinstance(args, Pair):
            raise SchemeError("invalid expressions in and: {args}")
        val = scheme_eval(args.first, env)
        if is_scheme_true(val):
            return val
        args = args.rest
    return val


# let_SF -> '(' 'let' '(' (let_bind)* ')' (Expresssion)+ ')'
#   let_bind -> '(' Identifier Expression ')'
@special_form("let")
def let_eval(args, env):
    newFrame = Frame(env)
    # binding temporary-symbol
    bindings = args.first
    while bindings != nil:
        bind = bindings.first
        validate_form(bind, 2, 2)
        identifier = bind.first
        validate_identifier(identifier)
        newFrame.define(identifier, scheme_eval(bind.rest.first, env))
        bindings = bindings.rest
    # interpret Expression s
    body = args.rest
    return begin_eval(body, newFrame)


# begin_SF -> '(' 'begin' (Expression)+ ')'
@special_form("begin")
def begin_eval(args, env):
    ret = None
    if not isinstance(args, Pair):
        raise SchemeError("invalid expressions in begin eval: {args}")
    while args != nil:
        expr = args.first
        args = args.rest
        ret = scheme_eval(expr, env)
    return ret


@special_form("lambda")
def lambda_eval(args, env):
    validate_form(args, 2)
    return LambdaProcedure(args.first, args.rest, env)


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


# mu_SF -> '(' 'mu' '(' (Identifier)+ ')' (Expression)* ')'
@special_form("mu")
def mu_eval(args, env):
    validate_form(args, 2)
    params = args.first
    body = args.rest
    return MuProcedure(params, body)
