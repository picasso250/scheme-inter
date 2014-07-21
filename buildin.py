def sum_(params, scope = {}):
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
        if not isinstance(p, int) and not isinstance(p, float):
            print(p)
            raise Exception('Error: type is not number')
            return 0
        if i == 0:
            s = p
        else:
            s -= p
        i += 1
    return s

def mul_(params, scope = {}):
    if len(params) == 0:
        print('* with no params')
        return 0
    s = 1
    for p in params:
        if not isinstance(p, int) and not isinstance(p, float):
            print(p)
            raise Exception('Error: type is not number')
            return 0
        else:
            s *= p
    return s

def div_(params, scope = {}):
    if len(params) == 0:
        print('/ with no params')
        return 0
    i = 0
    for p in params:
        if not isinstance(p, int) and not isinstance(p, float):
            print(p)
            raise Exception('Error: type is not number')
            return 0
        if i == 0:
            s = p
        else:
            s /= p
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
