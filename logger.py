class Log(object):
    """docstring for Log"""
    def __init__(self):
        super(Log, self).__init__()
        self.debug_ = True
    
    def debug(self, *arg):
        if self.debug_:
            print(*arg)
