
import scanner

code = '(+ 137 349)'
code = '(+ 137 349 (- 2 1))'
#code = '(+ 137 349 (- 2 1)))' # error
code = '3'
code = '3 4'
code = '(define pi 3) pi'
code = '(+ 2.7 10)'
code = '#t'
code = '#f'
if False:
    code ='''
(define (eval exp env)
  (cond ((self-evaluating? exp) exp)
        ((variable? exp) (lookup-variable-value exp env))
        ((quoted? exp) (text-of-quotation exp))
        ((assignment? exp) (eval-assignment exp env))
        ((definition? exp) (eval-definition exp env))
        ((if? exp) (eval-if exp env))
        ((lambda? exp)
         (make-procedure (lambda-parameters exp)
                         (lambda-body exp)
                         env))
        ((begin? exp) 
         (eval-sequence (begin-actions exp) env))
        ((cond? exp) (eval (cond->if exp) env))
        ((application? exp)
         (apply (eval (operator exp) env)
                (list-of-values (operands exp) env)))
        (else
         (error "Unknown expression type -- EVAL" exp))))
         '''
print(code)
ast = scanner.scan_code(code)
print(ast)
