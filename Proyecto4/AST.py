# -*- coding: utf-8 -*-

## Interpretador del lenguaje Setlan.
## Árbol Sintáctico Abstracto (AST)
## Autores:  - Mónica Figuera   11-10328
##           - Carlos Spaggiari 11-10987

import  re
from    symbols import indent, SymbolTable, Symbol
import sys

operator = {"+"   : "PLUS", 
            "-"   : "MINUS",
            "*"   : "TIMES",
            "/"   : "DIVIDE",           
            "%"   : "MODULE", 
            "and" : "AND",
            "or"  : "OR", 
            "not" : "NOT", 
            "<"   : "LESSTHAN",
            ">"   : "GREATERTHAN",
            "<="  : "LESSEQUALSTHAN",   
            "/="  : "NOTEQUALS",
            ">="  : "GREATEREQUALTHAN", 
            "@"   : "BELONGSTO",      
            "=="  : "EQUALS",
            "++"  : "SETUNION",
            "><"  : "SETINTERSECT",   
            "\\"  : "SETDIFF", 
            "<+>" : "SETMAPPLUS",
            "<->" : "SETMAPMINUS",    
            "<*>" : "SETMAPTIMES", 
            "</>" : "SETMAPDIVIDE",   
            "<%>" : "SETMAPMODULE", 
            ">?"  : "SETMAXVALUE",    
            "<?"  : "SETMINVALUE",
            "$?"  : "SETSIZE"}

typeDefault = { "int" : 0, "bool" : False, "set" : set() }

class Program:
    def __init__(self,program="",instruction=""):
        self.program     = program
        self.instruction = instruction
        self.scope       = SymbolTable()

    def printTree(self,tabs):
        string = indent(tabs)+"PROGRAM\n"
        string += self.instruction.printTree(tabs+1)
        return string

    def checkType(self):
        if self.instruction.checkType(self.scope):
            if typeError != []:
                for error in typeError:
                    print error
                return ""
            return self.scope

    def evaluate(self):
        if not self.instruction.execute(self.scope):
            print "\n"
            if typeError != []:
                for error in typeError:
                    print error
                return False
        return True

class Instruction:                                                              #############################################################
    def __init__(self,instruction = "",Id="",assign="",expression=""):
        self.instruction = instruction
        self.id          = Id
        self.assign      = assign
        self.expression  = expression

    def printTree(self,tabs):
        string =""
        if self.assign == "":
            if isinstance(self.instruction, str):
                string += indent(tabs)+self.instruction
            else:
                string += self.instruction.printTree(tabs)
        else:
            string += indent(tabs)+"ASSIGN\n"
            string += self.id.printTree(tabs+1) 
            string += indent(tabs+1)+"value\n"
            string += self.expression.printTree(tabs+2)
        return string 

    def checkType(self,scope):
        if not isinstance(self.instruction, str):
            return self.instruction.checkType(scope)
        else:
            var = self.id.checkType(scope)[0]
            expressionType = self.expression.checkType(scope)
            symbol = scope.lookup(var.value)
            if symbol:
                if symbol.iterator:
                    checkError('forIterator',symbol.name,"","",var.lineno,var.column)
                if symbol.type != expressionType:
                    checkError('badDeclaration',symbol.name,symbol.type,"",var.lineno,var.column)
                return True
        return True

    def execute(self,scope):
        if not isinstance(self.instruction, str):
            return self.instruction.execute(scope)
        else:
            value = self.expression.evaluate(scope)
            if value != None:
                scope.update(self.id.value,value)
                return True
            else:
                return False

class Block:
    def __init__(self,lcurly, instructionBlock,rcurly):
        self.rcurly           = rcurly
        self.lcurly           = lcurly
        self.instructionBlock = instructionBlock

    def printTree(self,tabs):
        string  = indent(tabs)+"BLOCK\n"
        string += self.instructionBlock.printTree(tabs+1)
        string += indent(tabs)+"BLOCK_END\n"
        return string

    def checkType(self,scope):
        return self.instructionBlock.checkType(scope)

    def execute(self,scope):
        return self.instructionBlock.evaluate(scope)

