import logger

log = logger.Log()
log.debug_ = True

class Tree(object):
    """docstring for Tree"""
    def __init__(self):
        super(Tree, self).__init__()
        self.left = None
        self.right = None

class Token(object):
    """docstring for Token"""
    def __init__(self, token):
        super(Token, self).__init__()
        self.token = token
        
class Number(object):
    """docstring for Number"""
    def __init__(self, value):
        super(Number, self).__init__()
        self.value = value

class String(object):
    """docstring for String"""
    def __init__(self, text):
        super(String, self).__init__()
        self.text = text

def parse_token(liter):
    return Token(liter)

# key: cur_state
# value: cur_char, next_state, callback
# callback(char, literal) => (literal, token_list, ErrorMessage, cmd)
# cmd=push|pop

when_normal = [
    [lambda c: c == '(', 'normal', lambda c, i: (None, None, None, 'push')],
    [lambda c: c == ')', 'normal', lambda c, i: (None, None, None, 'pop')],
    [lambda c: c.isspace(), 'normal', lambda c, i: (None, None, None)],
    [lambda c: c == '"', 'string', lambda c, i: ('', None, None)],
    [lambda c: True, 'token', lambda c, i: (c, None, None)],
]
when_token = [
    [lambda c: c.isalpha() or c.isdigit() or c in '.-_?<>', 'token', lambda c, i: (i+c, None, None)],
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

def token2value(token):
    # complex todo
    if token[0].isdigit():
        if '.' in token:
            token = float(token)
        else:
            token = int(token)
    elif token[0] == '#':
        if len(token) != 2:
            raise Exception(token+' is not boolean')
        if token[1] == 't':
            return True
        elif token[1] == 'f':
            return False
        else:
            raise Exception(token+' is not boolean')
    return token

class Scanner(object):
    """docstring for Scanner"""
    def __init__(self):
        super(Scanner, self).__init__()

        self.ERROR = -1
        self.NORMAL = 1
        self.TOKEN = 2
        self.STRING = 3
        self.ESCAPE = 4

        _normal = [
            [lambda c: c == '(', self.NORMAL, self.start_list],
            [lambda c: c == ')', self.NORMAL, self.end_list],
            [lambda c: c.isspace(), self.NORMAL, self.do_nothing],
            [lambda c: c == '"', self.STRING, self.start_string],
            [lambda c: True, self.TOKEN, self.start_token],
        ]
        is_token_char = lambda c: c.isalpha() or c.isdigit() or c in '-_?<>'
        _token = [
            [is_token_char, self.TOKEN, self.on_token],
            [lambda c: c.isspace(), self.NORMAL, self.end_token],
            [lambda c: c == ')', self.NORMAL, self.end_list],
            [lambda c: True, self.ERROR, self.do_nothing],
        ]
        _string = [
            [lambda c: c == '"', self.NORMAL, self.end_string],
            [lambda c: c == '\\', self.ESCAPE, self.do_nothing],
            [lambda c: True, self.STRING, self.on_string],
        ]
        _escape = [
            [lambda c: True, self.STRING, self.on_escape],
        ]
        self.trans_table = {
            self.NORMAL: _normal,
            self.TOKEN: _token,
            self.STRING: _string,
            self.ESCAPE: _escape,
        }
        self.escape_table = escape_table
        self.char = None
        self.cur_list = None
        self.stack = []
        self.is_right = False

    def scan(self, code):
        self.state = self.NORMAL
        self.token_list_tree = None
        self.ast = None
        for c in code:
            self.eat_char(c)
        return ast

    def match(self, char, test):
        return test(char)

    def eat_char(self, c):
        self.char = c
        print('current char', c)
        for e in self.trans_table[self.state]:
            if self.match(c, e[0]):
                next_state = e[1]
                e[2]()
                break
    
    def do_nothing(self):
        pass

    def start_list(self):
        print('start list')
        if self.cur_list is not None:
            self.stack.append(self.cur_list)
        self.cur_list = []

    def end_list(self):
        print('end list')
        _list = self.cur_list
        self.cur_list = self.stack.pop()
        self.cur_list.right = _list

    def start_token(self):
        print('start token', self.char)
        self.cur_token = ''
        self.on_token()

    def on_token(self):
        self.cur_token += self.char

    def end_token(self):
        print('end token',self.cur_token)
        self.cur_list.append(Token(self.cur_token))
        print(self.cur_list)

    def start_string(self):
        self.cur_string = ''

    def on_string(self):
        self.cur_string += self.char

    def end_string(self):
        self.cur_list.append(String(self.cur_string))

    def on_escape(self):
        c = self.char
        if self.char in self.escape_table:
            c = self.escape_table[self.char]
        self.cur_string += c

class Translator(object):
    """docstring for Translator"""
    def __init__(self, token_list_tree):
        super(Translator, self).__init__()
        self.token_list_tree = token_list_tree
        self.is_right = False
        self.cur_tree = None
        self.stack = []

    def translate(self):
        if isinstance(t, list):
            return self.eat_list(t)
        if isinstance(t, Token):
            return self.trans_token(t)
        return t

    def eat_list(self, lst):
        if len(lst) == 0:
            return Tree()
        root = None
        last_tree = None
        for t in lst:
            if isinstance(t, Token):
                if self.is_dot(Token):
                    assert not self.is_right, 'there are 2 dots'
                    assert root is not None
                    assert last_tree is not None
                    self.is_right = True
                    continue
                t = self.trans_token(t)
            if self.is_right:
                assert last_tree is not None
                assert last_tree.right is None, 'right most more than one'
                last_tree.right = t
            else:
                tree = Tree
                tree.left = t
                if root is None:
                    root = tree
                if last_tree:
                    last_tree.right = tree
                last_tree = tree
        
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
    # print(next_state)
    if next_state == 'error':
        raise Exception(str(pos)+': error state '+code)
    callback = entry[2]
    rs = callback(char, liter)
    # print(rs)
    liter, token, error, cmd = None, None, None, None
    if len(rs) == 4:
        liter, token, error, cmd = rs
    else:
        liter, token, error = rs
    if error is not None:
        raise Exception(error)
    if token is not None:
        # print(token)
        ast.append(token2value(token))
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
        if liter is not None and len(liter) > 0:
            if next_state == 'token':
                ast.append(token2value(liter))
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

if __name__ == '__main__':
    Scanner().scan('(1 2 3)')
    print('test')
