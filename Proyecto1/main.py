from tokens import *

AF = rexpr()


data = '''program {
    using
        int x,y,z;
    in
    
    scan x;
    println "Hola, soy la variable x, valgo: ", x;
    y = x+2;
    # Hola, soy un comentario y no un token. Seamos amigos, :).
}'''

AF.lexer.input(data)

output = ""

while True:    
    tok = AF.lexer.token()
    
    if not tok: break
    if (tok.type != 'Space' and tok.type != 'NewLine'):
        if tok.type == 'Quote' or tok.type == 'SimpleQuote':
            output += AF.StringQuote(tok)
        elif tok.type == 'Comment':
            while (tok.type != 'NewLine'):
                tok = AF.lexer.token() 
            
        else:    
            output+="Token%s %s (Linea %d,Columna %d)\n" %(tok.type,tok.value,tok.lineno,tok.lexpos - AF.inicioLinea)

print output