class UsingInInst:
    def __init__(self,Using,declaration,In,instruction):
        self.Using = Using
        self.declaration = declaration
        self.In = In
        self.instruction = instruction
        self.scope = None

    def printTree(self,tabs):
        string  = indent(tabs)+"USING\n"
        string += self.declaration.printTree(tabs+1)
        string += indent(tabs)+"IN\n"
        string += self.instruction.printTree(tabs+1)
        return string

    def checkType(self,scope):
        if scope.currentScope != {}:
            self.scope = SymbolTable()
            self.scope.previousScope = scope
            if (self.declaration.checkType(self.scope) and self.instruction.checkType(self.scope)):
                scope.innerScopes += [self.scope]
                return True
            return False
        else:   
            return (self.declaration.checkType(scope) and self.instruction.checkType(scope))

    def evaluate(self,scope):
        if self.scope != None:
            return self.instruction.evaluate(self.scope)
        else:
            return self.instruction.evaluate(scope)


class DeclarationBlock:
    def __init__(self,varType,Id,semicolon,declaration=""):
        self.varType     = varType
        self.Id          = Id
        self.semicolon   = semicolon
        self.declaration = declaration

    def printTree(self,tabs):
        string = ""
        string += self.Id.printTree(tabs,self.varType)
        if isinstance(self.declaration, str):
            if self.declaration != "":
                string += indent(tabs)+self.declaration
        else:
            string += self.declaration.printTree(tabs)
        return string

    def checkType(self, scope):
        varType = self.varType.checkType(scope)
        varList = self.Id.checkType(scope)
        for var in varList:
            if not var.value in scope.currentScope:
                symbol = Symbol(var.value,varType,typeDefault[varType])
                scope.insert(symbol)
            else:
                checkError('duplicated',var.value,"","",var.lineno,var.column)
        if self.declaration != "":
            return self.declaration.checkType(scope)
        return True

        
class Type:
    def __init__(self,type):
        self.type = type

    def printTree(self,tabs):
        string = indent(tabs)+self.type
        return string

    def checkType(self, scope):
        return self.type


class IDList:
    def __init__(self,value,comma="",IDrecursion="",lineno="",column=""):
        self.type        = 'id'
        self.value       = value
        self.IDrecursion = IDrecursion
        self.lineno      = lineno
        self.column      = column

    def printTree(self,tabs,varType=None):
        string = ""
        if varType:
            string += varType.printTree(tabs)
            string += " "+self.value+"\n"
        else:
            string += indent(tabs)+"variable\n"
            string += indent(tabs+1)+self.value+"\n"
        if not isinstance(self.IDrecursion,str):
            string += self.IDrecursion.printTree(tabs,varType)
        return string 

    def checkType(self,scope):        
        varList = [self]
        if not isinstance(self.IDrecursion,str):
            varList = [self] + self.IDrecursion.checkType(scope)
        return varList


class ID:
    def __init__(self,value,lineno,column):
        self.type   = 'id'
        self.value  = value
        self.lineno = lineno
        self.column = column

    def printTree(self,tabs,varType=None):
        string = ""
        if varType:
            string += varType.printTree(tabs)
            string += " "+self.value+"\n"
        else:
            string += indent(tabs)+"variable\n"
            string += indent(tabs+1)+self.value+"\n"
        return string 

    def checkType(self,scope):
        if scope.contains(self.value):
            return [self]
        checkError('undeclared',self.value,"","",self.lineno,self.column)
        return [self]
        #return [self]       #devuelve el simbolo del id

    def evaluate(self,scope):
        return scope.lookup(self.value).value

