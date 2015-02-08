# -*- coding: utf-8 -*-

import sys
import ply.lex  as lex
import ply.yacc as yacc
from   lexer    import tokens, findColumn
from   AST      import *

# Precedencia de operadores (de menor a mayor)
precedence = (
    ('right','RPAREN'),
    ('right','ELSE'),

    # Booleanos
    ('left','OR'),
    ('left','AND'),
    ('right','NOT'),

    # Comparativos
    ('nonassoc', 'LESSTHAN', 'GREATERTHAN', 'LESSEQUALTHAN', 'GREATEREQUALTHAN'),
    ('nonassoc', 'EQUALS', 'NOTEQUALS'),
    ('nonassoc', 'BELONGSTO'),  # no se si este esta bien aqui

    # Aritméticos
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULE'),
    
    # Conjuntos
    ('left', 'SETUNION', 'SETDIFF'),							# ¿s = s + {i * 2}; # unión de conjuntos? No es ++??
    ('left','SETINTERSECT'),
    
    # Conjuntos aritméticos
    ('left','SETMAPPLUS','SETMAPMINUS'),						# tiene mayor precedencia sobre la union...
    ('left', 'SETMAPTIMES', 'SETMAPDIVIDE', 'SETMAPMODULE'),

    # Unarios
    ('right','SETMINVALUE','SETMAXVALUE','SETSIZE','NEGATE'),
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
    if (len(p)==2):
        p[0] = Instruction(p[1])
    else:
        p[0] = Instruction("",p[1],p[2],p[3])


def p_block(p):
    '''block : LCURLY usingInInst RCURLY 
             | LCURLY instructionBlock RCURLY'''
    p[0] = Block(p[1],p[2],p[3])

def p_usingInInst(p):
    '''usingInInst : USING declarationBlock IN instructionBlock'''
    p[0] = UsingInInst(p[1],p[2],p[3],p[4])

def p_declarationBlock(p):
    '''declarationBlock : type id SEMICOLON declarationBlock
			   			| type id SEMICOLON'''
    if len(p) == 5:
        p[0] = DeclarationBlock(p[1],p[2],p[3],p[4])
    else:
        p[0] = DeclarationBlock(p[1],p[2],p[3],"")

def p_type(p):
    '''type : INT 
  			| BOOL 
  			| SET'''
    p[0] = Type(p[1])

def p_identifier(p):
    '''identifier : IDENTIFIER'''
    p[0] = ID(p[1])

def p_id(p):
    '''id : IDENTIFIER COMMA id
		  | IDENTIFIER'''
    if len(p) == 4:
        p[0] = ID(p[1],p[2],p[3])
    else:
        p[0] = ID(p[1])

# indica que estoy dentro de un bloque de instrucciones y por ello las inst llevan ;
def p_instructionBlock(p):
    '''instructionBlock : instruction SEMICOLON instructionBlock
                        |'''
    if len(p) == 3:
        p[0] = InstructionBlock(p[1],p[2])
    elif len(p) == 4:
        p[0] = InstructionBlock(p[1],p[2],p[3])
    elif len(p) == 1:
        p[0] = InstructionBlock()

def p_ifInst(p):
    '''ifInst : IF LPAREN expression RPAREN instruction
			  | IF LPAREN expression RPAREN instruction ELSE instruction '''
    if len(p) == 6:
        p[0] = IfInst(p[1],p[2],p[3],p[4],p[5])
    else:
        p[0] = IfInst(p[1],p[2],p[3],p[4],p[5],p[6],p[7])

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
    if len(p) == 7:
        p[0] = WhileInst(p[1],p[2],p[3],p[4],p[5],p[6])
    else:
        p[0] = WhileInst(p[1],p[2],p[3],p[4])

def p_repeatInst(p):
    '''repeatInst : REPEAT instruction whileInst'''
    p[0] = RepeatInst(p[1],p[2],p[3])

def p_scanInst(p):
    '''scanInst : SCAN expression'''
    p[0] = ScanInst(p[1],p[2])

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
    '''string : STRING'''
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
	                | SETMINVALUE expression
	                | SETMAXVALUE expression
	                | SETSIZE expression
                  | MINUS expression %prec NEGATE
                  | LPAREN expression RPAREN
                  | booleanValue          
                  | identifier 
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
    p[0] = Set(p[1],p[2],p[3])

def p_setNumbers(p):
    '''setNumbers : expression COMMA setNumbers
			      | expression'''
    if len(p) == 2:
        p[0] = SetNumbers(p[1])
    else:
        p[0] = SetNumbers(p[1],p[2],p[3])

def p_booleanValue(p):
    ''' booleanValue : TRUE 
                     | FALSE '''
    p[0] = BooleanValue(p[1])

def p_number(p):
    '''number : NUMBER'''
    p[0] = Number(p[1])

def p_error(p):
    if p:
        yaccError.append('''ERROR: Se encontró un token inesperado "%s" en la Línea %d, Columna %d.''' \
            % (p.value, p.lineno/2, findColumn(p.lexer.lexdata,p)))
    else:
        yaccError.append('''ERROR: Error de sintaxis en fin de archivo.''')


parser = yacc.yacc()
yaccError = []