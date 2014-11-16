import logging
from struct import *

class Tree(object):
    """docstring for Tree"""
    def __init__(self):
        super(Tree, self).__init__()
        self.left = None
        self.right = None

class Parser(object):
    """docstring for Parser"""
    def __init__(self, token_list):
        super(Parser, self).__init__()
        self.token_list = token_list
        self.ast = None
    def parse(self):
        for token in token_list:
            if isinstance(token, Token):
                if token.token == '(':
                    self.start_list()
                elif token.token == ')':
                    self.end_list()
                elif token.token == '.':
                    self.one_right()
                else:
                    self.token = self.parse_token(token)
                    self.on_token()
            elif isinstance(token, Comment):
                pass
                    
    def on_token(self):
        if isinstance(self.ast, Tree):
            self.ast.left = self.token
        else:
            self.ast = self.token
        
