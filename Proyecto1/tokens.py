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
    inicioLinea = -1
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
       'Colon',
       'SimpleQuote',
       'Quote',
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
       'ReturnValue'
    ] + list(reserved.values())
    

    t_Plus          = r'\+'
    t_Minus         = r'\-'
    t_Times         = r'\*'
    t_Divide        = r'\/'
    t_Module        = r'\%'       
    t_Comment       = r'\#'
    t_Comma         = r'\,'
    t_Semicolon     = r'\;'
    t_OpenCurly     = r'\{'
    t_CloseCurly    = r'\}'
    t_OpenBracket   = r'\('
    t_CloseBracket  = r'\)'
    t_Space         = r'\ '
    t_Equals        = r'\=' 
    t_Dot           = r'\.'
    t_Colon         = r'\:'
    t_SimpleQuote   = r'\''
    t_Quote         = r'\"'
    t_ReturnValue   = r"\-\>" #(?)

    # Set operators
    t_Union         = r'\+\+'    # (?)
    t_Difference    = r'\\'     # (?)
    t_Intersection  = r'\>\<'
    t_MappingPlus   = r'\<\+\>'
    t_MappinMinus   = r'\<\-\>'
    t_MappingTimes  = r'\<\*\>'
    t_MappingDivide = r'\<\/\>'
    t_MappingModule = r'\<\%\>'
    t_SetMaxValue   = r'\>\?'
    t_SetMinValue   = r'\<\?'
    t_SetSize       = r'\$\?'

    # Bool operators
    t_LessThan      = r'\<' 
    t_GreaterThan   = r'\>'
    t_LessEqualThan = r'\<\='
    t_GreaterEqualThan = r'\>\=' 
    t_Equivalence   = r'\=\='
    t_Inequivalence = r'\/\=' 
    t_BelongsTo     = r'\@'

    def t_Number(self,t):
        r'\d+'
        t.value = int(t.value)    
        return t

    def t_ID(self,t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
    
        if (self.reserved.get(t.value,'ID') != 'ID'):       # Es una palabra reservada
            t.type = self.reserved.get(t.value,'ID')
        elif (self.reserved.get(t.value,'ID') == 'ID'):     # Es un ID
            t.type = self.reserved.get(t.value,'ID')
        return t


        
    def t_NewLine(self,t):
        r'\n+'
        self.inicioLinea = t.lexpos 
        t.lexer.lineno += len(t.value)
        return t 
       
    #t_ignore  = '\t'
    
    def t_error(self,t):
        if self.readingString:
          print t.value[0]
          self.output += t.value[0]
        elif not self.readingComment:
          self.errorOutput += '''Error: Se encontró un caracter inesperado "%s" en la Línea %d, Columna %d\n''' % (t.value[0],t.lineno,t.lexpos - self.inicioLinea)
          self.error = True
        t.lexer.skip(1)
    
    # Funcion que atrapa todo el string dentro de comillas.

    def StringQuote(self,t):
        quoteType = t.type
        quote = t.value
        self.output += "TokenString: %s" % t.value
        n = t.lexpos - self.inicioLinea
        m = t.lineno
        t = self.lexer.token()
        self.readingString = True
        while not(t.type == quoteType):
            if t: 
                self.output += t.value
                t = self.lexer.token()
            else: break
        self.output += quote
        self.output += " (Línea %d, Columna %d)\n" %(m,n)
        self.readingString = False
    
    def ignoreComment(self,t):
        previousErrorValue = self.error
        while (t.type != 'NewLine'):
            t = self.lexer.token() 
        self.error = previousErrorValue

    def __init__(self):
        self.lexer = lex.lex(module=self)
