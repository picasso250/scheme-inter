# 3 node type
# function
# number
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
    [lambda c: c.isalpha() or c.isdigit() or c == '-' or c == '_', 'token', lambda c, i: (i+c, None)],
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

def token(code):
    print('code', code)
    tokens = []
    state = 'normal'
    liter = ''
    ln = 1
    col = 0
    for char in code:
        #print('char =', char, 'state', state)
        if state not in trans_table:
            print('Error:', state, 'not in trans table')
            return None
        entries = trans_table[state]
        for entry in entries:
            #print('.')
            char_cond = entry[0]
            next_state = entry[1]
            callback = entry[2]
            if char_cond(char):
                #print('next state', next_state)
                liter, token, msg = callback(char, liter)
                if token is not None:
                    #print(token)
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
    #print('tokens', tokens)
    return tokens

'''return an expression'''
def grammer_iter(tokens):
    #print('parse', tokens)
    if len(tokens) == 0:
        return [], []
    l = []
    while len(tokens) > 0:
        token = tokens[0]
        #print('for token', token)
        left = tokens[1:]
        if token['type'] == 'left parenthesis':
            print('enter with', left)
            il, left = grammer_iter(left)
            l.append(il)
        elif token['type'] == 'right parenthesis':
            return l, left
        else:
            print('apeend', token)
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
        print('enter with', tokens[1:])
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

def sum_(params):
    if len(params) == 0:
        print('+ with no params')
        return None
    for p in params:
        if not isinstance(p, list) and p['type'] != 'digit':
            print('Error: type is not number, but', p['type'])
            return 0
    return sum([evalue_expr(e) for e in params])

def sub_(params):
    if len(params) == 0:
        print('- with no params')
        return 0
    i = 0
    for p in params:
        if not isinstance(p, list) and p['type'] != 'digit':
            print('Error: type is not number, but', p['type'])
            return 0
        if i == 0:
            s = evalue_expr(p)
        else:
            s -= evalue_expr(p)
        i += 1
    return s

def mul_(params):
    if len(params) == 0:
        print('* with no params')
        return 0
    s = 1
    for p in params:
        if not isinstance(p, list) and p['type'] != 'digit':
            print('Error: type is not number, but', p['type'])
            return 0
        else:
            s *= evalue_expr(p)
    return s

def div_(params):
    if len(params) == 0:
        print('/ with no params')
        return 0
    i = 0
    for p in params:
        if not isinstance(p, list) and p['type'] != 'digit':
            print('Error: type is not number, but', p['type'])
            return 0
        if i == 0:
            s = evalue_expr(p)
        else:
            s /= evalue_expr(p)
        i += 1
    return s

def mod_(params):
    if len(params) == 0:
        print('% with no params')
        return 0
    len_params = len(params)
    if len(params) != 2:
        print('% need 2 params,', len_params, 'given')
        return 0
    for p in params:
        if not isinstance(p, list) and p['type'] != 'digit':
            print('Error: type is not number, but', p['type'])
            return 0
    return evalue_expr(params[0]) % evalue_expr(params[1])

def evalue_node(node):
    node_type = node['type']
    node_liter = node['liter']
    if node_type == 'digit':
        return float(node_liter)
    if node_type == 'string':
        return node_liter
    print('Error,', node_type, 'can not be evaluated')
    return None

def evalue_list(list_):
    return [evalue_node(e) for e in list_]

func_table = {
    '+': sum_,
    '-': sub_,
    '*': mul_,
    '/': div_,
    '%': mod_
    }

def evalue_expr(expr):
    if isinstance(expr, list):
        lmd = expr[0]
        lmd_type = lmd['type']
        if lmd_type != 'token':
            print('Error, type of head element of list should be token,', lmd_type, 'given')
            return None
        name = lmd['liter']
        print('lambda name', name)
        if name not in func_table:
            print('there is no lambda name', name)
            return None
        func = func_table[name]
        param_list = (expr[1:])
        print('param list', param_list)
        return func(param_list)
    else:
        return evalue_node(expr)

''' evalue list of expr '''
def evalue(ast):
    if len(ast) == 0:
        return None
    for expr in ast:
        val = evalue_expr(expr)
    return val

def evalue_code(code):
    tokens = token(code)
    print('== tokens', tokens)
    ast = grammer(tokens)
    print ('== ast', ast)
    val = evalue(ast)
    print('=============',val)

code = '(+ 137 349)';

statement = {
    'oper': {
        'type': 'lambda',
        'name': '+'
        },
    'params': [
        {
            'type': 'number',
            'value': 137
            },
        {
            'type': 'number',
            'value': 349
            }
        ]
    }
#ast = [statement]
#tokens = token(code)
#print('tokens', tokens)
#ast = grammer(tokens)
#print ('ast', ast)
#val = evalue(ast)
#print(val)

#evalue_code('(+ 137 349)')

#evalue_code('(- 1000 334)')
#evalue_code('(* 5 99)')
#evalue_code('(/ 10 5)')
#evalue_code('(+ 2.7 10)')

#evalue_code('(+ 21 35 12 7)')
#evalue_code('(* 25 4 12)')

#evalue_code('(+ (* 3 5) (- 10 6))')

evalue_code('(+ (* 3 (+ (* 2 4) (+ 3 5))) (+ (- 10 7) 6))')
evalue_code('''(+ (* 3
      (+ (* 2 4)
         (+ 3 5)))
   (+ (- 10 7)
      6))''')

