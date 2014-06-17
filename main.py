
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

#evalue_code('(+ 137 349)')

#evalue_code('(- 1000 334)')
#evalue_code('(* 5 99)')
#evalue_code('(/ 10 5)')
#evalue_code('(+ 2.7 10)')

#evalue_code('(+ 21 35 12 7)')
#evalue_code('(* 25 4 12)')

#evalue_code('(+ (* 3 5) (- 10 6))')

#evalue_code('(+ (* 3 (+ (* 2 4) (+ 3 5))) (+ (- 10 7) 6))')
# evalue_code('''(+ (* 3
#       (+ (* 2 4)
#          (+ 3 5)))
#    (+ (- 10 7)
#       6))''')

evalue_code('(define size 2)')
evalue_code('size')
