
import scanner

code = '(+ 137 349)'
code = '(+ 137 349 (- 2 1))'
print(code)
ast = scanner.scan_code(code)
print(ast)
