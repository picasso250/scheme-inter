# 3 node type
# function
# number
# string

def grammer(code):
    ast = []
    print('first char', code[0])
    
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
#ast = grammer(code)
val = evalue(ast)
print(val)
