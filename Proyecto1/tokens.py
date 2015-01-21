# -*- coding: utf-8 -*-

import ply.lex as lex
from django.template.base import Lexer

class rexpr:
    error = False
    inicioLinea = 0
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
        'return'  : 'Return'
        }
    
    tokens = [
       'NewLine',
       'Number',
       'Plus',
       'Minus',
       'Times',
       'Divide',
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
       'Quote'
    ] + list(reserved.values())
    
    t_Plus          = r'\+'
    t_Minus         = r'-'
    t_Times         = r'\*'
    t_Divide        = r'/'
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

    def t_String(self,t):
        r'\c+'
        t.type = 'String'     
        return t
        
    def t_NewLine(self,t):
        r'\n+'
        self.inicioLinea = t.lexpos + 1 
        #t.lineno += 1
        t.lexer.lineno += len(t.value)
        return t 
       
    t_ignore  = '\t'
    
    def t_error(self,t):
        print '''Error: Se encontró un caracter inesperado "%s" en la Línea %d, Columna %d''' % (t.value[0],t.lineno,t.lexpos - self.inicioLinea)
        self.error = True
        t.lexer.skip(1)
    
    # Funcion que atrapa todo el string dentro de comillas.
    # No acepta que haya salto de linea \n
    def StringQuote(self,t):
        QuoteType = t.type
        output = ""
        str = t.value
        n = t.lexpos - self.inicioLinea
        m = t.lineno
        t = self.lexer.token()
        while not(t.type == QuoteType):
            if t: 
                str += t.value
                t = self.lexer.token()
            else: break
        str += str[0]
        output += "TokenString: %s (Línea %d, Columna %d)\n" %(str,m,n)
        return output
    
    def __init__(self):
        self.lexer = lex.lex(module=self)
