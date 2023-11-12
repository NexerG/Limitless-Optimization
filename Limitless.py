import numpy
import matplotlib.pyplot as plt
from Algoritmai.Gradientas import gradientas as FGr
from Algoritmai.GradNusileidimas import GradNusileidimas as GrNu
from Algoritmai.GreiciausiasNusileidimas import GrcNusileid as GrcNu
from Algoritmai.DeformuojamasSimpleksas import DefSimplex as DefS

#2110266 A=6, B=6
A = 6 
B = 6
duomenys = [[0, 0], [1, 1], [A / 10, B / 10]]

#Tikslo funkcija
def TFunc(x, y):
	return -1*((1-x-y)*x*y)/8

class Obj1:
	def __init__(self, tikslofunkcija):
		self.Fja = tikslofunkcija
		self.__Own = {}
		self.__CallCount = 0

	def gauti_Own(self):
		return self.__Own

	def GetOwner(self, Own):
		self.__Own = Own

	def call(self, xy, Own = True):
		if not Own:
			return self.Fja(xy[0], xy[1])

		if xy in self.__Own:
			return self.__Own[xy]

		self.__Own[xy] = self.Fja(xy[0], xy[1])
		self.__CallCount += 1
		return self.__Own[xy]

	def CallCount(self):
		return self.__CallCount	
		
	def clear(self):
		self.__Own  ={}
		self.__CallCount = 0

		
class Obj2:
	def __init__(self, tikslofunkcija):
		self.Fja = tikslofunkcija
		self.__Own = {}
		self.__CallCount = 0

	def gauti_Own(self):
		return self.__Own

	def GetOwner(self, Own):
		self.__Own = Own

	def call(self, xy, Own = True):
		if not Own:
			return self.Fja(xy.x, xy.y)

		if xy in self.__Own:
			return self.__Own[xy]

		self.__Own[xy] = self.Fja(xy[0], xy[1])
		self.__CallCount += 1
		return self.__Own[xy]

	def CallCount(self):
		return self.__CallCount
		
	def clear(self):
		self.__Own = {}
		self.__CallCount = 0

#3D vizualization
def plot3d(funkcija): 
	x_reiksmes = (-1, 1) 
	y_reiksmes = (-1, 1)
	xs = numpy.linspace(x_reiksmes[0], x_reiksmes[1], 100)
	ys = numpy.linspace(y_reiksmes[0], y_reiksmes[1], 100)
	xs, ys = numpy.meshgrid(xs, ys)
	zs = numpy.array([funkcija.call((x, y), False) for x, y in zip(xs, ys) ])
	fig = plt.figure()
	ax = fig.add_subplot(111,projection='3d')

	def prideti_taska(ax, x, y, z, color='red', marker='o', size=20, zorder=1):
		ax.scatter(x, y, z, color=color, marker=marker, s=size, zorder=zorder)

	for key in funkcija.gauti_Own().keys():
		prideti_taska(ax, key[0], key[1], funkcija.gauti_Own()[key])

	ax.plot_surface(xs, ys, zs, color='grey')
	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Z')
	plt.show(block=True)

#Gradientinio nusileidimo objektas
GradientoNusileidimas = Obj1(TFunc)
GradGradientoNusileidimas = Obj2(FGr)

#Greiciausio nusileidimo objektas
GreiciausiasNusileidimas = Obj1(TFunc)
GradGreicNusileidimas= Obj2(FGr)

#Simplexo objektas
Simplexas = Obj1(TFunc) 
GradSimplexas= Obj2(FGr)

#Funciju isvedimas
print(' Gradiento nusileidimo algoritmas:')
for xy in duomenys:
	ats, iteracijos = GrcNu(GradientoNusileidimas, GradGradientoNusileidimas, (xy[0],xy[1]))
	print(f' Atsakymas: {ats}')
	print(f' f({ats[0]}, {ats[1]}): {TFunc(ats[0], ats[1])}')
	print(f' Iteracijos: {iteracijos}')
	print(f' funkcija buvo iskviesta {GradientoNusileidimas.CallCount()} kart')
	print(f' gradientas buvo iskviestas {GradGradientoNusileidimas.CallCount()} kart')
	plot3d(GradientoNusileidimas)
	GradientoNusileidimas.clear()
	GradGradientoNusileidimas.clear()
	print(' ')
	
print(' Greiciausio nusileidimo algoritmas:')
for xy in duomenys:
	ats, iteracijos = GrNu(GradGreicNusileidimas, (xy[0],xy[1]), 0.9)
	print(f' Atsakymas: {ats}')
	print(f' f({ats[0]}, {ats[1]}): {TFunc(ats[0], ats[1])}')
	print(f' Iteracijos: {iteracijos}')
	print(f' gradientas buvo kviestas {GradGreicNusileidimas.CallCount()} kart')
	GreiciausiasNusileidimas.GetOwner(GradGreicNusileidimas.gauti_Own())
	plot3d(GreiciausiasNusileidimas)
	GreiciausiasNusileidimas.clear()
	print(' ')

print(' Deformuojamo simplexo algoritmas:')
for xy in duomenys:
	ats, iteracijos = DefS(Simplexas, (xy[0],xy[1]), 0.1)
	print(f' Atsakymas: {ats}')
	print(f' f({ats[0]}, {ats[1]}): {TFunc(ats[0], ats[1])}')
	print(f' Iteracijos: {iteracijos}')
	print(f' funkcija buvo iskviesta {Simplexas.CallCount()} kart')
	plot3d(Simplexas)
	Simplexas.clear()
	print(' ')