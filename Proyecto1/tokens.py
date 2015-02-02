#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

import ply.lex as lex
from django.template.base import Lexer

class LexicalAnalyzer:
    error = False
    output = ""
    readingString = False
    errorOutput = ''
    beginningOfLine = -1
    reserved = {
        'if'      : 'IF',
        'else'    : 'ELSE',
        'elif'    : 'ELIF',
        'def'     : 'DEF',
        'class'   : 'CLASS',
        'while'   : 'WHILE',
        'for'     : 'FOR',
        'and'     : 'AND',
        'or'      : 'OR',
        'program' : 'PROGRAM',
        'in'      : 'IN',
        'using'   : 'USING',
        'scan'    : 'SCAN',
        'print'   : 'PRINT',
        'println' : 'PRINTLN',
        'int'     : 'INT',
        'bool'    : 'BOOL',
        'set'     : 'SET',
        'break'   : 'BREAK',
        'true'    : 'TRUE',
        'false'   : 'FALSE',
        'not'     : 'NOT',
        'do'      : 'DO',
        'repeat'  : 'REPEAT',
        'return'  : 'RETURN',
        'min'     : 'MIN',
        'max'     : 'MAX'
        }
    
    tokens = [
       'NEWLINE', 'NUMBER', 'IDENTIFIER', 'STRING', 'COMMENT', 
       'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULE',  'COMMA',
       'SEMICOLON', 'LCURLY', 'RCURLY', 'LBRACKET', 'RBRACKET',
       'SPACE', 'ASSIGN', 'DOT', 'TAB', 'COLON', 'SIMPLEQUOTE',
       'RDOUBLEQUOTE', 'SETUNION', 'SETDIFF', 'SETINTERSECT',
       'SETMAPPLUS', 'SETMAPMINUS', 'SETMAPTIMES', 'SETMAPDIVIDE',
       'SETMAPMODULE', 'SETMAXVALUE', 'SETMINVALUE', 'SETSIZE',
       'LESSTHAN', 'GREATERTHAN', 'LESSEQUALTHAN', 'GREATEREQUALTHAN',
       'EQUALS', 'NOTEQUALS', 'BELONGSTO', 'NEWLINEESC',
       'QUOTEESC', 'BACKSLASHESC'
    ] + list(reserved.values())
    
    states = (
        ('STRING','exclusive'),
    )

    t_ANY_PLUS      = r'\+'
    t_ANY_MINUS     = r'\-'
    t_ANY_TIMES     = r'\*'
    t_ANY_DIVIDE    = r'\/'
    t_ANY_MODULE    = r'\%' 
    t_ANY_COMMA     = r'\,'
    t_ANY_SEMICOLON = r'\;'
    t_ANY_LCURLY    = r'\{'
    t_ANY_RCURLY    = r'\}'
    t_ANY_LBRACKET  = r'\('
    t_ANY_RBRACKET  = r'\)'
    t_ANY_SPACE     = r'\ '
    t_ANY_TAB       = r'\t'
    t_ANY_ASSIGN    = r'\='
    t_ANY_DOT       = r'\.'
    t_ANY_COLON     = r'\:'
    t_ANY_SIMPLEQUOTE = r'\''
    
    # Set operators
    t_ANY_SETUNION      = r'\+\+'
    t_ANY_SETDIFF       = r'\\'
    t_ANY_SETINTERSECT  = r'\>\<'
    t_ANY_SETMAPPLUS    = r'\<\+\>'
    t_ANY_SETMAPMINUS   = r'\<\-\>'
    t_ANY_SETMAPTIMES   = r'\<\*\>'
    t_ANY_SETMAPDIVIDE  = r'\<\/\>'
    t_ANY_SETMAPMODULE  = r'\<\%\>'
    t_ANY_SETMAXVALUE   = r'\>\?'
    t_ANY_SETMINVALUE   = r'\<\?'
    t_ANY_SETSIZE       = r'\$\?'

    # Bool operators
    t_ANY_LESSTHAN      = r'\<' 
    t_ANY_GREATERTHAN   = r'\>'
    t_ANY_LESSEQUALTHAN = r'\<\='
    t_ANY_GREATEREQUALTHAN = r'\>\=' 
    t_ANY_EQUALS        = r'\=\='
    t_ANY_NOTEQUALS    = r'\/\=' 
    t_ANY_BELONGSTO     = r'\@'

    def t_ANY_NEWLINE(self, t):
        r'\n'
        self.beginningOfLine = t.lexpos
        t.lexer.lineno += len(t.value)
        return t 

    def t_ANY_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)    
        return t

    def t_ANY_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        if (self.reserved.get(t.value, 'IDENTIFIER') != 'IDENTIFIER'):      # Es una palabra reservada
            t.type = self.reserved.get(t.value, 'IDENTIFIER')
        elif (self.reserved.get(t.value, 'IDENTIFIER') == 'IDENTIFIER'):    # Es un ID
            t.type = self.reserved.get(t.value, 'IDENTIFIER')
        return t

    def t_STRING(self,t):
        r'\"'
        self.readingString = True
        t.lexer.begin('STRING')
        return t

    def t_STRING_RDOUBLEQUOTE(self,t):
        r'\"'
        self.readingString = False
        t.lexer.begin('INITIAL')
        return t

    def t_STRING_NEWLINEESC(self,t):
        r'\\n'
        return t
        
    def t_STRING_QUOTEESC(self,t):
        r'\\\"'
        return t

    def t_STRING_BACKSLASHESC(self,t):
        r'\\\\'
        return t

    def GetString(self, t):
        quoteType = t.type
        quote = t.value
        n = t.lexpos - self.beginningOfLine
        m = t.lineno
        t = self.lexer.token()
        if t:
            if t.lineno == m:
                self.output += "token STRING\t\tvalue (%s\") at line %d, column %d\n" % (quote,m,n)
        else:
             self.errorOutput += '''Error: Se encontró un caracter inesperado \" en la Línea %d, Columna %d.\n''' % (m, n)
             self.error = True

    def t_ANY_error(self, t):
        if self.readingString:
            print t.value[0]
            self.output += t.value[0]
        else:
            self.errorOutput += '''Error: Se encontró un caracter inesperado "%s" en la Línea %d, Columna %d\n''' % (t.value[0], t.lineno, t.lexpos - self.beginningOfLine)
            self.error = True
        t.lexer.skip(1)

    t_ANY_ignore_COMMENT = r'\#.*'

    def __init__(self):
        self.lexer = lex.lex(module=self)