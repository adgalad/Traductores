#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

import ply.lex as lex
from django.template.base import Lexer

class LexicalAnalyzer:
    error = False
    output = ""
    readingString = False
    readingComment = False
    errorOutput = ''
    beginningOfLine = -1
    reserved = {
        'if'      : 'If',
        'else'    : 'Else',
        'elif'    : 'Elif',
        'def'     : 'Def',
        'class'   : 'Class',
        'while'   : 'While',
        'for'     : 'for',
        'and'     : 'And',
        'or'      : 'Or',
        'program' : 'Program',
        'in'      : 'In',
        'using'   : 'Using',
        'scan'    : 'Scan',
        'print'   : 'Print',
        'println' : 'Println',
        'int'     : 'Int',
        'bool'    : 'Bool',
        'set'     : 'Set',
        'break'   : 'Break',
        'true'    : 'True',
        'false'   : 'False',
        'not'     : 'Not',
        'do'      : 'Do',
        'repeat'  : 'Repeat',
        'return'  : 'Return',
        'min'     : 'Min',
        'max'     : 'Max'
        }
    
    tokens = [
       'NewLine',
       'Number',
       'Plus',
       'Minus',
       'Times',
       'Divide',
       'Module',
       'ID',
       'String',
       'Comment',
       'Comma',
       'Semicolon',
       'OpenCurly',
       'CloseCurly',
       'OpenBracket',
       'CloseBracket',
       'Space',
       'Equals',
       'Dot',
       'Tab',
       'Colon',
       'SimpleQuote',
       'CloseQuote',
       'Union',
       'Difference',
       'Intersection',
       'MappingPlus',
       'MappinMinus',
       'MappingTimes',
       'MappingDivide',
       'MappingModule',
       'SetMaxValue',
       'SetMinValue',
       'SetSize',
       'LessThan',
       'GreaterThan',
       'LessEqualThan',
       'GreaterEqualThan',
       'Equivalence',
       'Inequivalence',
       'BelongsTo',
       'ReturnValue',
       'NewLineEsc',
       'QuoteEsc',
       'BackSlashEsc',
    ] + list(reserved.values())
    
    t_ANY_Plus = r'\+'
    t_ANY_Minus = r'\-'
    t_ANY_Times = r'\*'
    t_ANY_Divide = r'\/'
    t_ANY_Module = r'\%' 
    t_ANY_Comma = r'\,'
    t_ANY_Semicolon = r'\;'
    t_ANY_OpenCurly = r'\{'
    t_ANY_CloseCurly = r'\}'
    t_ANY_OpenBracket = r'\('
    t_ANY_CloseBracket = r'\)'
    t_ANY_Space = r'\ '
    t_ANY_Tab = r'\t'
    t_ANY_Equals = r'\='
    t_ANY_Dot = r'\.'
    t_ANY_Colon = r'\:'
    t_ANY_SimpleQuote = r'\''
    t_ANY_ReturnValue = r"\-\>"  # (?)
    
    # Set operators
    t_ANY_Union = r'\+\+'  # (?)
    t_ANY_Difference = r'\\'  # (?)
    t_ANY_Intersection = r'\>\<'
    t_ANY_MappingPlus = r'\<\+\>'
    t_ANY_MappinMinus = r'\<\-\>'
    t_ANY_MappingTimes = r'\<\*\>'
    t_ANY_MappingDivide = r'\<\/\>'
    t_ANY_MappingModule = r'\<\%\>'
    t_ANY_SetMaxValue = r'\>\?'
    t_ANY_SetMinValue = r'\<\?'
    t_ANY_SetSize = r'\$\?'

    # Bool operators
    t_ANY_LessThan = r'\<' 
    t_ANY_GreaterThan = r'\>'
    t_ANY_LessEqualThan = r'\<\='
    t_ANY_GreaterEqualThan = r'\>\=' 
    t_ANY_Equivalence = r'\=\='
    t_ANY_Inequivalence = r'\/\=' 
    t_ANY_BelongsTo = r'\@'
    
    #Escape Sequence

    states = (
        ('String','exclusive'),
    )

    def t_ANY_Number(self, t):
        r'\d+'
        t.value = int(t.value)    
        return t

    def t_ANY_NewLine(self, t):
        r'\n'
        self.beginningOfLine = t.lexpos
        t.lexer.lineno += len(t.value)
        return t 

    def t_String(self,t):
        r'\"'
        t.lexer.begin('String')
        return t

    def t_String_CloseQuote(self,t):
        r'\"'
        t.lexer.begin('INITIAL')
        return t

    def t_String_NewLineEsc(self,t):
        r'\\n'
        return t
        
    def t_String_QuoteEsc(self,t):
            r'\\\"'
            return t
    def t_String_BackSlashEsc(self,t):
            r'\\\\'
            return t
    
    def t_ANY_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
    
        if (self.reserved.get(t.value, 'ID') != 'ID'):  # Es una palabra reservada
            t.type = self.reserved.get(t.value, 'ID')
        elif (self.reserved.get(t.value, 'ID') == 'ID'):  # Es un ID
            t.type = self.reserved.get(t.value, 'ID')
        return t
        
       
    
    def t_ANY_error(self, t):
        if self.readingString:
          print t.value[0]
          self.output += t.value[0]
        elif not self.readingComment:
          self.errorOutput += '''Error: Se encontró un caracter inesperado "%s" en la Línea %d, Columna %d\n''' % (t.value[0], t.lineno, t.lexpos - self.beginningOfLine)
          self.error = True
        t.lexer.skip(1)
    
    # Funcion que atrapa todo el string dentro de comillas.


    def String(self, t):
        quoteType = t.type
        quote = t.value
        self.output += "TokenString: %s" % t.value
        n = t.lexpos - self.beginningOfLine
        m = t.lineno
        t = self.lexer.token()
        self.readingString = True

        while not(t.type == "CloseQuote"):
            if t.value == '\\':
                self.errorOutput += '''Error: Se encontró un caracter inesperado "%s" en la Línea %d, Columna %d\n''' % (t.value[0], t.lineno, t.lexpos - self.beginningOfLine)
                self.error = True
            if t: 
                self.output += t.value
                t = self.lexer.token()
            else: break
        self.output += quote
        self.output += " (Línea %d, Columna %d)\n" % (m, n)
        self.readingString = False
    
    t_ANY_ignore_Comment = r'\#.*'

    def __init__(self):
        self.lexer = lex.lex(module=self)
        
        
    
