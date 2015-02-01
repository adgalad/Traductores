# -*- coding: utf-8 -*-

import ply.lex as lex
import ply.yacc as yacc
from lexer import tokens

# Precedencia, de menor a mayor
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

def p_program(p):
	'''program 	: PROGRAM LCURLY USING declarationList IN instructionList RCURLY
				| PROGRAM LCURLY USING declarationList RCURLY
				| PROGRAM LCURLY IN instructionList RCURLY
				| PROGRAM LCURLY RCURLY'''
	if len(p) == 8:
		p[0] = Program(p[4],p[6])
	elif len(p) == 6:
		if p[3] == 'USING':
			p[0] = Program(p[4],None)
		elif p[3] == 'IN':
			p[0] = Program(None,p[4])
	else:
		p[0] = Program(None,None)

class Program:
	def __init__(self,declarations=None,instructions=None):
		self.declarations = declarations
		self.instructions = instructions

	def getValue(self):
		return "reconocio un programa"

def p_declarationList(p):
	'''declarationList : types id declarationList
					   | types id SEMICOLON'''

def p_types(p):		# cambiar nombre
	'''types : INT 
  			 | BOOL 
  			 | SET'''
 	p[0] = p[1]

def p_id(p):
	'''id : IDENTIFIER
		  | IDENTIFIER COMMA id'''	
	p[0] = ID(p[1]);

def p_instructionList(p):
    '''instructionList : instruction 
    				   | instruction SEMICOLON instructionList'''

def p_instruction(p):
	'''instruction : ifInst'''
#  				   | whileInst 
#  				   | repeatInst 
#  				   | forInst 
#  				   | scanInst
#  				   | printInst 
#  				   | printlnInst'''
  	p[0] = p[1]

def p_ifInst(p):
	'''ifInst : IF expression SEMICOLON
			  | IF expression ELSE expression SEMICOLON 
			  | IF expression ELSE ifInst'''

class ID:
	def __init__(self,value):
		self.type = 'id'
		self.value = value

	def getValue(self):
		return self.value

class Number:
    def __init__(self,value):
        self.type = 'number'
        self.value = value

    def getValue(self):
        return self.value

def p_number(p):
    '''number : NUMBER'''
    p[0] = Number(p[1])


def p_expression(p):
	'''expression : binaryOp'''
	p[0] = p[1]

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