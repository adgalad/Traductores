# -*- coding: utf-8 -*-

## Interpretador del lenguaje Setlan.
## Tabla de símbolos
## Autores:  - Mónica Figuera   11-10328
##           - Carlos Spaggiari 11-10987

class symbolTable:
	def __init__(self):
		self.previousScope = None
		self.currentScope = {}
		self.innerScopes = []

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

class Symbol:
	def __init__(self, name, type, value):
		self.name = name
		self.type = type
		self.value = value

	def __str__(self):
		return printSymbol()

	def printSymbol(self):
		pass