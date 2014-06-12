# 3 node type
# function
# number
# string

# key: cur_state
# value: cur_char, next_state, callback(char, literal, token) => (literal, token, ErrorMessage)
when_normal = [
    ['(', 'normal', lambda c, i, t: None, {'type': 'left parenthesis'}, None],
    [')', 'normal', lambda c, i, t: None, {'type': 'right parenthesis'}, None],
    [lambda c: c.isdigit(), 'digit', lambda c, i, t: c, None, None],
    [lambda c: c.isalpha(), 'token', lambda c, i, t: c, None, None],
    [lambda c: c.isspace(), 'token', lambda c, i, t: c, None, None],
    ['"', 'string', lambda c, i, t: '', None, None],
    [True, 'error', lambda c, i, t: None, None, 'unexpected '+c],
    ]
when_digit = [
    [lambda c: c.isdigit() or c == '.', 'digit', lambda c, i, t: i+c, None],
    [lambda c: c.isspace(), 'normal', lambda c, i, t: None, {'type': 'digit', 'liter': i}],
    [True, 'error', lambda c, i, t: None, None, 'digit '+literal+', should not follow by '+char],
    ]
when_token = [
    [lambda c: c.isalpha() or c.isdigit() or c == '-' or c == '_', 'token', lambda c, i, t: i+c, None],
    [lambda c: c.isspace(), 'normal', lambda c, i, t: None, {'type': 'digit', 'liter': i}],
    [True, 'error', lambda c, i, t: None, None, 'digit '+literal+', should not follow by '+char],
    ]
when_string = [
    ['"', 'normal', lambda c, i, t: None, {'type': 'string', 'liter': i}, None],
    ['\\', 'escape', lambda c, i, t: None, None, None],
    [True, 'error', lambda c, i, t: i+c, None, None, None],
    ]
escape_table = {
    'n': "\n",
    'r': "\r",
    't': "\t",
    'v': "\v",
    }
when_escape = [
    ['n', 'string', lambda c, i, t: escape_table[c], None, None],
    [True, 'string', lambda c, i, t: i+'\\'+c, None, None],
    ]
transfer_table = {
    'normal': when_normal,
    'digit': when_digit,
    'token': when_token,
    'string': when_string,
    'escape': when_escape
    }
def token(code):
    tokens = []
    state = 'normal'
    literal = ''
    for char in code:
        
        pass

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
