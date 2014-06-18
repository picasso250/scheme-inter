
from scheme import evalue_code

code = '(+ 137 349)';

statement = {
    'oper': {
        'type': 'lambda',
        'name': '+'
        },
    'params': [
        {
            'type': 'number',
            'value': 137
            },
        {
            'type': 'number',
            'value': 349
            }
        ]
    }
#ast = [statement]
#tokens = token(code)
#print('tokens', tokens)
#ast = grammer(tokens)
#print ('ast', ast)
#val = evalue(ast)
#print(val)

evalue_code('(define (square x) (* x x))')
# evalue_code('(square 21)')
# evalue_code('(square (+ 2 5))')
# evalue_code('(square (square 3))')

evalue_code('''
(define (sum-of-squares x y)
  (+ (square x) (square y)))''')
# evalue_code('(sum-of-squares 3 4)')

evalue_code('''
(define (f a)
  (sum-of-squares (+ a 1) (* a 2)))
(f 5)''')
