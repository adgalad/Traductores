# -*- coding: utf-8 -*-

## Interpretador del lenguaje Setlan.
## Tabla de símbolos
## Autores:  - Mónica Figuera   11-10328
##           - Carlos Spaggiari 11-10987

def indent(tabs):
    return "   "*tabs

class SymbolTable:
	def __init__(self):
		self.previousScope = None
		self.currentScope = {}
		self.innerScopes = []

	def __str__(self):
		return self.printTable(0)

	def printTable(self,tabs):
		string = "SCOPE\n"
		for var in self.currentScope:
			string += indent(tabs+1) + self.currentScope[var].printSymbol()
		for scope in self.innerScopes:
			string += scope.printTable(tabs+1)
		string += "END_SCOPE\n"
		return string

	def insert(self, symbol):
		if not self.contains(symbol.name):
			self.currentScope[symbol.name] = symbol
			return True
		return False

	def delete(self, symbol):
		if self.contains(symbolName):
			del self.currentScope[symbolName]
			return True
		return False

	def update(self, name, type, value):
		if name in self.currentScope:
			self.currentScope[name] = Symbol(name,type,value)
			return True
		elif self.previousScope:
			return self.previousScope.update(name,type,value)
		return False

	def contains(self, symbolName):
		if symbolName in self.currentScope:
			return True
		elif self.previousScope:
			return self.previousScope.contains(symbolName)
		return False

	def lookup(self, symbolName):
		if self.contains(symbolName):
			if symbolName in self.currentScope:
				return self.currentScope[x]			# daba problemas si ponia self.currentScope[symbolName]
		return None


class Symbol(object):

	def __init__(self, name, type, value):
		self.name = name
		self.type = type
		self.value = value

	def printSymbol(self):
		string =  "Variable: %s | Type: %s  | Value: %s\n"%(self.name,self.type,self.value)
		return string