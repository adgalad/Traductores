# -*- coding: utf-8 -*-

class Program:
	def __init__(self,declarations=None,instructions=None):
		self.declarations = declarations
		self.instructions = instructions

	def getValue(self):
		return "reconocio un programa"

class InstructionBlock:
	def __init__(self,inst,sigInst=None):
		self.inst = inst
		self. sigInst = sigInst

class ID:
	def __init__(self,value):
		self.type = 'id'
		self.value = value

	def getValue(self):
		return self.value

class Number:
    def __init__(self,value):
        self.type = 'number'
        self.value = value

    def getValue(self):
        return self.value

class BinaryOp:
    def __init__(self,left,op,right):
        self.type = "binaryOp"
        self.left = left
        self.right = right
        self.op = op

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