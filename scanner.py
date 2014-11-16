import logger
import logging

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

    def __repr__(self):
        return "<{}>".format(self.token)
        
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

    def __repr__(self):
        return '"{}"'.format(self.text)
class Comment(object):
    """docstring for Comment"""
    def __init__(self, text):
        super(Comment, self).__init__()
        self.text = text
    def __repr__(self):
        return ';{}'.format(self.text)

def parse_token(liter):
    return Token(liter)

# this should be extended
escape_table = {
    'n': "\n",
    'r': "\r",
    't': "\t",
    'v': "\v",
}

class Scanner(object):
    """docstring for Scanner"""
    def __init__(self):
        super(Scanner, self).__init__()

        self.ERROR = -1
        self.NORMAL = 1
        self.TOKEN = 2
        self.STRING = 3
        self.ESCAPE = 4
        self.COMMENT = 5

        _normal = [
            [lambda c: c in '()', self.NORMAL, self.one_token],
            [lambda c: c.isspace(), self.NORMAL, self.do_nothing],
            [lambda c: c == '"', self.STRING, self.start_string],
            [lambda c: c == ';', self.COMMENT, self.start_comment],
            [lambda c: True, self.TOKEN, self.start_token],
        ]
        is_token_char = lambda c: c.isalpha() or c.isdigit() or c in '.-_?<>!'
        _token = [
            [is_token_char, self.TOKEN, self.on_token],
            [lambda c: c.isspace(), self.NORMAL, self.end_token],
            [lambda c: c == ')', self.NORMAL, [self.end_token, self.one_token]],
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
        _comment = [
            [lambda c: c == '\n', self.NORMAL, self.end_comment],
            [lambda c: True, self.COMMENT, self.on_comment],
        ]
        self.trans_table = {
            self.NORMAL: _normal,
            self.TOKEN: _token,
            self.STRING: _string,
            self.ESCAPE: _escape,
            self.COMMENT: _comment,
        }
        self.escape_table = escape_table
        self.char = None
        self.token_list = []

    def scan(self, code):
        self.state = self.NORMAL
        self.token_list_tree = None
        self.ast = None
        for c in code:
            self.eat_char(c)
        if self.token_list:
            return self.token_list
        assert False

    def match(self, char, test):
        return test(char)

    def eat_char(self, c):
        self.char = c
        logging.debug('current char %s', c)
        for e in self.trans_table[self.state]:
            if self.match(c, e[0]):
                next_state = e[1]
                self.do_callback(e[2])
                self.state = next_state
                break

    def do_callback(self, callback):
        if isinstance(callback, list):
            for cb in callback:
                cb()
        else:
            callback()

    def do_nothing(self):
        pass

    def one_token(self):
        self.cur_token = self.char
        self.end_token()

    def start_token(self):
        self.cur_token = ''
        self.on_token()

    def on_token(self):
        self.cur_token += self.char

    def end_token(self):
        self.token_list.append(Token(self.cur_token))

    def start_string(self):
        self.cur_string = ''

    def on_string(self):
        self.cur_string += self.char

    def end_string(self):
        self.token_list.append(String(self.cur_string))

    def start_comment(self):
        self.cur_comment = ''

    def on_comment(self):
        self.cur_comment += self.char

    def end_comment(self):
        self.token_list.append(Comment(self.cur_comment))

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
        

if __name__ == '__main__':
    print('test')
    print(Scanner().scan('(1 2 3)'))
    print(Scanner().scan('((1 2) 3)'))
    print(Scanner().scan('("abc" 3)'))
    print(Scanner().scan('("a\tbc" 3)'))
    print(Scanner().scan('("a\\tbc" 3)'))
    print(Scanner().scan(';xxx\n("a\\tbc" 3)'))
