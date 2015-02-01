# -*- coding: utf-8 -*-

import ply.lex as lex
from django.template.base import Lexer

error = False
output = ""
beginningOfLine = -1
reserved = {
    'program' : 'PROGRAM',
    'using'   : 'USING',
    'in'      : 'IN',
    'if'      : 'IF',
    'else'    : 'ELSE',
    'while'   : 'WHILE',
    'do'      : 'DO',
    'repeat'  : 'REPEAT',
    'for'     : 'FOR',
    'min'     : 'MIN',
    'max'     : 'MAX'
    'and'     : 'AND',
    'or'      : 'OR',
    'not'     : 'NOT',
    'scan'    : 'SCAN',
    'print'   : 'PRINT',
    'println' : 'PRINTLN',
    'int'     : 'INT',
    'bool'    : 'BOOL',
    'set'     : 'SET',
    'true'    : 'TRUE',
    'false'   : 'FALSE',
    }

tokens = [
   'NEWLINE', 'NUMBER', 'IDENTIFIER', 'STRING', 'COMMENT', 
   'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULE',  'COMMA',
   'SEMICOLON', 'LCURLY', 'RCURLY', 'LBRACKET', 'RBRACKET',
   'ASSIGN', 'COLON', 'SIMPLEQUOTE', 'RDOUBLEQUOTE', 'SETUNION',
   'SETDIFF', 'SETINTERSECT', 'SETMAPPLUS', 'SETMAPMINUS', 
   'SETMAPTIMES', 'SETMAPDIVIDE', 'SETMAPMODULE', 'SETMAXVALUE',
   'SETMINVALUE', 'SETSIZE', 'LESSTHAN', 'GREATERTHAN', 'LESSEQUALTHAN',
   'GREATEREQUALTHAN', 'EQUALS', 'NOTEQUALS', 'BELONGSTO'
] + list(reserved.values())

t_PLUS          = r'\+'
t_MINUS         = r'\-'
t_TIMES         = r'\*'
t_DIVIDE        = r'\/'
t_MODULE        = r'\%' 
t_COMMA         = r'\,'
t_SEMICOLON     = r'\;'
t_LCURLY        = r'\{'
t_RCURLY        = r'\}'
t_LBRACKET      = r'\('
t_RBRACKET      = r'\)'
t_ASSIGN        = r'\='
t_COLON         = r'\:'
t_SIMPLEQUOTE   = r'\''

# Set operators
t_SETUNION      = r'\+\+'
t_SETDIFF       = r'\\'
t_SETINTERSECT  = r'\>\<'
t_SETMAPPLUS    = r'\<\+\>'
t_SETMAPMINUS   = r'\<\-\>'
t_SETMAPTIMES   = r'\<\*\>'
t_SETMAPDIVIDE  = r'\<\/\>'
t_SETMAPMODULE  = r'\<\%\>'
t_SETMAXVALUE   = r'\>\?'
t_SETMINVALUE   = r'\<\?'
t_SETSIZE       = r'\$\?'

# Bool operators
t_LESSTHAN      = r'\<' 
t_GREATERTHAN   = r'\>'
t_LESSEQUALTHAN = r'\<\='
t_GREATEREQUALTHAN = r'\>\=' 
t_EQUALS        = r'\=\='
t_NOTEQUALS     = r'\/\=' 
t_BELONGSTO     = r'\@'

def t_NEWLINE(t):
    r'\n'
    beginningOfLine = t.lexpos
    t.lexer.lineno += len(t.value)
    return t 

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_IDENTIFIER( t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if (reserved.get(t.value, 'IDENTIFIER') != 'IDENTIFIER'):      # Es una palabra reservada
        t.type = reserved.get(t.value, 'IDENTIFIER')
    elif (reserved.get(t.value, 'IDENTIFIER') == 'IDENTIFIER'):    # Es un ID
        t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_STRING(t):
    r'\"([^\n"\\]|\\n|\\"|\\\\|\\’|\\a|\\b|\\f|\\r|\\t|\\v)*?\"'
    return t

def t_error(t):
    print '''Error: Se encontró un caracter inesperado "%s" en la Línea %d, Columna %d''' % (t.value[0], t.lineno, t.lexpos - beginningOfLine)
    error = True
    t.lexer.skip(1)

t_ignore  = ' \t'
t_ignore_COMMENT = r'\#.*'

lexer = lex.lex()