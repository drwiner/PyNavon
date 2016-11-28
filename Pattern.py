import numpy as np
import random as rand

class Pattern:
	def __init__(self, name, length, positions, center):
		self.name = name
		self.length = length
		self.positions = positions
		self.center = center

	def astuple(self):
		return (self.length, self.positions, self.center)

	def replaceCenter(self):
		self.center = self.positions[rand.randint(0,self.length)]

A_6 = Pattern(name='A', length=6, positions=np.array([(2,0),(1,1),(3,1), (1,2), (3,2), (0,3), (1,3), (2,3), (3,3), (4,3), (4,3), (0,4), (4,4)]), center=np.array([2,3]))
B_6 = Pattern(name='B', length=6, positions=np.array([(0,0),(1,0),(0,1),(2,1),(0,2),(1,2),(2,2),(3,2),(3,2), (0,3), (3,3),(0,4),(1,4),(2,4)]), center=np.array([0,3]))
C_6 = Pattern(name='C', length=6, positions=np.array([(1,0),(2,0),(0,1),(0,2),(0,3),(1,4),(2,4),(3,0), (3,4)]), center=np.array([0,3]))
D_6 = Pattern(name='D', length=6, positions=np.array([(0,0), (1,0),(2,0), (0,1), (3,1), (0,2), (3,2),(0,3),(3,3), (0,4),(1,4),(2,4)]), center=np.array([3,3]))
E_6 = Pattern(name='E', length=6, positions=np.array([(0,0), (1,0), (2,0), (3,0), (0,1), (0,2), (1,2), (2,2), (0,3), (0,4), (1,4), (2,4), (3,4)]), center=np.array([2,2]))
F_6 = Pattern(name='F', length=6, positions=np.array([(0,0), (1,0), (2,0), (3,0), (0,1), (0,2), (1,2), (2,2), (0,3), (0,4)]), center=np.array([0,1]))
G_6 = Pattern(name='G', length=6, positions=np.array([(0,1), (0,2), (0,3), (1,0), (1,4), (2,0), (2,2), (2,4), (3,0), (3,2), (3,4), (4,0), (4,2), (4,3), (4,4)]), center=np.array([3,2]))
H_6 = Pattern(name='H', length=6, positions=np.array([(0,0), (4,0), (0,1), (4,1), (0,2), (1,2), (2,2), (3,2), (4,2), (0,3), (4,3), (0,4), (4,4)]), center=np.array([4,0]))
I_6 = Pattern(name='I', length=6, positions=np.array([(1,0), (2,0), (3,0), (1,4), (2,4), (3,4), (2,1), (2,2), (2,3)]), center=np.array([4,4]))
J_6 = Pattern(name='J', length=6, positions=np.array([(3,0), (3,1), (3,2), (3,3), (3,4), (2,4), (1,4), (0,3)]), center=np.array([3,3]))
K_6 = Pattern(name='K', length=6, positions=np.array([(0,0), (0,1), (0,2), (0,3), (0,4), (1,2), (2,1), (3,0), (2,3), (3,3), (3,4)]), center=np.array([3,3]))
L_6 = Pattern(name='L', length=6, positions=np.array([(0,0), (0,1), (0,2), (0,3), (0,4), (1,4), (2,4), (3,4)]), center=np.array([0,4]))
M_6 = Pattern(name='M', length=6, positions=np.array([(0,0), (0,1), (1,1), (4,0), (3,1), (4,1), (0,2), (2,2), (4,2), (0,3), (4,3), (0,4), (4,4)]), center=np.array([0,0]))
N_6 = Pattern(name='N', length=6, positions=np.array([(0,0), (4,0), (0,1), (0,2), (0,3), (0,4), (1,1), (2,2), (3,3), (4,4), (4,3), (4,2), (4,1)]), center=np.array([0,1]))
O_6 = Pattern(name='O', length=6, positions=np.array([(1,0), (2,0), (3,0), (0,1), (4,1), (0,2), (4,2), (0,3), (4,3), (1,4), (2,4), (3,4)]), center=np.array([1,4]))
P_6 = Pattern(name='P', length=6, positions=np.array([(0,0), (1,0), (2,0), (0,1), (0,2), (0,3), (0,4), (1,2), (2,2), (3,2), (3,1)]), center=np.array([1,2]))
Q_6 = Pattern(name='Q', length=6, positions=np.array([(1,0), (2,0), (3,0), (0,1), (4,1), (0,2), (4,2), (0,3), (1,4), (4,4), (2,4), (3,3), (2,2)]), center=np.array([1,4]))
R_6 = Pattern(name='R', length=6, positions=np.array([(0,0), (1,0), (2,0), (0,1), (0,2), (0,3), (0,4), (1,2), (2,2), (3,2), (3,1), (2,3), (3,4)]), center=np.array([1,2]))
S_6 = Pattern(name='S', length=6, positions=np.array([(1,0), (2,0), (3,0), (4,0), (0,1), (0,2), (1,2), (2,2), (3,2), (4,2), (4,3), (3,4), (2,4), (1,4), (0,4)]), center=np.array([1,2]))
T_6 = Pattern(name='T', length=6, positions=np.array([(0,0), (1,0), (2,0), (3,0), (4,0), (2,1), (2,2),(2,3),(2,4)]), center=np.array([1,4]))
U_6 = Pattern(name='U', length=6, positions=np.array([(0,0), (0,1), (0,2), (0,3), (1,4), (2,4), (3,4), (4,3), (4,2), (4,1), (4,0)]), center=np.array([4,0]))
V_6 = Pattern(name='V', length=6, positions=np.array([(0,0), (0,1), (4,0), (4,1), (1,2), (3,2), (1,3), (3,3), (2,4)]), center=np.array([2,4]))
W_6 = Pattern(name='W', length=6, positions=np.array([(0,0), (0,1), (0,2), (0,3), (1,4), (2,3), (2,2), (3,4), (4,3), (4,2), (4,1), (4,0)]), center=np.array([4,0]))
X_6 = Pattern(name='X', length=6, positions=np.array([(0,0), (1,1), (2,2), (3,3), (4,4), (4,0), (3,1), (1,3), (0,4)]), center=np.array([0,4]))
Y_6 = Pattern(name='Y', length=6, positions=np.array([(0,0), (1,1), (2,2), (2,3), (2,4), (3,1), (4,0)]), center=np.array([4,0]))
Z_6 = Pattern(name='Z', length=6, positions=np.array([(0,0), (1,0), (2,0), (3,0), (4,0), (4,1), (3,2), (2, 2), (1, 3), (0,4), (1,4), (2,4), (3,4), (4,4)]), center=np.array([4,4]))