class InstructionBlock:
    def __init__(self,instruction="",semicolon="",instructionBlock=""):
        self.instruction      = instruction
        self.semicolon        = semicolon
        self.instructionBlock = instructionBlock

    def printTree(self,tabs):
        string = ""
        if self.instruction != "":
            string += self.instruction.printTree(tabs)
            if isinstance(self.instructionBlock, str):
                string += indent(tabs)+self.instructionBlock
            else:
                string += self.instructionBlock.printTree(tabs)
        return string

    def checkType(self,scope):
        if not isinstance(self.instruction,str):
            if self.instruction.checkType(scope):
                if not isinstance(self.instructionBlock, str):
                    return self.instructionBlock.checkType(scope)
            else:
                return False
        return True

    def evaluate(self,scope):
        if not isinstance(self.instruction,str):
            if self.instruction.execute(scope):
                if not isinstance(self.instructionBlock, str):
                    return self.instructionBlock.evaluate(scope)
                return True
            return False
        else:
            return True


class IfInst:
    def __init__(self, If, lparen, expression, rparen, instruction, Else="", elseInstruction="",lineno="",column=""):
        self.If              = If
        self.lparen          = lparen
        self.expression      = expression
        self.rparen          = rparen
        self.instruction     = instruction
        self.Else            = Else
        self.elseInstruction = elseInstruction
        self.lineno          = lineno
        self.column          = column

    def printTree(self, tabs):
        string  = indent(tabs)+"IF\n"
        string += indent(tabs+1)+"condition\n"
        string += self.expression.printTree(tabs+2)
        string += indent(tabs+1)+"THEN\n"
        string += self.instruction.printTree(tabs+2)
        if (self.Else != ""):
            string += indent(tabs)+"ELSE\n"
            string += self.elseInstruction.printTree(tabs+1)
        return string        

    def checkType(self, scope):
        expressionType = self.expression.checkType(scope)
        if expressionType == "bool":
            if self.instruction.checkType(scope):
                if self.Else != "":
                    return self.elseInstruction.checkType(scope)
                return True
            else:
                return False
        checkError('condition','if','bool', expressionType,self.lineno,self.column)
        return True

    def execute(self,scope):
        if self.expression.evaluate(scope):
            return self.instruction.execute(scope)
        elif self.Else != "":
            return self.elseInstruction.execute(scope)
        else:
            return True

class ForInst:
    def __init__(self,For,Id,Dir,Set,Do,instruction):
        self.For = For
        self.id  = Id
        self.dir = Dir
        self.set = Set
        self.Do  = Do
        self.instruction = instruction
        self.scope = None

    def printTree(self,tabs):
        string  = indent(tabs)+"FOR\n"
        string += self.id.printTree(tabs+1)
        string += self.dir.printTree(tabs+1)
        string += indent(tabs+1)+"IN\n"
        string += self.set.printTree(tabs+1)
        string += indent(tabs+1)+"DO\n"
        string += self.instruction.printTree(tabs+2)
        return string

    def checkType(self,scope):
        symbol                   = Symbol(self.id.value,"int",0,True) # es un iterator
        self.scope               = SymbolTable()
        self.scope.insert(symbol)
        self.scope.previousScope = scope
        scope.innerScopes       += [self.scope]
        expressionType = self.set.checkType(scope)
        if expressionType == "set":
            return self.instruction.checkType(self.scope)
        checkError('range','for','set',expressionType,self.dir.checkType(scope).lineno,self.dir.checkType(scope).column)
        self.instruction.checkType(self.scope)
        return True

    def execute(self,scope):
        Set = list(self.set.evaluate(scope))
        iterator = self.id.value
        if Set == None:
            return False
        Set.sort()
        if self.dir.direction == "min":
            for element in Set:
                self.scope.update(iterator,element)
                if not self.instruction.evaluate(self.scope):
                    return False
        else:
            for element in reversed(Set):
                self.scope.update(iterator,element)
                if not self.instruction.execute(self.scope):
                    return False
        return True

class Direction:
    def __init__(self,direction,lineno,column):
        self.direction = direction
        self.lineno    = lineno
        self.column    = column

    def printTree(self,tabs):
        string = indent(tabs)+"DIRECTION\n"
        string += indent(tabs+1)+self.direction+"\n"
        return string

    def checkType(self,scope):
        return self


