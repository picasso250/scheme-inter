
from scheme import evalue_code, log
import glob

log.debug_ = False
  
def equal(result, expected):
    if str(result) != expected:
        float_output = expected+'.0'
        if str(result) == float_output:
            print('Warn, it shoud be int, not float', expected)
            return True
        else:
            return False
    return True

def test():

    file_list = glob.iglob(r'test/*.code')

    for f in file_list:
        fh = open(f)
        ofh = open(f+'.output')
        for code in fh.readlines():
            print('code', code)
            rs = evalue_code(code)
            print('result', rs)
            output = ofh.readline().strip()
            if not equal(rs, output):
                print('Error, result', rs, 'expected', output)
                return False

    file_list = glob.iglob(r'test/*.sc')

    for f in file_list:
        fh = open(f)
        ofh = open(f+'.output')
        code = fh.read()
        print('code', code)
        rs = evalue_code(code)
        print('result', rs)
        output = ofh.readline().strip()
        if not equal(rs, output):
            print('Error, result', rs, 'expected', output)
            return False
    return True

if not test():
    print('Fail!')
else:
    print('Pass!')


