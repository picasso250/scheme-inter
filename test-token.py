
import scanner

code = '(+ 137 349)'
code = '(+ 137 349 (- 2 1))'
code = '(+ 137 349 (- 2 1)))' # error
print(code)
ast = scanner.scan_code(code)
print(ast)
