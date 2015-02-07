# -*- coding: utf-8 -*-



class Program:
	def __init__(self,declarations"",instructions""):
		self.declarations = declarations
		self.instructions = instructions

	def getValue(self):
		return "PROGRAM"

class InstructionBlock:
	def __init__(self,inst,sigInst,instRec""):
		self.inst = inst
		self. sigInst = sigInst

class Direction:
	def __init__(self,direction):
		self.direction = direction

	def getValue(self):
		return "direction\n\t%s" %self.direction


class For:
	def __init__(self):
		print "entra"
		pass

	def getValue(self):
		print "sale"
		return "FOR\n\t"

class ID:
	def __init__(self,value):
		self.type = 'id'
		self.value = value

	def getValue(self):
		return "variable\n\t%d" % self.variable

class Number:
    def __init__(self,value):
        self.type = 'number'
        self.value = value

    def getValue(self):
        return "int\n\t%d" % int(self.value)

class IfInst:
	def __init__(self):
		pass

class BinaryOp:
    def __init__(self,left,op"",right""):
        self.type  = "binaryOp"
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