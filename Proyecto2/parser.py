# -*- coding: utf-8 -*-

import ply.lex as lex
import ply.yacc as yacc
from lexer import tokens
from AST import *

# Precedencia de operadores (de menor a mayor)
precedence = (
	# Booleanos
	('left','OR'),
	('left','AND'),
	('left','NOT'),

	# Comparativos
	('left', 'LESSTHAN', 'GREATERTHAN', 'LESSEQUALTHAN', 'GREATEREQUALTHAN'),
	('left', 'EQUALS', 'NOTEQUALS'),

	# Aritméticos
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULE'),
    
    # Conjuntos
    ('left', 'SETUNION', 'SETDIFF'),							# ¿s = s + {i * 2}; # unión de conjuntos? No es ++??
    ('left','SETINTERSECT'),
    
    # Conjuntos aritméticos
    ('left','SETMAPPLUS','SETMAPMINUS'),						# tiene mayor precedencia sobre la union...
    ('left', 'SETMAPTIMES', 'SETMAPDIVIDE', 'SETMAPMODULE'),
	('left', 'BELONGSTO'),	# no se si este esta bien aqui

	# Falta el menos unario
)

def p_program(p):
	'''program 	: PROGRAM LCURLY USING declarationBlock IN instructionBlock RCURLY
				| PROGRAM LCURLY USING declarationBlock RCURLY
				| PROGRAM LCURLY IN instructionBlock RCURLY
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

# al hacer declaraciones deberia poder asignarles un valor tambien a las variables, no?
def p_declarationBlock(p):
	'''declarationBlock : types id declarationBlock
					   	| types id SEMICOLON'''
	p[0] = p[1]

def p_types(p):		# cambiar nombre
	'''types : INT 
  			 | BOOL 
  			 | SET'''
 	p[0] = p[1]

def p_id(p):
	'''id : IDENTIFIER
		  | IDENTIFIER COMMA id'''	
	p[0] = ID(p[1]);

def p_instructionBlock(p):
    '''instructionBlock : instruction SEMICOLON
    				   	| instruction SEMICOLON instructionBlock'''
    p[0] = InstructionBlock(p[1],p[3])

def p_instruction(p):
	'''instruction : ifInst
  				   | printOutput'''
#  				   | whileInst 
#  				   | repeatInst 
#  				   | forInst 
#  				   | scanInst
  	p[0] = p[1]

# la instruccion (expression debe ser de tipo bool)
def p_ifInst(p):
	'''ifInst : IF expression instructionBlock
			  | IF expression ELSE instructionBlock 
			  | IF expression ELSE ifInst
  			  | IF expression LCURLY instructionBlock RCURLY
			  | IF expression LCURLY instructionBlock RCURLY ELSE LCURLY instructionBlock RCURLY
			  | IF expression LCURLY instructionBlock RCURLY ELSE ifInst'''

def p_printOutput(p):
	'''printOutput : PRINT outputType
				   | PRINTLN  outputType'''

# le faltan casos
def p_outputType(p):
	'''outputType : STRING
				  | expression'''

def p_expression(p):
	'''expression : binaryOp'''
	p[0] = p[1]

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
                | number'''
    p[0] = self.BinaryOp(p[1],p[2],p[3])

def p_number(p):
    '''number : NUMBER'''
    p[0] = Number(p[1])

# Error rule for syntax errors
def p_error(p):
    print p
    print "Syntax error in input"