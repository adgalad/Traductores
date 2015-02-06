# -*- coding: utf-8 -*-


output = []
class Program:
	def __init__(self,declarations=None,instructions=None):
		self.declarations = declarations
		self.instructions = instructions
		global output
		output += ["PROGRAM"]

class Block:
	def __init__(self,lcurly, instruction,rcurly):
		self.rcurly = rcurly
		self.lcurly = lcurly
		self.instruction = instruction
		global output
		output += ["BLOCK"]

class Instruction:
	def __init__(self,instruction = None,id=None,assign=None,expression=None):
		self.instruction = instruction
		self.id = id
		self.assign = assign
		self.expression = expression

class InstructionBlock:
	def __init__(self,inst,sigInst,instRec=None):
		self.inst = inst
		self. sigInst = sigInst


class Direction:
	def __init__(self,direction):
		self.direction = direction
		global output
		output += ["DIRECTION\n\t%s" %direction]


class For:
	#FOR IDENTIFIER direction IDENTIFIER DO instruction
	def __init__(self,For,id,dir,set,do,instruction):
		global output
		output += ["FOR"]


class ID:
	def __init__(self,value):
		self.type = 'id'
		self.value = value
		global output
		output += ["variable\n\t%s"%value]

class Number:
    def __init__(self,value):
        self.type = 'number'
        self.value = value

    def getValue(self):
        return "int\n\t%d" % int(self.value)

class IfInst:
	def __init__(self):
		pass

class Expression:
    def __init__(self,left,op=None,right=None):
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