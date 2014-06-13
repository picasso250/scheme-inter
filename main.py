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
        print('char =', char, 'state', state)
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
                print('next state', next_state)
                liter, token, msg = callback(char, liter)
                if token is not None:
                    print(token)
                    tokens += (token)
                elif liter is None and token is None:
                    print('line', ln, 'col', col, msg)
                    return None
                state = next_state
                
                break;
        col += 1
        if char == "\n":
            ln += 1
            col = 0
    print('tokens', tokens)
    return tokens

def grammer(code):
    ast = []
    print('first char', code[0])
    for char in code:
        print(char)
    return ast

def sum_(params):
    if len(params) == 0:
        print('+ with no params')
        return None
    for p in params:
        if p['type'] != 'number':
            print('Error: type is not number, but', p['type'])
            return None
    int_list = [i['value'] for i in params]
    print('sum of', int_list)
    return sum(int_list)

def sub_(params):
    if len(params) == 0:
        print('- with no params')
        return 0
    for p in params:
        if p['type'] != 'number':
            print('Error: type is not number, but', p['type'])
            return 0
    i = params.pop(0)['value']
    return reduce(lambda a,b: a-b, params, i)

def mul_(params):
    if len(params) == 0:
        print('* with no params')
        return 0
    s = 1
    for p in params:
        if p['type'] != 'number':
            print('Error: type is not number, but', p['type'])
            return 0
        else:
            s *= p['value']
    return s

def div_(params):
    if len(params) == 0:
        print('/ with no params')
        return 0
    for p in params:
        if p['type'] != 'number':
            print('Error: type is not number, but', p['type'])
            return 0
    i = params.pop(0)['value']
    return reduce(lambda a,b: a/b, params, i)

def mod_(params):
    if len(params) == 0:
        print('% with no params')
        return 0
    len_params = len(params)
    if len(params) != 2:
        print('% need 2 params,', len_params, 'given')
        return 0
    return params[0]['value'] % params[1]['value']

func_table = {
    '+': sum_,
    '-': sub_,
    '*': mul_,
    '/': div_,
    '%': mod_
    }

def evalue_statement(statement):
    pass
    name = statement['oper']['name']
    print('lambda name', name)
    if name not in func_table:
        print('there is no lambda name', name)
        return None
    func = func_table[name]
    return func(statement['params'])

def evalue(ast):
    if len(ast) == 0:
        return None
    for statement in ast:
        val = evalue_statement(statement)
    return val

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
ast = [statement]
tokens = token(code)
print('tokens', tokens)
ast = grammer(tokens)
val = evalue(ast)
print(val)
