
import ply.lex as lex
from ply.ctokens import t_EQUALS

class rexpr:
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
        'program' : 'Program',
        'in'      : 'In',
        'using'   : 'Using',
        'scan'    : 'Scan',
        'print'   : 'Print',
        'int'     : 'Int'
        }
    
    tokens = [
       'NewLine',
       'Number',
       'Plus',
       'Minus',
       'Times',
       'Divide',
       'String',
       'Id',
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
    
    def t_String(self,t):
        r'\c+'
        return t
    
    def t_Id(self,t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
    
        if (self.reserved.get(t.value,'Id') != 'Id'):
            t.type = self.reserved.get(t.value,'Id')
        else:
            t.type = 'String'
        return t
    
    def t_NewLine(self,t):
        r'\n+'
        return t
    
    t_ignore  = '\t'
    
    
    def t_error(self,t):
        print "Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)
    
    def StringQuote(self,t):
        QuoteType = t.type
        output = ""
        str = t.value
        n = t.lexpos+1
        m = t.lineno
        t = self.lexer.token() 
        while not(t.type == QuoteType):
            if t.value:
                str += t.value
                t = self.lexer.token() 
            else: break
        str += str[0]
        output += "TokenString: %s (Linea %d, Columna %d)\n" %(str,m,n)
        return output
    
    def __init__(self):
        self.lexer = lex.lex(module=self)
