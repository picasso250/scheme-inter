
class Log(object):
    """docstring for Log"""
    def __init__(self):
        super(Log, self).__init__()
        self.debug_ = True
    
    def debug(self, *arg):
        if self.debug_:
            print(*arg)

log = Log()
log.debug_ = True

# 3 node type
# function
# digit
# string

# key: cur_state
# value: cur_char, next_state, callback(char, literal, token) => (literal, token, ErrorMessage)

when_normal = [
    [lambda c: c == '(', 'normal', lambda c, i: (None, [{'type': 'left parenthesis'}], None)],
    [lambda c: c == ')', 'normal', lambda c, i: (None, [{'type': 'right parenthesis'}], None)],
    [lambda c: c.isdigit(), 'digit', lambda c, i: (c, None, None)],
    [lambda c: c.isspace(), 'normal', lambda c, i: (None, None, None)],
    [lambda c: c == '"', 'string', lambda c, i: ('', None, None)],
    [lambda c: True, 'token', lambda c, i: (c, None, None)],
    ]
when_digit = [
    [lambda c: c.isdigit() or c == '.', 'digit', lambda c, i: (i+c, None, None)],
    [lambda c: c.isspace(), 'normal', lambda c, i: (None, [{'type': 'digit', 'liter': i}], None)],
    [lambda c: c == ')', 'normal', lambda c, i: (None, [{'type': 'digit', 'liter': i}, {'type': 'right parenthesis'}], None)],
    [lambda c: True, 'error', lambda c, i: (None, None, 'digit '+literal+', should not follow by '+char)],
    ]
when_token = [
    [lambda c: c.isalpha() or c.isdigit() or c == '-' or c == '_', 'token', lambda c, i: (i+c, None, None)],
    [lambda c: c.isspace(), 'normal', lambda c, i: (None, [{'type': 'token', 'liter': i}], None)],
    [lambda c: c == ')', 'normal', lambda c, i: (None, [{'type': 'token', 'liter': i}, {'type': 'right parenthesis'}], None)],
    [lambda c: True, 'error', lambda c, i: (None, None, 'digit '+literal+', should not follow by '+char)],
    ]
when_string = [
    [lambda c: c == '"', 'normal', lambda c, i: (None, [{'type': 'string', 'liter': i}], None)],
    [lambda c: c == '\\', 'escape', lambda c, i: (None, None, None)],
    [lambda c: True, 'error', lambda c, i: (i+c, None, None, None)],
    ]
escape_table = {
    'n': "\n",
    'r': "\r",
    't': "\t",
    'v': "\v",
    }
when_escape = [
    [lambda c: c == 'n', 'string', lambda c, i: (escape_table[c], None, None)],
    [lambda c: True, 'string', lambda c, i: (i+'\\'+c, None, None)],
    ]
trans_table = {
    'normal': when_normal,
    'digit': when_digit,
    'token': when_token,
    'string': when_string,
    'escape': when_escape
    }

'''scan'''
def token(code):
    print('code', code)
    tokens = []
    state = 'normal'
    liter = ''
    ln = 1
    col = 0
    for char in code:
        # print('char =', char, 'state', state)
        if state not in trans_table:
            print('Error:', state, 'not in trans table')
            return None
        entries = trans_table[state]
        for entry in entries:
            # print('.')
            char_cond = entry[0]
            next_state = entry[1]
            callback = entry[2]
            if char_cond(char):
                # print('next state', next_state)
                liter, token, msg = callback(char, liter)
                if token is not None:
                    # print(token)
                    tokens += (token)
                elif liter is None and token is None:
                    if msg is not None:
                        print('line', ln, 'col', col, msg)
                        return None
                state = next_state
                
                break;
        col += 1
        if char == "\n":
            ln += 1
            col = 0
    if liter is not None:
        tokens.append({'type': 'token', 'liter': liter})
    log.debug('tokens', tokens)
    return tokens

'''return an expression'''
def grammer_iter(tokens):
    log.debug('parse', tokens)
    if len(tokens) == 0:
        return [], []
    l = []
    while len(tokens) > 0:
        token = tokens[0]
        log.debug('for token', token)
        left = tokens[1:]
        if token['type'] == 'left parenthesis':
            log.debug('enter with', left)
            il, left = grammer_iter(left)
            l.append(il)
        elif token['type'] == 'right parenthesis':
            return l, left
        else:
            log.debug('apeend', token)
            l.append(token)
        tokens = left
    print('Error, after ) left', left)
    return None, None

'''return a list of expressions'''
def grammer(tokens):
    if len(tokens) == 0:
        print('no tokens')
        return []
    token = tokens[0]
    token_type = token['type']
    if token_type == 'left parenthesis':
        log.debug('enter with', tokens[1:])
        ast, left = grammer_iter(tokens[1:])
        if len(left) == 0:
            return [ast]
        else:
            return grammer(left)
    elif token_type == 'right parenthesis':
        print('Eorror, )')
        return None
    else:
        return [token] + grammer(tokens[1:])

def sum_(params, scope = {}):
    if len(params) == 0:
        print('Error: + with no params')
        return None
    for p in params:
        if not isinstance(p, list) and p['type'] != 'token' and p['type'] != 'digit':
            print('Error: type is not number, but', p['type'])
            return 0
    return sum([evalue_expr(e, scope) for e in params])

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

# maybe var_table and func_table should be one
var_table = {}
func_table = {
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
    if name in var_table:
        print('Warn:', name, 'has been define')
    var_table[name] = value
    return name

def evalue_lambda(body, param_name_list, params, scope):
    log.debug('evalue_lambda params', param_name_list, params)
    log.debug('scope', scope)
    scope_var_table = {}
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
    if name in func_table:
        print('Warn:', name, 'in func_table')
    func_table[name] = user_func(body, params)
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


func_table['define'] = define

def evalue_node(node, scope = {}):
    log.debug('evalue_node', node)
    node_type = node['type']
    node_liter = node['liter']
    if node_type == 'digit':
        return float(node_liter)
    if node_type == 'string':
        return node_liter
    log.debug('scope', scope)
    if node_type == 'token':
        if node_liter in var_table:
            return evalue_expr(var_table[node_liter])
        elif node_liter in scope:
            return evalue_expr(scope[node_liter])
        else:
            print('Error, token', node_liter, 'can not be evaluated')
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
        lmd_type = lmd['type']
        if lmd_type != 'token':
            print('Error, type of head element of list should be token,', lmd_type, 'given')
            return None
        name = lmd['liter']
        log.debug('lambda name', name)
        if name not in func_table:
            print('there is no lambda name', name)
            return None
        func = func_table[name]
        param_list = (expr[1:])
        log.debug('param list', param_list)
        return func(param_list, scope)
    else:
        return evalue_node(expr, scope)

''' evalue list of expr '''
def evalue(ast):
    if len(ast) == 0:
        return None
    for expr in ast:
        val = evalue_expr(expr)
    return val

def evalue_code(code):
    tokens = token(code)
    log.debug('== tokens', tokens)
    ast = grammer(tokens)
    log.debug ('== ast', ast)
    val = evalue(ast)
    log.debug('=============',val)
    return val
