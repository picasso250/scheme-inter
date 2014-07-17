import logger

log = logger.Log()
log.debug_ = True

# key: cur_state
# value: cur_char, next_state, callback(char, literal) => (literal, token, ErrorMessage)

when_normal = [
    [lambda c: c == '(', 'normal', lambda c, i: (None, [{'type': 'left parenthesis'}], None)],
    [lambda c: c == ')', 'normal', lambda c, i: (None, [{'type': 'right parenthesis'}], None)],
    [lambda c: c.isspace(), 'normal', lambda c, i: (None, None, None)],
    [lambda c: c == '"', 'string', lambda c, i: ('', None, None)],
    [lambda c: True, 'token', lambda c, i: (c, None, None)],
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

'''scan'''
def scan_code(code):
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
