class Square:
	def __init__(self, length=1):
		self._length = length
	
	@property
	def length(self):
		print("Getting length")
		return self._length
	
	
	@length.setter
	def length(self, a):
		print("Setting length")
		self._length = a
	
	
	@length.deleter
	def length(self):
		print("Deleting length")
		del self._length
		

a = Square(3)
print(a.length)
a.length = 5
print(a.length)
del a.length
print(a.length)
