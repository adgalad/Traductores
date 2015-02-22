# -*- coding: utf-8 -*-

## Interpretador del lenguaje Setlan.
## Árbol Sintáctico Abstracto (AST)
## Autores:  - Mónica Figuera   11-10328
##           - Carlos Spaggiari 11-10987

import  symbols

operator = {"+"   : "PLUS", 
            "-"   : "MINUS",
            "*"   : "TIMES",
            "/"   : "DIVIDE",           
            "%"   : "MODULE", 
            "and" : "AND",
            "or"  : "OR", 
            "<"   : "LESSTHAN",
            ">"   : "GREATERTHAN",
            "<="  : "LESSEQUALSTHAN",   
            "/="  : "NOTEQUALS",
            "\\"  : "SETDIFF", 
            ">="  : "GREATEREQUALTHAN", 
            "not" : "NOT", 
            "++"  : "SETUNION",
            "@"   : "BELONGSTO",      
            "=="  : "EQUALS",   
            "><"  : "SETINTERSECT",   
            "<+>" : "SETMAPPLUS",
            "<->" : "SETMAPMINUS",    
            "<*>" : "SETMAPTIMES", 
            "</>" : "SETMAPDIVIDE",   
            "<%>" : "SETMAPMODULE", 
            ">?"  : "SETMAXVALUE",    
            "<?"  : "SETMINVALUE",
            "$?"  : "SETSIZE"}

typeDefault = { "int" : "0", "bool" : "False", "set" : "{}" }

def indent(tabs):
    return "   "*tabs

class Program:
    def __init__(self,program="",instruction=""):
        self.program = program
        self.instruction = instruction
        self.scope = symbols.symbolTable()

    def printTree(self,tabs):
        string = indent(tabs)+"PROGRAM\n"
        string += self.instruction.printTree(tabs+1)
        return string

    def checkType(self):
        if self.instruction.checkType(self.scope):
            print self.scope.currentScope

class Instruction:
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
        if self.assign == "":
            if not isinstance(self.instruction, str):
                self.instruction.checkType(scope)               # . . . A Y U D A
                return True
        else:
            print("Asigno")
            var = self.id.checkType()[0]
            value = self.expression.checkType(scope)
            symbol = scope.lookup(var)
            if symbol:
                scope.update(symbol.name, symbol.type, value)
                return True
        return False


class Block:
    def __init__(self,lcurly, instructionBlock,rcurly):
        
        self.rcurly = rcurly
        self.lcurly = lcurly
        self.instructionBlock = instructionBlock

    def printTree(self,tabs):
        string  = indent(tabs)+"BLOCK\n"
        string += self.instructionBlock.printTree(tabs+1)
        string += indent(tabs)+"BLOCK_END\n"
        return string

    def checkType(self,scope):
#        print(scope.currentScope)
        if scope.previousScope:
            newScope = symbols.symbolTable()
            newScope.previousScope = scope
            scope.innerScopes += [newScope]
            scope = newScope
        else:
            if scope.currentScope != {}:
                newScope = symbols.symbolTable()
                newScope.previousScope = scope
                scope.innerScopes += [newScope]
                scope = newScope
               
        if self.instructionBlock.checkType(scope): 
            if scope.previousScope:
                scope = scope.previousScope
                print(scope.previousScope)
            return True

        return False


class UsingInInst:
    def __init__(self,Using,declaration,In,instruction):
        self.Using = Using
        self.declaration = declaration
        self.In = In
        self.instruction = instruction

    def printTree(self,tabs):
        string = indent(tabs)+"USING\n"
        string += self.declaration.printTree(tabs+1)
        string += indent(tabs)+"IN\n"
        string += self.instruction.printTree(tabs+1)
        return string

    def checkType(self,scope):
        if (self.declaration.checkType(scope) and self.instruction.checkType(scope)):
#            print(scope.currentScope)
            return True
        return False

