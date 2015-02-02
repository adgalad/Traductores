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
	'''program : PROGRAM LCURLY instructionType RCURLY
	 		   | PROGRAM LCURLY RCURLY'''
	p[0] = Program(p[1])

def p_instructionType(p):
	''' instructionType : LCURLY instructionBlock RCURLY SEMICOLON
						| instruction''' 										
	
# al hacer declaraciones deberia poder asignarles un valor tambien a las variables, o no? (no hay ningun ejemplo asi)
def p_declarationBlock(p):
	'''declarationBlock : types id SEMICOLON 
			   			| types id SEMICOLON declarationBlock'''
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
	'''instruction : USING declarationBlock IN instructionBlock
				   | IDENTIFIER ASSIGN expression
				   | ifInst
  				   | printOutput
  				   '''
#  				   | whileInst 
#  				   | repeatInst 
#  				   | forInst 
#  				   | scanInst
  	p[0] = p[1]

# la instruccion (expression debe ser de tipo bool)
def p_ifInst(p):
	'''ifInst : IF LPAREN expression RPAREN instructionType
			  | IF LPAREN expression RPAREN instructionType ELSE instructionType'''

# poner {1,2,3} lo acepta como id? si es asi, desps de direction va una sola regla con IDENTIFIER.
def p_forInst(p):
	'''forInst : FOR IDENTIFIER direction IDENTIFIER DO instructionType
			   | FOR IDENTIFIER direction LCURLY IDENTIFIER RCURLY DO instructionType'''

def p_direction(p):
	''' direction : MIN
				  |	MAX'''

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
                | LPAREN binaryOp RPAREN
                | TRUE
                | FALSE              
                | number'''
    p[0] = BinaryOp(p[1],p[2],p[3])

def p_number(p):
    '''number : NUMBER'''
    p[0] = Number(p[1])

# Error rule for syntax errors
def p_error(p):
    print p
    print "Syntax error in input"