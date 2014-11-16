
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