class WhileInst:
    def __init__(self,While,lparen,expression,rparen,Do="",instruction="",lineno="",column=""):
        self.While       = While
        self.expression  = expression
        self.Do          = Do
        self.instruction = instruction
        self.lineno      = lineno
        self.column      = column

    def printTree(self,tabs):
        string  = indent(tabs)+"WHILE\n"
        string += indent(tabs+1)+"condition\n"
        string += self.expression.printTree(tabs+2)
        if not isinstance(self.instruction,str):
            string += indent(tabs)+"DO\n"
            string += self.instruction.printTree(tabs+1)
        return string

    def checkType(self, scope):
        expressionType = self.expression.checkType(scope)
        if expressionType == "bool":
            if self.Do != "":
                return self.instruction.checkType(scope)
        checkError('condition','while','bool',expressionType,self.lineno,self.column)
        self.instruction.checkType(scope)
        return True

    def execute(self,scope):
        while self.expression.evaluate(scope):
            if not self.instruction.execute(scope):
                return False
        return True


class RepeatInst:
    def __init__(self,repeat,instruction,While):
        self.While       = While
        self.repeat      = repeat
        self.instruction = instruction

    def printTree(self,tabs):
        string  = indent(tabs)+"REPEAT\n"
        string += self.instruction.printTree(tabs+1)
        string += self.While.printTree(tabs)
        return string
    
    def checkType(self,scope):
        return (self.instruction.checkType(scope) and self.While.checkType(scope))
        
    def execute(self,scope):
        return self.instruction.execute(scope)

class ScanInst:
    def __init__(self,scan,expression,lineno,column):
        self.scan       = scan
        self.expression = expression
        self.lineno     = lineno
        self.column     = column

    def printTree(self,tabs):
        string = indent(tabs)+"SCAN\n"
        string += self.expression.printTree(tabs+1)
        return string
    
    def checkType(self,scope):
        expressionType = self.expression.checkType(scope)
        if (expressionType != 'int') & (expressionType != 'bool'):
            checkError('scanSet','','',expressionType,self.lineno,self.column)
        return True
        
    def execute(self,scope):
        return True         ################ Debe funcionar scanear una variable?

class PrintInst:
    def __init__(self,Print,output):
        self.Print  = Print
        self.output = output

    def printTree(self,tabs):
        string  = indent(tabs)+"PRINT"+"\n"
        string += indent(tabs+1)+"elements\n"
        string += self.output.printTree(tabs+2)
        if (self.Print == "println"):
            string += String("\"\\n\"").printTree(tabs+2)
        return string
    
    def checkType(self,scope):
        return self.output.checkType(scope)
        
    def execute(self,scope):
        if self.output.evaluate(scope):
            if self.Print == "println":
                sys.stdout.write("\n")
            return True
        return False

class OutputType:
    def __init__(self,expression,comma="",outputRecursion=""):
        self.expression      = expression
        self.comma           = comma
        self.outputRecursion = outputRecursion

    def printTree(self,tabs):
        string = self.expression.printTree(tabs)
        if not isinstance(self.outputRecursion,str):
            string += self.outputRecursion.printTree(tabs)
        return string
      
    def checkType(self,scope):
        self.expression.checkType(scope)
        if not isinstance(self.outputRecursion,str):
            self.outputRecursion.checkType(scope)
        return True

    def evaluate(self,scope):

        output = self.expression.evaluate(scope)
        if output == None:
            return False
        elif isinstance(output,set):
            Set = "{"
            for j in output:
                Set += str(j)+","
            if Set[len(Set)-1] == ",":
                Set = Set[:len(Set)-1]
            Set += "}"
            sys.stdout.write(Set)
        elif isinstance(output,bool):
            if output:
                sys.stdout.write("true")
            else:
                sys.stdout.write("false")
        else:
            sys.stdout.write(str(output))
        if self.comma != "":
            return self.outputRecursion.evaluate(scope)
        return True

class String:
    def __init__(self,string):
        self.string = string

    def printTree(self,tabs):
        string = indent(tabs)+"string\n"
        string += indent(tabs+1)+self.string+"\n"
        return string

    def checkType(self,scope):
        return True

    def evaluate(self,scope):
        return self.string[1:len(self.string)-1]        

