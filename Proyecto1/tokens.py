
import ply.lex as lex
from ply.ctokens import t_COMMENT

reserved = {
    'if'    : 'IF',
    'else'  : 'ELSE',
    'elif'  : 'ELIF',
    'def'   : 'DEF',
    'class' : 'CLASS',
    'while' : 'WHILE',
    'for'   : 'FOR',
    'and'   : 'AND',
    'or'    : 'OR',
    'program' : 'PROGRAM',
    'in'    : 'IN',
    'using' : 'USING',
    'scan'  : 'SCAN',
    'print' : 'PRINT'
    }

tokens = [
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
   'PALABRA',
   'COMMENT'
] + list(reserved.values())

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_COMMENT = r'\#'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_PALABRA(t):
    r'\c+'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'

    if (reserved.get(t.value,'ID') != 'ID'):
        t.type = reserved.get(t.value,'ID')
    else:
        t.type = 'PALABRA'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'


def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)
