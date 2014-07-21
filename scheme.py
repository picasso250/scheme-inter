import logger
import scanner

log = logger.Log()
log.debug_ = True

import buildin

g_var_table = buildin.g_var_table

def define_var(name, value):
    if not isinstance(name, str):
        print(name)
        raise Exception('Error: can not be defined')
    if name in g_var_table:
        print('Warn:', name, 'has been define')
    v, _ = evalue_expr(value)
    g_var_table[name] = v
    return name, {}

# evaluate user defined lambda
def evalue_lambda(name, body, param_name_list, params, scope):
    log.debug('evalue_lambda params', param_name_list, params)
    # log.debug('scope', scope)
    scope_var_table = scope
    if len(param_name_list) != len(params):
        raise Exception(name, 'params count not compatible, expected '+len(param_name_list)+', given', len(params))

    # assign
    i = 0
    for pname in param_name_list:
        scope[pname] = params[i]
        i += 1
    rs = evalue_expr(body, scope)
    log.debug('evalue_lambda', name, body, param_name_list, params, scope, '==>', rs)
    v, s = rs
    return v

def user_func(name, body, param_name_list):
    return lambda params, scope: evalue_lambda(name, body, param_name_list, params, scope)

def define_func(name_list, body):
    for node in name_list:
        if not isinstance(node, str):
            print(node)
            raise Exception('Error: node is not token')
            return None
    params = name_list[1:]
    name = name_list[0]
    print('g_var_table', g_var_table)
    if name in g_var_table:
        print('Warn:', name, 'in g_var_table')
    g_var_table[name] = user_func(name, body, params)
    return name, {}

def define(params, scope = {}):
    if len(params) == 0:
        raise Exception('Error: define with no params')
        return None
    if len(params) != 2:
        raise Exception('Error: define has two params')
        return None
    name_node = params[0]
    value = params[1]
    if isinstance(name_node, list):
        return define_func(name_node, value)
    else:
        return define_var(name_node, value)

g_verb_table = {}
g_verb_table['define'] = define

def evalue_node(node, scope = {}):
    # log.debug('evalue_node', node)
    if isinstance(node, int) or isinstance(node, float) or isinstance(node, bool):
        return node
    if isinstance(node, tuple):
        if len(node) != 2:
            print(node)
            raise Exception('unknown tuple')
        t, value = node
        if t != 'string':
            raise Exception('unknown type '+t+', should be string')
        return value
    log.debug('scope', scope)
    if isinstance(node, str):
        if node in g_var_table:
            return (g_var_table[node])
        elif node in scope:
            return (scope[node])
        else:
            raise Exception('Error, token', node, 'can not be evaluated')
            return None
    print('Error,', node_type, 'can not be evaluated')
    return None

def evalue_expr(expr, scope = {}):
    if isinstance(expr, list):
        if len(expr) == 0:
            log.debug('list is empty')
            return None
        lmd = expr[0]
        if not isinstance(lmd, str):
            print('Error, type of head element of list should be token')
            return None
        # log.debug('lambda name', lmd)
        param_list = expr[1:]
        if lmd not in g_var_table:
            # print('there is no lambda name', lmd)
            if lmd not in g_verb_table:
                raise Exception('no lambda '+lmd)
            else:
                func = g_verb_table[lmd]
                value, more_scope = func(param_list)
                scope = scope.update(more_scope)
                print('scope', scope)
                return value, scope
            return None
        func = g_var_table[lmd]
        log.debug('param list', param_list)
        plist = [evalue_expr(p, scope)[0] for p in param_list]
        return func(plist, scope), scope
    else:
        return evalue_node(expr, scope), scope

''' evalue list of expr '''
def evalue_ast(ast):
    if len(ast) == 0:
        return None
    env = {}
    for expr in ast:
        val, env_update = evalue_expr(expr, env)
        print('env_update', env_update)
        if env_update is not None:
            env.update(env_update)
        print('g_var_table', g_var_table)
    return val

'''
ast  ::= expr*
expr ::= node|list
node ::= token|string|digit
'''
def evalue_code(code):
    ast = scanner.scan_code(code)
    log.debug ('== ast ==', ast)
    val = evalue_ast(ast)
    log.debug('=== val ===',val)
    return val
