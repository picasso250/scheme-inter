import logger
import scanner

log = logger.Log()
log.debug_ = True

def sum_(params, scope = {}):
    print('sum of', params)
    if len(params) == 0:
        raise Exception('Error: + with no params')
        return None
    for p in params:
        if not isinstance(p, int) and not isinstance(p, float):
            print(p)
            raise Exception('Error: type is not number')
            return 0
    return sum(params)

def sub_(params, scope = {}):
    if len(params) == 0:
        print('- with no params')
        return 0
    i = 0
    for p in params:
        if not isinstance(p, list) and p['type'] != 'token' and p['type'] != 'digit':
            print('Error: type is not number, but', p['type'])
            return 0
        if i == 0:
            s = evalue_expr(p, scope)
        else:
            s -= evalue_expr(p, scope)
        i += 1
    return s

def mul_(params, scope = {}):
    if len(params) == 0:
        print('* with no params')
        return 0
    s = 1
    for p in params:
        if not isinstance(p, list) and p['type'] != 'token' and p['type'] != 'digit':
            print('Error: type is not number, but', p['type'])
            return 0
        else:
            s *= evalue_expr(p, scope)
    return s

def div_(params, scope = {}):
    if len(params) == 0:
        print('/ with no params')
        return 0
    i = 0
    for p in params:
        if not isinstance(p, list) and p['type'] != 'token' and p['type'] != 'digit':
            print('Error: type is not number, but', p['type'])
            return 0
        if i == 0:
            s = evalue_expr(p, scope)
        else:
            s /= evalue_expr(p, scope)
        i += 1
    return s

def mod_(params, scope = {}):
    if len(params) == 0:
        print('% with no params')
        return 0
    len_params = len(params)
    if len(params) != 2:
        print('% need 2 params,', len_params, 'given')
        return 0
    for p in params:
        if not isinstance(p, list) and p['type'] != 'token' and p['type'] != 'digit':
            print('Error: type is not number, but', p['type'])
            return 0
    return evalue_expr(params[0], scope) % evalue_expr(params[1], scope)

# build in func
g_var_table = {
    '+': sum_,
    '-': sub_,
    '*': mul_,
    '/': div_,
    '%': mod_
    }

def define_var(name_node, value):
    node_type = name_node['type']
    if node_type != 'token':
        print('Error: type', node_type, 'can not be defined')
    name = name_node['liter']
    if name in g_var_table:
        print('Warn:', name, 'has been define')
    g_var_table[name] = value
    return name

# evaluate user defined lambda
def evalue_lambda(body, param_name_list, params, scope):
    log.debug('evalue_lambda params', param_name_list, params)
    log.debug('scope', scope)
    scope_var_table = scope
    i = 0
    for pname in param_name_list:
        log.debug('pname', pname)
        param = params[i]
        if not isinstance(param, list) and param['type'] == 'token':
            scope_pname = param['liter']
            log.debug('scope_pname', scope_pname)
            if scope_pname in scope:
                param = scope[scope_pname]
        scope_var_table[pname] = param
        i += 1
    log.debug('scope_var_table', scope_var_table)
    rs = evalue_expr(body, scope_var_table)
    log.debug('evalue_lambda', body, param_name_list, params, scope, '==>', rs)
    return rs

def user_func(body, params):
    param_name_list = [p['liter'] for p in params]
    return lambda params, scope: evalue_lambda(body, param_name_list, params, scope)

def define_func(name_node, body):
    for node in name_node:
        name_node_type = node['type']
        if name_node_type != 'token':
            print('Error:', name_node_type)
            return None
    params = name_node[1:]
    name_node = name_node[0]
    name = name_node['liter']
    if name in g_var_table:
        print('Warn:', name, 'in g_var_table')
    g_var_table[name] = user_func(body, params)
    return name

def define(params, scope = {}):
    if len(params) == 0:
        print('Error: define with no params')
        return None
    if len(params) != 2:
        print('Error: define has two params')
        return None
    name_node = params[0]
    value = params[1]
    if isinstance(name_node, list):
        return define_func(name_node, value)
    else:
        return define_var(name_node, value)


g_var_table['define'] = define

def evalue_node(node, scope = {}):
    log.debug('evalue_node', node)
    if isinstance(node, int) or isinstance(node, float):
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
            print('Error, token', node, 'can not be evaluated')
            return None
    print('Error,', node_type, 'can not be evaluated')
    return None

def evalue_list(list_):
    return [evalue_node(e) for e in list_]

def evalue_expr(expr, scope = {}):
    if isinstance(expr, list):
        if len(expr) == 0:
            log.debug('list is empty')
            return None
        lmd = expr[0]
        if not isinstance(lmd, str):
            print('Error, type of head element of list should be token')
            return None
        log.debug('lambda name', lmd)
        if lmd not in g_var_table:
            print('there is no lambda name', lmd)
            return None
        func = g_var_table[lmd]
        param_list = expr[1:]
        log.debug('param list', param_list)
        return func([evalue_expr(p, scope)[0] for p in param_list]), scope
    else:
        return evalue_node(expr, scope), scope

''' evalue list of expr '''
def evalue_ast(ast):
    if len(ast) == 0:
        return None
    env = {}
    for expr in ast:
        val, env = evalue_expr(expr, env)
    return val

'''
ast  ::= expr*
expr ::= node|list
node ::= token|string|digit
'''
def evalue_code(code):
    ast = scanner.scan_code(code)
    log.debug ('== ast', ast)
    val = evalue_ast(ast)
    log.debug('=============',val)
    return val
