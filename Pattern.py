import numpy as np

class Pattern:
	def __init__(self, name, length, positions, center):
		self.name = name
		self.length = length
		self.positions = positions
		self.center = center

	def astuple(self):
		return (self.length, self.positions, self.center)


pat_A = Pattern(name='A', length=12, positions=np.array([(5,0),(6,0),(5,1),(6,1),(4,2),(5,2),(6,2),(7,2),(4,3),(5,3),(6,3),(7,3),(3,4),(4,4),(7,4),(8,4),(3,5),(4,5),(7,5),(8,5),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6),(8,6),(9,6),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),(8,7),(9,7),(1,8),(2,8),(9,8),(10,8),(1,9),(2,9),(9,9),(10,9),(0,10),(1,10),(10,10),(11,10),(0,11),(1,11),(10,11),(11,11)]),center=np.array([5, 0]))

pat_C = Pattern(name='C', length=12, positions=np.array([(0,4),(0,5),(0,6),(0,7),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(2,2),(2,3),(2,4),(2,7),(2,8),(2,9),(3,1),(3,2),(3,3),(3,8),(3,9),(3,10),(4,0),(4,1),(4,2),(4,9),(4,10),(4,11),(5,0),(5,1),(6,0),(6,1),(7,0),(7,1),(8,0),(8,1),(5,11),(5,10),(6,11),(6,10),(7,11),(7,10),(8,11),(8,10),(9,11),(9,10),(9,9),(10,10),(10,9),(10,8),(9,0),(9,1),(9,2),(9,3),(9,8),(10,1),(10,2),(10,3)]), center=np.array([5, 0]))

pat_T = Pattern(name='T', length=12, positions=np.array([(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1),(10,1),(1,2),(10,2),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7),(5,8),(5,9),(5,10),(6,2),(6,3),(6,4),(6,5),(6,6),(6,7),(6,8),(6,9),(6,10),(3,10),(4,9),(4,10),(7,9),(7,10),(8,10)]),center=np.array([5, 0]))

pat_hyphen = Pattern(name='hyphen', length=12, positions=np.array([(i, 5) for i in range(1, 12)] + [(i, 6) for i in range(1, 12)]), center=np.array([6, 6]))
pat_full = Pattern(name='full', length=12, positions=np.array([(i, j) for i in range(12) for j in range(12)]), center=np.array([6,6]))

class WORD:
	wd = [pat_A, pat_C, pat_T]
	def __len__(self):
		return len(self.wd)

	def __getitem__(self, pos):
		return self.wd[pos]