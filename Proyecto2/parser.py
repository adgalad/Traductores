# -*- coding: utf-8 -*-

import ply.lex as lex
import ply.yacc as yacc
from lexer import tokens

# Precedencia, de menor a mayor
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

class Number:
    def __init__(self,value):
        self.type = "number"
        self.value = value

    def getValue(self):
        return self.value

def p_number(p):
    'number : NUMBER'
    p[0] = Number(p[1])


# def p_expression(p):
#     '''expression : binaryOp'''
#     p[0] = p[1]

class BinaryOp:
    def __init__(self,left,op,right):
        self.type = "binaryOp"
        self.left = left
        self.right = right
        self.op = op

    def getValue(self):
        if op == '+':
            return left + right

def p_binaryOp(p):
    '''binaryOp : binaryOp PLUS binaryOp
                | binaryOp MINUS binaryOp
                | binaryOp TIMES binaryOp
                | binaryOp DIVIDE binaryOp
                | binaryOp MODULE binaryOp
                | binaryOp AND binaryOp
                | binaryOp OR binaryOp
                | LBRACKET binaryOp RBRACKET
                | TRUE
                | FALSE              
                | NUMBER'''
    p[0] = self.BinaryOp(p[1],p[2],p[3])
#     print(p[0])
#     if len(p) == 4:
#         if p[2] == '+':
#             p[0] = p[1] + p[3]
#         elif p[2] == '-':
#             p[0] = p[1] - p[3]
#         elif p[2] == '*':
#             p[0] = p[1] * p[3]
#         elif p[2] == '/':
#             p[0] = p[1] / p[3]

    

# Error rule for syntax errors
def p_error(p):
    print p
    print "Syntax error in input"