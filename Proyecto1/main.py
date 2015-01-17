from tokens import *

lexer = lex.lex()

data = '''
program {
    using
        int x,y,z;
    in
    
    scan x;
    println "Hola, soy la variable x, valgo: ", x;
    y = x+2;
    # Hola, soy un comentario y no un token. Seamos amigos, :).
}
'''

lexer.input(data)


while True:
    
    tok = lexer.token()
    
    if not tok:
        
         print("hola","hola")
         break
    if tok.type == 'COMMENT':
        lexer.lineno += len(tok.value) 
    else:    
        print tok
