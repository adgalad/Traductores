
import ply.lex as lex

class AFD:
	transiciones = [[]]
	
	
	def __init__(self):
		self.transiciones += [
		 #0
		 [[1,"Program"]]
		 #1
		 [[2,"OpenCurly"]]
		 #2
		 [[3,"Comment"],[4,"Int"],[5,"Char"],[6,"Bool"],[9,"CloseCurly"],[10,"Id"]]
		 #3
		 [[2,"NewLine"]]
		 #4
		 [[7,"Id"]]
		 #5
		 [[7,"Id"]]
		 #6
		 [[7,"Id"]]
		 #7				
		 [[2,"Semicolon"],[8,"Comma"]]	
		 #8
		 [[7,"Id"]]
		 #9
		 [[-1,"Fin"]]
		 #10
		 [[11,"Equals"]]
		 #11
		 [[2,"Semicolon"],[12,"Id"],[13,"Number"],[14,"Quote"],[16,"SimpleQuote"]]
		 #12
		 [[11,["Plus","Minus","Times","Divide"]]
		 #13
		 [[11,["Plus","Minus","Times","Divide"]]
		 #14
		 [[15,"String"]]
		 #15
		 [[11,"Quote"]]
		 #16
		 [[17,"String"]]
		 #17
		 [[11,"SimpleQuote"]]
		 #18
		 [[18,""]]
		 #19
		 [[19,""]]
		 #20
		 [[21,"Quote"]]
		 #21
		 [[22,"String"]]
		 #22
		 [[25,"Quote"]]
		 #23
		 [[24,"String"]]
		 #24
		 [[25,"SimpleQuote"]]
		 #25
		 [[20,"Comma"][2,"Semicolon"]]
		 #26
		 [[20,"Comma"],[2,"Semicolon"]]
		 #27
		 [[22,"String"]]
		 #28
		 [[25,"Quote"]]
		]
		