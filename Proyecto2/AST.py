# -*- coding: utf-8 -*-


def indent(tabs):
	return "   "*tabs

output = []
class Program:
	def __init__(self,declarations="",instruction=""):
		self.declarations = declarations
		self.instruction = instruction

	def printTree(self,tabs):
		string = indent(tabs)+"PROGRAM\n"
		string += self.instruction.printTree(tabs+1)
		return string


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


class Instruction:
	def __init__(self,instruction = "",Id="",assign="",expression=""):
		self.instruction = instruction
		self.id = Id
		self.assign = assign
		self.expression = expression

	def printTree(self,tabs):
		string =""
		if self.assign == "":
			if isinstance(self.instruction, str):
				string += indent(tabs+1)+self.instruction
			else:
				string += self.instruction.printTree(tabs+1)
		else:
			string += indent(tabs)+"ASSIGN\n"
			string += self.id.printTree(tabs+1) 
			string += indent(tabs+1)+"value\n"
			string += self.expression.printTree(tabs+2)

		return string 



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

class Direction:
	def __init__(self,direction):
		self.direction = direction
		global output
		output += [["DIRECTION\n"],["\t%s" %direction]]


class ForInst:
	#FOR IDENTIFIER direction IDENTIFIER DO instruction
	def __init__(self,For,Id,Dir,Set,Do,instruction):
		self.For = For
		self.id = Id
		self.dir = Dir
		self.set = Set
		self.Do = Do
		self.instruction = instruction

	def printTree(self,tabs):
		string = indent(tabs)+"FOR\n"
		for i in self.Id:
			string += i.printTree(tabs+1)
		string += self.Dir.printTree(tabs+1)
		string += self.Set.printTree(tabs+1)
		string += indent(tabs)+"DO"
		for i in self.instruction:
			string += i.printTree(tabs+1)
		return string


class ID:
	def __init__(self,value,comma="",IDrecursion=""):
		self.type = 'id'
		self.value = value

	def printTree(self,tabs):
		string = indent(tabs)+"variable\n"
		string += indent(tabs+1)+self.value+"\n"
		return string 

class Number:
    def __init__(self,value):
        self.type = 'number'
        self.value = value

    def getValue(self):
        return "int\n\t%d" % int(self.value)

class IfInst:
	def __init__(self):
		pass

class UsingInInst:
	def __init__(self,Using,declaration,In,instruction):
		self.Using = Using
		self.declaration = declaration
		self.In = In
		self.instruction = instruction

	def printTree(self,tabs):
		string = indent(tabs)+"USING\n"
		for i in self.declaration:
			string += i.printTree(tabs+1)
		string += indent(tabs)+"IN\n"
		for i in self.instruction:
			string += i.printTree(tabs+1)

class Number:
	def __init__(self,value):
		self.value = value

	def printTree(self,tabs):
		string  = indent(tabs)+"INT\n"
		string += indent(tabs+1) + str(self.value) + "\n"
		return string

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
	    		string += indent(tabs+1)+self.op
	    		string += self.left.printTree(tabs+1)
	    	else:
	    		string += indent(tabs)+self.op+"\n"
	    		string += self.left.printTree(tabs+1)
	    		string += self.right.printTree(tabs+1)
    	else:
    		if isinstance(self.left, str):
    			string += self.left
    		else:
    			string += self.left.printTree(tabs+1)
    		
    	return string









