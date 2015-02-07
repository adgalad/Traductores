# -*- coding: utf-8 -*-


def indent(tabs):
	return "   "*tabs

output = []
class Program:
	def __init__(self,declarations="",instructions=""):
		self.declarations = declarations
		self.instructions = instructions
		global output
		output += [["PROGRAM",]]

	def printTree(self,tabs):
		string = indent(tabs)+"PROGRAM\n"
		for i in self.instruction:
			string += i.printTree(tabs+1)
		return string


class Block:
	def __init__(self,lcurly, instruction,rcurly):
		self.rcurly = rcurly
		self.lcurly = lcurly
		self.instruction = instruction

	def printTree(self,tabs):
		string = indent(tabs)+"BLOCK\n"
		for i in self.instruction:
			string += i.printTree(tabs+1)
		string += indent(tabs)+"BLOCK_END\n"


class Instruction:
	def __init__(self,instruction = "",id="",assign="",expression=""):
		self.instruction = instruction
		self.id = id
		self.assign = assign
		self.expression = expression

	def printTree(self,tabs):
		string =""
		for i in self.instruction:
			string += i.printTree(tabs)
		string += self.id  
		string += self.assign 
		for i in self.expression:
			string += i.printTree(tabs)
		return string 

class InstructionBlock:
	def __init__(self,instruction,sigInst,instRec=""):
		self.instruction = instruction
		self. sigInst = sigInst
		self.instRec = instRec

	def printTree(self,tabs):
		string = ""
		for i in self.instruction:
			string += i.printTree(tabs)
		string += self.sigInst
		for i in self.instRec:
			string += i.printTree(tabs)


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
	def __init__(self,value):
		self.type = 'id'
		self.value = value
		global output
		output += [["variable\n","\t%s"%value,]]

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


class Expression:
    def __init__(self,left,op="",right=""):
        self.type  = "expression"
        self.left  = left
        self.right = right
        self.op    = op

    def getValue(self):
        if op == '+':
            return left + right
#     if len(p) == 4:
#         if p[2] == '+':
#             p[0] = p[1] + p[3]
#         elif p[2] == '-':
#             p[0] = p[1] - p[3]
#         elif p[2] == '*':
#             p[0] = p[1] * p[3]
#         elif p[2] == '/':
#             p[0] = p[1] / p[3]