class DeclarationBlock:
    def __init__(self,varType,Id,semicolon,declaration=""):
        self.varType = varType
        self.Id = Id
        self.semicolon = semicolon
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
            symbol = symbols.Symbol(var,varType,typeDefault[varType])
            if not scope.insert(symbol):
                return checkError('duplicated',"","",var)                 ###########################
#            print(scope.currentScope)
        if self.declaration != "":
            self.declaration.checkType(scope)
        return True

        
class Type:
    def __init__(self,type):
        self.type = type

    def printTree(self,tabs):
        string = indent(tabs)+self.type
        return string

    def checkType(self, scope):
        return self.type


class ID:
    def __init__(self,value,comma="",IDrecursion=""):
        self.type = 'id'
        self.value = value
        self.IDrecursion = IDrecursion

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
        if not isinstance(self.IDrecursion,str):
            self.IDrecursion.checkType(scope)
        else:
            if not scope.contains(self.value):
                checkError('undeclared',self.value)
        return self.value


class InstructionBlock:
    def __init__(self,instruction="",semicolon="",instructionBlock=""):
        self.instruction = instruction
        self.semicolon = semicolon
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
        if self.instruction != "":
            self.instruction.checkType(scope)
            if not isinstance(self.instructionBlock, str):
                self.instructionBlock.checkType(scope)
            return True
        return False


class IfInst:
    def __init__(self, If, lparen, expression, rparen, instruction, Else="", elseInstruction=""):
        self.If              = If
        self.lparen          = lparen
        self.expression      = expression
        self.rparen          = rparen
        self.instruction     = instruction
        self.Else            = Else
        self.elseInstruction = elseInstruction

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

#    def checkType(self):
#        if self.expression.opType != 'bool':
#            checkError('condition','if','bool',self.expression.opType)
#            return False

    def checkType(self, scope):
        expresionType = self.expression.checkType(scope)
        if expresionType == "bool":
            if self.instruction.checkType(scope):
                if self.Else != "":
                    if self.elseInstruction.checkType(scope):
                        return True
                return True
            else:
                return False
        return checkError('condition','if','bool',expresionType)

class ForInst:
    def __init__(self,For,Id,Dir,Set,Do,instruction):
        self.For = For
        self.id = Id
        self.dir = Dir
        self.set = Set
        self.Do = Do
        self.instruction = instruction

    def printTree(self,tabs):
        string = indent(tabs)+"FOR\n"
        string += self.id.printTree(tabs+1)
        string += self.dir.printTree(tabs+1)
        string += indent(tabs+1)+"IN\n"
        string += self.set.printTree(tabs+1)
        string += indent(tabs+1)+"DO\n"
        string += self.instruction.printTree(tabs+2)
        return string

    def checkType(self,scope):
        expresionType = self.set.checkType(scope)
        if expresionType == "set":
            return self.instruction.checkType(scope)
        return checkError('condition','for','set',expresionType)

class Direction:
    def __init__(self,direction):
        self.direction = direction

    def printTree(self,tabs):
        string = indent(tabs)+"DIRECTION\n"
        string += indent(tabs+1)+self.direction+"\n"
        return string


class WhileInst:
    def __init__(self,While,lparen,expression,rparen,Do="",instruction=""):
        self.While = While
        self.expression = expression
        self.Do = Do
        self.instruction = instruction

    def printTree(self,tabs):
        string = indent(tabs)+"WHILE\n"
        string += indent(tabs+1)+"condition\n"
        string += self.expression.printTree(tabs+2)
        if not isinstance(self.instruction,str):
            string += indent(tabs)+"DO\n"
            string += self.instruction.printTree(tabs+1)
        return string

    def checkType(self, scope):
        expresionType = self.expression.checkType(scope)
        if expresionType == "bool":
            return self.instruction.checkType(scope)
        
        return checkError('condition','while','bool',expresionType)


