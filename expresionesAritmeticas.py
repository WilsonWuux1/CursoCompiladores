import re

def evaluate_expression(expression):
    
    try:
        
        correct = True
        result = eval(expression)
    except (SyntaxError, ZeroDivisionError, NameError):
        
        correct = False
        result = None
    
    return correct, result

expressions = ["1 + 3 * 5 - 2", "1 + 3 *", "/ 5"]
evaluation_results = [evaluate_expression(expr) for expr in expressions]

print(evaluation_results)