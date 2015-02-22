

class symbolTable:
	def __init__(self):
		self.previousScope = None
		self.currentScope = {}
		innerScopes = []

	def insert(self, symbol):
		if not self.contains(symbol.name):
			self.currentScope[symbol.name] = symbol

	def delete(self, symbol):
		if self.contains(symbolName):
			del self.currentScope[symbolName]

	def update(self, name, type, value):
		if name in self.currentScope:
			self.currentScope[name] = symbol

	def contains(self, symbolName):
		if symbolName in self.currentScope:
			return True
		elif self.previousScope:
			return self.previousScope.contains(symbolName)
		return False

	def lookup(self, symbolName):
		if self.contains(symbolName):
			return self.currentScope[symbolName]
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