class Expression:
    def __init__(self,left,op="",right=""):
        self.type  = "expression"
        self.left  = left
        self.right = right
        self.op    = op

    def printTree(self,tabs):
        string = ""
        if self.op != "":
            if self.right == "":
                if self.op == '-':
                    string += indent(tabs)+"NEGATE"+" "+self.op+"\n"
                else:
                    string += indent(tabs)+operator[self.op]+" "+self.op+"\n"
                string += self.left.printTree(tabs+1)
            else:
                if self.left == "(" and self.right == ")":
                    string += self.op.printTree(tabs)
                else:
                    string += indent(tabs)+operator[self.op]+" "+self.op+"\n"
                    string += self.left.printTree(tabs+1)
                    string += self.right.printTree(tabs+1)
        else:
            if isinstance(self.left, str):
                string += self.left
            else:
                string += self.left.printTree(tabs)
        return string

    def checkType(self,scope):
        if self.op != "":
            # Operadores unarios
            if self.right == "":
                type1 = self.left.checkType(scope)
                if re.match(r'[not]',self.op) and type1 == "bool":
                    return "bool"
                elif re.match(r'[\-]',self.op) and type1 == "int":
                    return "int"
                elif re.match(r'[>?|<?|$?]',self.op) and type1 == "set":
                    return "int"
                
            # Operadores binarios
            else:
                if self.left == "(" and self.right == ")":
                    return self.op.checkType(scope)
                else:
                    type1 = self.left.checkType(scope)
                    type2 = self.right.checkType(scope)
                    if re.match(r'[+|*|/|\-|%]',self.op) and type1 == type2 == "int":
                        return "int"
                    elif re.match(r'[and|or]',self.op) and type1 == type2 == "bool":
                        return "bool"
                    elif re.match(r'[<|>|<=|>=|/=]',self.op) and type1 == type2 == "int":
                        return "bool"
                    elif re.match(r'[++|><|\\]',self.op) and type1 == type2 == "set":
                        return "set"
                    elif ((self.op == "<+>") | (self.op == "<->") | (self.op == "<*>") | (self.op == "</>") | (self.op == "<%>")) \
                     and (type1 == "int" or type1 == "set") and (type2 == "int" or type2 == "set") and type1 != type2:
                        return "set"
                    elif re.match(r'[@]',self.op) and type1 == "int" and type2 == "set":
                        return "bool"
                checkError('expression',self.op,type1,type2)
        else:
            if not isinstance(self.left, str):
                self.left.checkType(scope)
                if isinstance(self.left.value,str):
                    if (self.left.value != 'true') & (self.left.value != 'false'):
                        if isinstance(self.left.value,str):
                            if re.match(r'[a-zA-Z_][a-zA-Z_0-9]*',self.left.value):     # verifica si el id usado fue declarado y chequea su tipo
                                symbol = scope.lookup(self.left.value)
                                if symbol:
                                    return symbol.type 
                                else: 
                                    return ''                                           # '' indica que se ingreso una variable no declarada
                                                   # '' indica que se ingreso una variable no declarada
            
            return self.left.checkType(scope)
        return ''
        
    def evaluate(self,scope):
        if self.op != "":
            if self.right == "":
                value = self.left.evaluate(scope)
                if (self.op == "-"):
                    return -value
                elif (self.op == "not"):
                    return not value
                elif self.op == ">?":
                    if len(value):
                        return max(value)
                    else:
                        return checkError("emptySetOperation")
                elif self.op == "<?": 
                    if len(value):
                        return min(value)
                    else:
                        return checkError("emptySetOperation")
                elif self.op == "$?":
                    return len(value)
            else:
                pass
        elif not isinstance(self.left,str):
            return self.left.evaluate(scope)

class Set:
    def __init__(self,lcurly,setNumbers="",rcurly=""):
        self.lcurly = lcurly
        self.value = setNumbers
        self.rcurly = rcurly

    def printTree(self, tabs):
        string = indent(tabs)+"set\n"
        if not isinstance(self.value, str):
            string += self.value.printTree(tabs+1)
        return string
        
    def checkType(self,scope):
        if not isinstance(self.value,str):
            return self.value.checkType(scope)
        return 'set'    # conjunto vacio    

    def evaluate(self,scope):
        Set = []
        if not isinstance(self.value, str):
            Set += self.value.evaluate(scope)
        return set(Set)

