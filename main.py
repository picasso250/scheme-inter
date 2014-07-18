
from scheme import evalue_code

#evalue_code('3')

code = '(+ 137 349)';
if True:
    evalue_code(code)
evalue_code('(define size 2)')

#evalue_code('(define (square x) (* x x))')
# evalue_code('(square 21)')
# evalue_code('(square (+ 2 5))')
# evalue_code('(square (square 3))')

if False:
    evalue_code('''
    (define (sum-of-squares x y)
      (+ (square x) (square y)))''')
    # evalue_code('(sum-of-squares 3 4)')

    evalue_code('''
    (define (f a)
      (sum-of-squares (+ a 1) (* a 2)))
    (f 5)''')
