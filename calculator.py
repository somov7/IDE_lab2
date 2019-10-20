import sys


class Parser:
    def parse(self, expr):
        tokens = []
        currentlyNumber = False
        number = 0
        for c in expr:
            if '0' <= c and c <= '9':
                if currentlyNumber:
                    number += c
                else:
                    currentlyNumber = True
                    number = c
                continue
            elif currentlyNumber:
                currentlyNumber = False
                tokens.append(int(number, 10))
            if c in "+-*/()":
                tokens.append(c)
            elif c == ' ':
                continue
            else:
                return False
        if currentlyNumber:
            tokens.append(int(number, 10))
        prev_token = '('
        for i in range(len(tokens)):
            if isinstance(prev_token, str):
                if prev_token == '(' and tokens[i] == ')':
                    return False
                if prev_token in "(+-*/":
                    if tokens[i] == '+':
                        tokens[i] = '#'
                    elif tokens[i] == '-':
                        tokens[i] = '_'
                elif prev_token in "#_":
                    if tokens[i] != "(" and not isinstance(tokens[i], int):
                        return False
            prev_token = tokens[i]
        return tokens

class Calculator:

    def shuntingYard(self, tokens):
        out = []
        operator = []
        for token in tokens:
            if isinstance(token, int):
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
            elif token in "#_":
                while operator and operator[-1] in "#_":
                    out.append(operator.pop())
                operator.append(token)
            elif token in "*/":    
                while operator and operator[-1] in "#_*/":
                    out.append(operator.pop())
                operator.append(token)
            elif token in "+-":    
                while operator and operator[-1] in "#_*/+-":
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
            if isinstance(token, int):
                stack.append(token)
            elif token in "#_":
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
        if len(stack) != 1 or not isinstance(stack[0], int):
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
            return first // second
        elif operation == '#':
            return first
        elif operation == '_':
            return -first
        else:
            return False