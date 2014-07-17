import logger

log = logger.Log()
log.debug_ = True

# key: cur_state
# value: cur_char, next_state, callback
# callback(char, literal) => (literal, token_list, ErrorMessage, cmd)
# cmd=push|pop
# token is pure string, and string is ("string", "xxxx"), and digit is digit

when_normal = [
    [lambda c: c == '(', 'normal', lambda c, i: (None, None, None, 'push')],
    [lambda c: c == ')', 'normal', lambda c, i: (None, None, None, 'pop')],
    [lambda c: c.isspace(), 'normal', lambda c, i: (None, None, None)],
    [lambda c: c == '"', 'string', lambda c, i: ('', None, None)],
    [lambda c: True, 'token', lambda c, i: (c, None, None)],
    ]
when_token = [
    [lambda c: c.isalpha() or c.isdigit() or c in '-_?<>', 'token', lambda c, i: (i+c, None, None)],
    [lambda c: c.isspace(), 'normal', lambda c, i: (None, i, None)],
    [lambda c: c == ')', 'normal', lambda c, i: (None, i, None, 'pop')],
    [lambda c: True, 'error', lambda c, i: (None, None, 'token '+i+', should not follow by '+c)],
    ]
when_string = [
    [lambda c: c == '"', 'normal', lambda c, i: (None, ('string', i), None)],
    [lambda c: c == '\\', 'escape', lambda c, i: (None, None, None)],
    [lambda c: True, 'string', lambda c, i: (i+c, None, None, None)],
    ]
# this should be extended
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
    'token': when_token,
    'string': when_string,
    'escape': when_escape
    }

def test_entry(char, state):
    if state not in trans_table:
        raise Exception('Error: current state '+state+' not in trans_table')
    when = trans_table[state]
    for entry in when:
        # print(entry)
        cond = entry[0]
        # print(cond)
        if cond(char):
            return entry
    return None

def token2num(token):
    if token[0].isdigit():
        if '.' in token:
            token = float(token)
        else:
            token = int(token)
    return token
'''
consume a char, and build, but it can not build tree 
pre-condition:
    1. char + code = old_code
'''
def consume(char, state, ast, code, liter, level, pos):
    # print('consume '+char+' -|- '+code+'----'+str(level))
    entry = test_entry(char, state)
    if entry is None:
        raise Exception('current state '+state+', char: '+char)
    next_state = entry[1]
    print(next_state)
    if next_state == 'error':
        raise Exception(str(pos)+': error state '+code)
    callback = entry[2]
    rs = callback(char, liter)
    print(rs)
    liter, token, error, cmd = None, None, None, None
    if len(rs) == 4:
        liter, token, error, cmd = rs
    else:
        liter, token, error = rs
    if error is not None:
        raise Exception(error)
    if token is not None:
        print(token)
        
        ast.append(token2num(token))
    if cmd == 'push':
        # print('push')
        _, sub_ast, code, _ = consume(code[0], 'normal', [], code[1:], '', level+1, pos+1)
        if len(sub_ast) > 0:
            ast.append(sub_ast)
    elif cmd == 'pop':
        # print('pop '+str(level)+' '+code)
        if len(code) > 0 and level <= 0:
            raise Exception('code left "'+code+'"')
        return next_state, ast, code, liter
    elif cmd is not None:
        raise Exception('unknown command '+cmd)
    if len(code) == 0:
        if len(liter) > 0:
            if next_state == 'token':
                ast.append(token2num(liter))
            else:
                raise Exception('error '+next_state)
        return 'end', ast, code, liter
    return consume(code[0], next_state, ast, code[1:], liter, level, pos+1)

def scan_code(code):
    ast = []
    state = 'normal'
    liter = ''
    code = code.strip()
    state, ast, code, liter = consume(code[0], state, ast, code[1:], liter, 0, 0)
    return ast