class SetNumbers:
    def __init__(self, expression, comma="", setNumbersRecursion=""):
        self.expression = expression
        self.comma = comma
        self.setNumbersRecursion = setNumbersRecursion
        
    def printTree(self, tabs):
        string = self.expression.printTree(tabs)
        if not isinstance(self.setNumbersRecursion, str):
            string += self.setNumbersRecursion.printTree(tabs)
        return string
    
    def checkType(self,scope):
        if self.expression.checkType(scope) != 'int':
            return ''
        if not isinstance(self.setNumbersRecursion, str):
            self.setNumbersRecursion.checkType(scope)
        return 'set'

    def evaluate(self,scope):
        Set = [self.expression.evaluate(scope)]
        if self.comma != "":
            Set += self.setNumbersRecursion.evaluate(scope)
        return Set

class BooleanValue:
    def __init__(self,value):
        self.value = value

    def printTree(self, tabs):
        string  = indent(tabs)+"bool\n"
        string += indent(tabs+1)+self.value+"\n"
        return string

    def checkType(self,scope):
        return 'bool'

    def evaluate(self,scope):
        return self.value == "true"


class Number:
    def __init__(self,value):
        self.value = value

    def printTree(self,tabs):
        string  = indent(tabs)+"int\n"
        string += indent(tabs+1) + str(self.value) + "\n"
        return string
    
    def checkType(self,scope): 
        return 'int'
        
    def evaluate(self,scope):
        return self.value

def checkError(error,instOrVar="",expectedType="",wrongType="",lineno="",column=""):
    if error == 'condition':
        if wrongType == "":
            wrongType = "*no especificado*"
        typeError.append('''ERROR en la Linea %d, Columna %d: La instruccion "%s" espera condicion de tipo "%s", no de tipo "%s".''' \
        % (lineno, column, instOrVar, expectedType, wrongType))
    elif error == 'range':
        if wrongType == "":
            wrongType = "*no especificado*"
        typeError.append('''ERROR en la Linea %d, Columna %d: La instruccion "%s" espera rango de tipo "%s", no de tipo "%s".''' \
        % (lineno, column, instOrVar, expectedType, wrongType))
    elif error == 'undeclared':
        typeError.append('''ERROR en la Linea %d, Columna %d: La variable "%s" no ha sido declarada en este alcance.''' \
            % (lineno, column, instOrVar))
    elif error == 'badDeclaration':
        typeError.append('''ERROR en la Linea %d, Columna %d: La variable "%s" espera valores de tipo "%s".''' \
            % (lineno, column, instOrVar, expectedType))
    elif error == 'duplicated':
        typeError.append('''ERROR en la Linea %d, Columna %d: La variable "%s" ya fue declarada en este alcance.''' \
            % (lineno, column, instOrVar))
    elif error == 'forIterator':
        typeError.append('''ERROR en la Linea %d, Columna %d: La variable de iteracion "%s" no puede ser modificada.''' \
            % (lineno, column, instOrVar))
    elif error == 'scanSet':
        if wrongType == "":
            wrongType = "*no declarada*"
        typeError.append('''ERROR en la Linea %d, Columna %d: La instruccion "scan" no puede escanear variable de tipo "%s".''' \
            % (lineno, column,wrongType))
    elif error == 'expression':
        if (expectedType == ""):
            expectedType = "*no especificado*"
        if (wrongType == ""):
            wrongType = "*no especificado*"
        typeError.append('''ERROR en la Linea %d, Columna %d: El operador "%s" no opera sobre tipos "%s" y "%s".''' \
            % (0000, 0000, instOrVar, expectedType, wrongType)) 
    elif error == 'emptySetOperation':
        typeError.append("Error en la linea %d, Columna %d: Operación sobre un conjunto vacio"%(1,1)       )
    return False

typeError = []