
from scheme import evalue_code
import glob  
  
def equal(result, expected):
    if str(rs) != output:
        float_output = output+'.0'
        print(str(rs), float_output)
        if str(rs) == float_output:
            print('Warn, it shoud be int, not float', output)
            return True
        else:
            return False
    return True

file_list = glob.iglob(r'test/*.code')

for f in file_list:
    fh = open(f)
    ofh = open(f+'.output')
    for code in fh.readlines():
        print(code)
        rs = evalue_code(code)
        print(rs)
        output = ofh.readline().strip()
        print(str(rs), output)
        if not equal(rs, output):
            print('Error, result', rs, 'expected', output)
            break

#evalue_code('(+ (* 3 (+ (* 2 4) (+ 3 5))) (+ (- 10 7) 6))')
# evalue_code('''(+ (* 3
#       (+ (* 2 4)
#          (+ 3 5)))
#    (+ (- 10 7)
#       6))''')

#evalue_code('(define size 2)')
#evalue_code('size')
#evalue_code('(* 5 size)')

#evalue_code('(define pi 3.14159)')
#evalue_code('(define radius 10)')
#evalue_code('(* pi (* radius radius))')
#evalue_code('(define circumference (* 2 pi radius))')
#evalue_code('circumference')

#evalue_code('''
#(* (+ 2 (* 4 6))
#   (+ 3 5 7))''')

# evalue_code('(define (square x) (* x x))')
#evalue_code('(square 21)')
#evalue_code('(square (+ 2 5))')
#evalue_code('(square (square 3))')

# evalue_code('''
# (define (sum-of-squares x y)
#   (+ (square x) (square y)))''')
# evalue_code('(sum-of-squares 3 4)')
