# -*- coding: utf-8 -*-

import ply.yacc as yacc
from tokens import *

class SyntacticalAnalyzer:

    class Expr: pass

    class BinaryOp(Expr):
        def __init__(self,left,op,right):
            self.type = "binaryOp"
            self.left = left
            self.right = right
            self.op = op

    class Number(Expr):
        def __init__(self,value):
            self.type = "number"
            self.value = value

    def p_expression_binaryOp(p):
        '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
        p[0] = BinaryOp(p[1],p[2],p[3])

    def p_expression_number(p):
        'expression : NUMBER'
        p[0] = Number(p[1])

    def __init__(self):
        self.yacc = yacc.yacc(module=self)