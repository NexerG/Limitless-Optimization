import numpy
import matplotlib.pyplot as plt
from Algoritmai.Gradientas import gradientas as FGr
from Algoritmai.GradNusileidimas import GradNusileidimas as GrNu
from Algoritmai.GreiciausiasNusileidimas import GrcNusileid as GrcNu
from Algoritmai.DeformuojamasSimpleksas import DefSimplex as DefS

#2110266 A=6, B=0
A = 6 
B = 6
duomenys = [[0, 0], [1, 1], [A / 10, B / 10]]

#Tikslo funkcija
def TFunc(x, y):
	return -1*((1-x-y)*x*y)/8

class FloatFunWrapper: #kodas ir tai netvarkingas todel aptvarkau ji su funkciju aplanku <- sitas grazina float values
	def __init__(self, tikslofunkcija):
		self.__funkcija = tikslofunkcija
		self.__talpykla = {}
		self.__kvietimai = 0

	def gauti_talpykla(self):
		return self.__talpykla

	def nustatyti_talpykla(self, talpykla):
		self.__talpykla = talpykla

	def kviesti(self, xy, talpykla = True):
		if not talpykla:
			return self.__funkcija(xy[0], xy[1])

		if xy in self.__talpykla:
			return self.__talpykla[xy]

		self.__talpykla[xy] = self.__funkcija(xy[0], xy[1])
		self.__kvietimai += 1
		return self.__talpykla[xy]

	def kvietimai(self):
		return self.__kvietimai	

class TupleFunWrapper: #kodas ir tai netvarkingas todel aptvarkau ji su funkciju aplanku <- sitas grazina Tuple values
	def __init__(self, tikslofunkcija):
		self.__funkcija = tikslofunkcija
		self.__talpykla = {}
		self.__kvietimai = 0

	def gauti_talpykla(self):
		return self.__talpykla

	def nustatyti_talpykla(self, talpykla):
		self.__talpykla = talpykla

	def kviesti(self, xy, talpykla = True):
		if not talpykla:
			return self.__funkcija(xy.x, xy.y)

		if xy in self.__talpykla:
			return self.__talpykla[xy]

		self.__talpykla[xy] = self.__funkcija(xy[0], xy[1])
		self.__kvietimai += 1
		return self.__talpykla[xy]

	def kvietimai(self):
		return self.__kvietimai

#3D vizualization
def plot3d(funkcija): 
	x_reiksmes = (-1, 1) 
	y_reiksmes = (-1, 1)
	xs = numpy.linspace(x_reiksmes[0], x_reiksmes[1], 100)
	ys = numpy.linspace(y_reiksmes[0], y_reiksmes[1], 100)
	xs, ys = numpy.meshgrid(xs, ys)
	zs = numpy.array([funkcija.kviesti((x, y), False) for x, y in zip(xs, ys) ])
	fig = plt.figure()
	ax = fig.add_subplot(111,projection='3d')

	def prideti_taska(ax, x, y, z, color='red', marker='o', size=20, zorder=1):
		ax.scatter(x, y, z, color=color, marker=marker, s=size, zorder=zorder)

	for key in funkcija.gauti_talpykla().keys():
		prideti_taska(ax, key[0], key[1], funkcija.gauti_talpykla()[key])

	ax.plot_surface(xs, ys, zs, color='yellow')
	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Z')
	plt.show(block=True)

#Gradientinio nusileidimo objektas
GradientoNusileidimas = FloatFunWrapper(TFunc)
GradGradientoNusileidimas = TupleFunWrapper(FGr)

#Greiciausio nusileidimo objektas
GreiciausiasNusileidimas = FloatFunWrapper(TFunc)
GradGreicNusileidimas= TupleFunWrapper(FGr)

#Simplexo objektas
Simplexas = FloatFunWrapper(TFunc)
GradSimplexas= TupleFunWrapper(FGr)

#Funciju isvedimas
print(' Gradiento nusileidimo algoritmas:')
for xy in duomenys:
	ats, iteracijos = GrcNu(GradientoNusileidimas, GradGradientoNusileidimas, (xy[0],xy[1]))
	print(f' Atsakymas: {ats}')
	print(f' f({ats[0]}, {ats[1]}): {TFunc(ats[0], ats[1])}')
	print(f' Iteracijos: {iteracijos}')
	print(f' funkcija buvo iskviesta {GradientoNusileidimas.kvietimai()} kart')
	print(f' gradientas buvo iskviestas {GradGradientoNusileidimas.kvietimai()} kart')
	plot3d(GradientoNusileidimas)
	print(' ')
	
print(' Greiciausio nusileidimo algoritmas:')
for xy in duomenys:
	ats, iteracijos = GrNu(GradGreicNusileidimas, (xy[0],xy[1]), 0.9)
	print(f' Atsakymas: {ats}')
	print(f' f({ats[0]}, {ats[1]}): {TFunc(ats[0], ats[1])}')
	print(f' Iteracijos: {iteracijos}')
	print(f' gradientas buvo kviestas {GradGreicNusileidimas.kvietimai()} kart')
	GreiciausiasNusileidimas.nustatyti_talpykla(GradGreicNusileidimas.gauti_talpykla())
	plot3d(GreiciausiasNusileidimas)
	print(' ')

print(' Deformuojamo simplexo algoritmas:')
for xy in duomenys:
	ats, iteracijos = DefS(Simplexas, (xy[0],xy[1]), 0.1)
	print(f' Atsakymas: {ats}')
	print(f' f({ats[0]}, {ats[1]}): {TFunc(ats[0], ats[1])}')
	print(f' Iteracijos: {iteracijos}')
	print(f' funkcija buvo iskviesta {Simplexas.kvietimai()} kart')
	plot3d(Simplexas)
	print(' ')