class RepeatInst:
    def __init__(self,repeat,instruction,While):
        self.While = While
        self.repeat = repeat
        self.instruction = instruction

    def printTree(self,tabs):
        string = indent(tabs)+"REPEAT\n"
        string += self.instruction.printTree(tabs+1)
        string += self.While.printTree(tabs)
        return string
    
    def checkType(self,scope):
        return True
        

class ScanInst:
    def __init__(self,scan,expression):
        self.scan = scan
        self.expression = expression

    def printTree(self,tabs):
        string = indent(tabs)+"SCAN\n"
        string += self.expression.printTree(tabs+1)
        return string
    
    def checkType(self,scope):
        return True
        

class PrintInst:
    def __init__(self,Print,output):
        self.Print = Print
        self.output = output

    def printTree(self,tabs):
        string = indent(tabs)+"PRINT"+"\n"
        string += indent(tabs+1)+"elements\n"
        string += self.output.printTree(tabs+2)
        if (self.Print == "println"):
            string += String("\"\\n\"").printTree(tabs+2)
        return string
    
    def checkType(self,scope):
        return True
        

class OutputType:
    def __init__(self,expression,comma="",outputRecursion=""):
        self.expression = expression
        self.comma = comma
        self.outputRecursion = outputRecursion

    def printTree(self,tabs):
        string = self.expression.printTree(tabs)
        if not isinstance(self.outputRecursion,str):
            string += self.outputRecursion.printTree(tabs)
        return string
      
    def checkType(self,scope):
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

class Expression:
    def __init__(self,left,op="",right=""):
        self.type  = "expression"
        self.left  = left
        self.right = right
        self.op    = op
        self.opType = None

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
            if self.right == "":
                if (self.op == "-") | (self.op == ">?") | (self.op == "<?") | (self.op == "$?"):
                    self.opType = 'int' 
                elif self.op == 'not':
                    self.opType = 'bool'
            else:
                if self.left == "(" and self.right == ")":
                    self.op.checkType(scope)
                else:
                    if (self.op == "+") | (self.op == "-") | (self.op == "*") | (self.op == "/") | (self.op == "%"): 
                        self.opType = 'int'
                    elif (self.op == "and") | (self.op == "or")| (self.op == "<") | (self.op == ">") | (self.op == "<=") | (self.op == ">=") | (self.op == "==") | (self.op == "/=") | (self.op == "@"):
                        self.opType = 'bool'
                    else:
                        self.opType = 'set'
        else:
            if not isinstance(self.left, str):
                self.opType = self.left.checkType(scope)
        
        return self.opType
        

class Set:
    def __init__(self,lcurly,setNumbers,rcurly):
        self.lcurly = lcurly
        self.setNumbers = setNumbers
        self.rcurly = rcurly

    def printTree(self, tabs):
        string = indent(tabs)+"set\n"
        string += self.setNumbers.printTree(tabs+1)
        return string
        
    def checkType(self,scope):
        return self.setNumbers.checkType(scope)
        

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
        if not isinstance(self.setNumbersRecursion, str):
            string += self.setNumbersRecursion.checkType(scope)
        else: 
            return 'set'

class BooleanValue:
    def __init__(self,value):
        self.value = value

    def printTree(self, tabs):
        string  = indent(tabs)+"bool\n"
        string += indent(tabs+1)+self.value+"\n"
        return string

    def checkType(self,scope):
        return 'bool'
        

class Number:
    def __init__(self,value):
        self.value = value

    def printTree(self,tabs):
        string  = indent(tabs)+"int\n"
        string += indent(tabs+1) + str(self.value) + "\n"
        return string
    
    def checkType(self,scope): 
        return 'int'
        

def checkError(error,inst="",expectedType="",wrongType=""):
    if error == 'condition':
        if (inst == 'if') | (inst == 'while'):
            typeError.append('''ERROR: esperada condicion de tipo "%s", se encontro una de tipo "%s"''' % (expectedType,wrongType)) 
            print(typeError)
    return False


typeError = []
