# -*- coding: utf-8 -*-

## Interpretador del lenguaje Setlan.
## Analizador Lexicográfico (Lexer)
## Autores:  - Mónica Figuera   11-10328
##           - Carlos Spaggiari 11-10987

import ply.lex as lex
maxInt = 2147483648
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
    'max'     : 'MAX',
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
   'NUMBER', 'IDENTIFIER', 'STRING', 'LCURLY', 'RCURLY', 'LPAREN', 'RPAREN',
   'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULE', 'COMMA', 'SEMICOLON', 
   'ASSIGN', 'SETUNION', 'SETDIFF', 'SETINTERSECT', 'SETMAPPLUS',
   'SETMAPMINUS', 'SETMAPTIMES', 'SETMAPDIVIDE', 'SETMAPMODULE',
   'SETMAXVALUE', 'SETMINVALUE', 'SETSIZE', 'LESSTHAN', 'GREATERTHAN',
   'LESSEQUALTHAN', 'GREATEREQUALTHAN', 'EQUALS', 'NOTEQUALS', 'BELONGSTO'
] + list(reserved.values())

t_LCURLY        = r'\{'
t_RCURLY        = r'\}'
t_LPAREN        = r'\('
t_RPAREN        = r'\)'
t_PLUS          = r'\+'
t_MINUS         = r'\-'
t_TIMES         = r'\*'
t_DIVIDE        = r'\/'
t_MODULE        = r'\%' 
t_COMMA         = r'\,'
t_SEMICOLON     = r'\;'
t_ASSIGN        = r'\='

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

t_ignore  = ' \t'
t_ignore_COMMENT = r'\#.*'

def t_NUMBER(t):
    r'\d+'
    if int(t.value) > maxInt:
        error_NUMBER(t)
    t.value = int(t.value)    
    return t

def t_IDENTIFIER( t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_STRING(t):
    r'\"([^\n"\\]|\\n|\\"|\\\\)*?\"'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def findColumn(input,tokLexpos):
    beginOfLine = input.rfind('\n',0,tokLexpos)
    if beginOfLine < 0:
        beginOfLine = -1
    column = (tokLexpos - beginOfLine)
    return column

def t_error(t):
    lexError.append('''ERROR: Se encontró un caracter inesperado "%s" en la Línea %d, Columna %d.''' \
        % (t.value[0], t.lineno, findColumn(t.lexer.lexdata,t.lexpos)))
    t.lexer.skip(1)

def error_NUMBER(t):
    lexError.append('''ERROR: Entero fuera de rango "%s" en la Línea %d, Columna %d.''' \
        % (t.value, t.lineno, findColumn(t.lexer.lexdata, t.lexpos)))

def printLex(data):
    lex2 = lex.lex()
    lex2.input(data)
    while True:
        tok = lex2.token()
        if not tok : 
            print ""
            break
        if len(tok.type) > 9:
            print '''Token %s\tvalor (%s), en la Línea %d, Columna %d.''' \
                % (tok.type,tok.value,tok.lineno,findColumn(lex2.lexdata, tok.lexpos))
        else:
            print '''Token %s\t\tvalor (%s), en la Línea %d, Columna %d.''' % \
                (tok.type,tok.value,tok.lineno,findColumn(lex2.lexdata, tok.lexpos))

# Construcción del lexer
lexer = lex.lex()
lexError = []