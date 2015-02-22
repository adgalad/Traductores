

class symbolTable:
	def __init__(self):
		self.previusScope = None
		self.currentScope = {}
		innerScopes = []

	def insert(self, symbol):
		if not self.contains(symbol.name):
			self.currentScope[symbol.name] = symbol
			return True
		return False

	def delete(self, symbol):
		if self.contains(symbolName):
			del self.currentScope[symbolName]

	def update(self):
		pass

	def contains(self, symbolName):
		if symbolName in self.currentScope:
			return True
		elif self.previusScope:
			return self.previusScope.contains(symbolName)
		return False

	def lookup(self, symbolName):
		if self.contains(symbolName):
			return self.currentScope[symbolName]
		return None





class symbol:
	def __init__(self, name, type, value):
		self.name = name
		self.type = type
		self.value = value

	def __str__(self):
		return printSymbol()

	def printSymbol(self):
		pass

