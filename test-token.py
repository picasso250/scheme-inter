
import scanner

code = '(+ 137 349)';
print(code)
ast = scanner.scan_code(code)
print(ast)
