class Counter:
	def __init__(self, start, end):
		self.num = start
		self.end = end
	
	
	def __iter__(self):
		self._callable = self.__call__()
		return self
	
	
	def __next__(self):
		if self.num > self.end:
			raise StopIteration
		else:
			self.num += 1
			return self.num - 1
	
		pog = self._callable.__next__()
	
	
	def __call__(self):
		print(self.num)
	
	
a = Counter(5,9)


for i in enumerate(a):
	print(i)
