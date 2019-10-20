import sys
import math

class Parser:
    def parse(self, expr):
        tokens = []
        functions = ['sin', 'cos'] 
        currentlyNumber = False
        currentlyFrac = False
        currentlyFunc = False
        number = 0
        func = ''
        for c in expr:
            if currentlyNumber and c not in '0123456789.':
                currentlyNumber = False
                currentlyFrac = False
                tokens.append(float(number))
            elif currentlyFunc and not ('a' <= c and c <= 'z'):
                if func in functions:
                    tokens.append(func[0])
                    currentlyFunc = False
                else:
                    return False
            if ('0' <= c and c <= '9') or c == '.':
                if c == '.':
                    if currentlyFrac is False:
                        currentlyFrac = True
                    else:
                        return False
                if currentlyNumber:
                    number += c
                else:
                    currentlyNumber = True
                    number = c
                continue
            elif 'a' <= c and c <= 'z':
                if currentlyFunc:
                    func += c
                else:
                    currentlyFunc = True
                    func = c
            elif c in "+-*/()":
                tokens.append(c)
            elif c == ' ':
                continue
            else:
                return False
        if currentlyNumber:
            tokens.append(float(number))
        prev_token = '('
        for i in range(len(tokens)):
            if isinstance(prev_token, str):
                if prev_token == '(' and tokens[i] == ')':
                    return False
                if prev_token in "(+-*/sc":
                    if tokens[i] == '+':
                        tokens[i] = '#'
                    elif tokens[i] == '-':
                        tokens[i] = '_'
                elif prev_token in "#_":
                    if tokens[i] != "(" and not isinstance(tokens[i], float):
                        return False
            prev_token = tokens[i]
        return tokens

class Calculator:
    def shuntingYard(self, tokens):
        out = []
        operator = []
        for token in tokens:
            if isinstance(token, float):
                out.append(token)
            elif token == '(':
                operator.append(token)
            elif token == ')':
                while operator and operator[-1] != '(':
                    out.append(operator.pop())
                if(len(operator) == 0):
                    return False
                else:
                    operator.pop()
            elif token in "sc":
                operator.append(token)
            elif token in "#_":
                while operator and operator[-1] in "#_sc":
                    out.append(operator.pop())
                operator.append(token)
            elif token in "*/":    
                while operator and operator[-1] in "#_*/sc":
                    out.append(operator.pop())
                operator.append(token)
            elif token in "+-":    
                while operator and operator[-1] in "#_*/+-sc":
                    out.append(operator.pop())
                operator.append(token)     
        while operator:
            out.append(operator.pop())
        return out

    def calculate(self, string, postfix = False):
        queue = Parser().parse(string)
        if queue is False:
            return False
        if postfix is False:
            queue = self.shuntingYard(queue)
        if queue is False:
            return False
        stack = []
        for token in queue:
            if token is False:
                return False
            if isinstance(token, float):
                stack.append(token)
            elif token in "#_sc":
                if stack:
                    first = stack.pop()
                else:
                    return False
                stack.append(self.evaluate(token, first))
            else:
                if stack:
                    second = stack.pop()
                else:
                    return False
                if stack:
                    first = stack.pop()
                else:
                    return False
                stack.append(self.evaluate(token, first, second))
        if len(stack) != 1 or not isinstance(stack[0], float):
            return False
        else:
            return stack[0]

    def evaluate(self, operation, first, second = 0):
        if operation == '+':
            return first + second
        elif operation == '-':
            return first - second
        elif operation == '*':
            return first * second
        elif operation == '/':
            return first / second
        elif operation == '#':
            return first
        elif operation == '_':
            return -first
        elif operation == 's':
            return math.sin(first)
        elif operation == 'c':
            return math.cos(first)
        else:
            return False