alphabet = [A_6, B_6, C_6, D_6, E_6, F_6, G_6, H_6, I_6, J_6, K_6, L_6, M_6, N_6, O_6, P_6, Q_6, R_6, S_6, T_6, U_6, V_6, W_6, X_6, Y_6, Z_6]

pat_A = Pattern(name='A', length=12, positions=np.array([(5,0),(6,0),(5,1),(6,1),(4,2),(5,2),(6,2),(7,2),(4,3),(5,3),(6,3),(7,3),(3,4),(4,4),(7,4),(8,4),(3,5),(4,5),(7,5),(8,5),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6),(8,6),(9,6),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),(8,7),(9,7),(1,8),(2,8),(9,8),(10,8),(1,9),(2,9),(9,9),(10,9),(0,10),(1,10),(10,10),(11,10),(0,11),(1,11),(10,11),(11,11)]),center=np.array([5, 0]))

pat_C = Pattern(name='C', length=12, positions=np.array([(0,4),(0,5),(0,6),(0,7),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(2,2),(2,3),(2,4),(2,7),(2,8),(2,9),(3,1),(3,2),(3,3),(3,8),(3,9),(3,10),(4,0),(4,1),(4,2),(4,9),(4,10),(4,11),(5,0),(5,1),(6,0),(6,1),(7,0),(7,1),(8,0),(8,1),(5,11),(5,10),(6,11),(6,10),(7,11),(7,10),(8,11),(8,10),(9,11),(9,10),(9,9),(10,10),(10,9),(10,8),(9,0),(9,1),(9,2),(9,3),(9,8),(10,1),(10,2),(10,3)]), center=np.array([5, 0]))

pat_T = Pattern(name='T', length=12, positions=np.array([(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1),(10,1),(1,2),(10,2),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7),(5,8),(5,9),(5,10),(6,2),(6,3),(6,4),(6,5),(6,6),(6,7),(6,8),(6,9),(6,10),(3,10),(4,9),(4,10),(7,9),(7,10),(8,10)]),center=np.array([5, 0]))

pat_hyphen = Pattern(name='hyphen', length=12, positions=np.array([(i, 5) for i in range(1, 12)] + [(i, 6) for i in range(1, 12)]), center=np.array([6, 6]))
pat_full = Pattern(name='full', length=12, positions=np.array([(i, j) for i in range(12) for j in range(12)]), center=np.array([6,6]))

class WORD:
	wd = alphabet

	def __len__(self):
		return len(self.wd)

	def __getitem__(self, pos):
		return self.wd[pos]

	def replaceCenters(self):
		for wd in self.wd:
			wd.replaceCenter()

	def wd_lens(self):
		return [self.wd[i].length for i in range(len(self))]

	def get_size(self, i, top_level):
		lengths = self.wd_lens()
		total = 1
		for j in range(i):
			total *= lengths[(top_level + j) % len(self)]
		return total