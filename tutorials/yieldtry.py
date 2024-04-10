class A:
	def __init__(self):
		self.a = ["1","2","3","4"]
		self.num = 0
	
	
	def __iter__(self):
		self._callabe = self.__call__()
		return self
	
	
	def __next__(self):
		batch = self._callable.__next__()
		
		if batch is None:
			raise StopIteration
		
		return batch
	
	
	def __call__(self):
		self.a
		#for i in range(len(a)):
			#yield a[i]
		
		return None
		

opa = A()

for i,a in enumerate(A):
	print(i)
	print(a)
