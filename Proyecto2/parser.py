# -*- coding: utf-8 -*-

import ply.lex  as lex
import ply.yacc as yacc
from   lexer    import tokens
from   AST      import *

# Precedencia de operadores (de menor a mayor)
precedence = (
	('right','RPAREN'),
	('right','ELSE'),

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
	('left','SETMINVALUE','SETMAXVALUE','SETSIZE'),
)

def p_program(p):
    '''program : PROGRAM instruction'''
    p[0] = Program(p[1],p[2])

def p_instruction(p):
    '''instruction : block
                   | ifInst
                   | forInst 
                   | whileInst 
                   | repeatInst 
                   | scanInst
                   | printInst
                   | id ASSIGN expression'''
    #print "instruction"
    if (len(p)==2):
        p[0] = Instruction(p[1])
    else:
        p[0] = Instruction("",p[1],p[2],p[3])


def p_block(p):
    ''' block : LCURLY usingInInst RCURLY 
              | LCURLY instructionBlock RCURLY'''
    #print "block"
    p[0] = Block(p[1],p[2],p[3])

def p_usingInInst(p):
    '''usingInInst : USING declarationBlock IN instructionBlock'''
    p[0] = UsingInInst(p[1],p[2],p[3],p[4])

# al hacer declaraciones deberia poder asignarles un valor tambien a las variables, o no? (no hay ningun ejemplo asi)
def p_declarationBlock(p):
    '''declarationBlock : type id SEMICOLON declarationBlock
			   			| type id SEMICOLON'''
    if len(p) == 5:
        p[0] = DeclarationBlokc(p[1],p[2],p[3],p[4])
    else:
        p[0] = DeclarationBlokc(p[1],p[2],p[3],"")

def p_type(p):
    '''type : INT 
  			 | BOOL 
  			 | SET'''
    p[0] = Type(p[1])

def p_id(p):
    '''id : IDENTIFIER COMMA id
		  | IDENTIFIER'''
    if len(p) == 4:
        p[0] = ID(p[1],p[2],p[3])
    else:
        p[0] = ID(p[1])


# total de instrucciones dentro de un bloque de instrucciones (internas)    
# indica que estoy dentro de un bloque de instrucciones y por ellos las inst llevan ;
def p_instructionBlock(p):
    '''instructionBlock : instruction SEMICOLON instructionBlock
                        |'''
    #print "instructionBlock"
    if len(p) == 3:
        p[0] = InstructionBlock(p[1],p[2])
    elif len(p) == 4:
        p[0] = InstructionBlock(p[1],p[2],p[3])
    elif len(p) == 1:
        p[0] = InstructionBlock()

def p_ifInst(p):
    '''ifInst : IF LPAREN expression RPAREN instruction
			  | IF LPAREN expression RPAREN instruction ELSE instruction '''
	#p[0] = IfInst()

# poner {1,2,3} lo acepta como id? si es asi, desps de direction va una sola regla con IDENTIFIER.
def p_forInst(p):
    '''forInst : FOR expression direction expression DO instruction'''
    p[0] = ForInst(p[1],p[2],p[3],p[4],p[5],p[6])

def p_direction(p):
    '''direction : MIN
				 | MAX'''
    p[0] = Direction(p[1])

def p_whileInst(p):
    '''whileInst : WHILE LPAREN expression RPAREN DO instruction
				 | WHILE LPAREN expression RPAREN'''
    print "\n\n\n\n\n\nsdasasdas\n\n\n\n\n\n\n"
    if len(p) == 7:
        p[0] = WhileInst(p[1],p[2],p[3],p[4],p[5],p[6])
    else:
        p[0] = WhileInst(p[1],p[2],p[3],p[4])

def p_repeatInst(p):
    '''repeatInst : REPEAT instruction whileInst'''
    p[0] = RepeatInst(p[1],p[2],p[3])

def p_scanInst(p):
	'''scanInst : SCAN expression'''


def p_printInst(p):
    '''printInst : PRINT outputType
				 | PRINTLN outputType'''
    p[0] = PrintInst(p[1],p[2])


def p_outputType(p):
    '''outputType : expression COMMA outputType
				  | expression
                  | string COMMA outputType
                  | string'''
    if (len(p) == 2):
        p[0] = OutputType(p[1])
    else:
        p[0] = OutputType(p[1],p[2],p[3])


def p_string(p):
    ''' string : STRING '''
    p[0] = String(p[1])

def p_expression(p):
    '''expression : expression PLUS expression
                | expression MINUS expression
                | expression TIMES expression
                | expression DIVIDE expression
                | expression MODULE expression
                | expression AND expression
                | expression OR expression
                | expression LESSTHAN expression
                | expression LESSEQUALTHAN expression
                | expression GREATERTHAN expression
                | expression GREATEREQUALTHAN expression
                | expression EQUALS expression
                | expression NOTEQUALS expression
                | expression SETUNION expression
                | expression SETDIFF expression
                | expression SETINTERSECT expression
                | expression SETMAPPLUS expression
                | expression SETMAPMINUS expression
                | expression SETMAPTIMES expression
                | expression SETMAPDIVIDE expression
                | expression SETMAPMODULE expression
                | expression BELONGSTO expression
                | NOT expression
                | MINUS expression
	            | SETMINVALUE expression
	            | SETMAXVALUE expression
	            | SETSIZE expression
                | LPAREN expression RPAREN
                | TRUE
                | FALSE              
                | id 
                | set
                | number'''
    if len(p) == 2:
    	p[0] = Expression(p[1])
    elif len(p) == 3:
    	p[0] = Expression(p[2],p[1])
    else:
    	p[0] = Expression(p[1],p[2],p[3])

def p_set(p):
    '''set : LCURLY setNumbers RCURLY'''

def p_setNumbers(p):
	'''setNumbers : expression COMMA setNumbers
			      | '''

def p_number(p):
    '''number : NUMBER'''
    p[0] = Number(p[1])

def p_error(p):
    print p
    print "Syntax error in input"
