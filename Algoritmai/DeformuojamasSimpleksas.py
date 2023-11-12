import numpy
	
def DefSimplex(funkcija, x0y0, a):
	e = 1e-6
	iteracijos = 0
	n = len(x0y0)

	simplexas = numpy.zeros((n + 1, n))
	simplexas[0] = numpy.array([ x0y0[0], x0y0[1] ])

	d1 = (numpy.sqrt(n + 1) + n - 1) / (n * numpy.sqrt(2)) * a
	d2 = (numpy.sqrt(n + 1) - 1) / (n * numpy.sqrt(2)) * a

	for i in range(1, n + 1):
		for j in range(n):
			if i == j + 1:
				simplexas[i][j] = simplexas[0][j] + d2
			else:
				simplexas[i][j] = simplexas[0][j] + d1

	while True:
		iteracijos += 1
		blogiausia = 0
		geresne = 0

		for i in range(1, n + 1):
			if funkcija.call((simplexas[i][0], simplexas[i][1])) > funkcija.call((simplexas[blogiausia][0], simplexas[blogiausia][1])):
				blogiausia = i

			if funkcija.call((simplexas[i][0], simplexas[i][1])) < funkcija.call((simplexas[geresne][0], simplexas[geresne][1])):
				geresne = i

		xc = numpy.zeros(n)

		for i in range(n + 1):
			if i != blogiausia:
				xc += simplexas[i]

		xc /= n
		xr = -simplexas[blogiausia] + 2 * xc

		if funkcija.call((xr[0], xr[1])) < funkcija.call((simplexas[blogiausia][0], simplexas[blogiausia][1])):
			simplexas[blogiausia] = xr
		else:
			xc = (simplexas[blogiausia] + xc) / 2

			for i in range(n + 1):
				if i != blogiausia:
					simplexas[i] = (simplexas[i] + simplexas[blogiausia]) / 2

				if funkcija.call((simplexas[i][0], simplexas[i][1])) < funkcija.call((simplexas[geresne][0], simplexas[geresne][1])):
					geresne = i

			if funkcija.call((xr[0], xr[1])) < funkcija.call((simplexas[geresne][0], simplexas[geresne][1])):
				simplexas[blogiausia] = xr
			else:
				for i in range(n + 1):
					if i != geresne:
						simplexas[i] = (simplexas[i] + simplexas[geresne]) / 2

					if funkcija.call((simplexas[i][0], simplexas[i][1])) < funkcija.call((simplexas[geresne][0], simplexas[geresne][1])):
						geresne = i

		if numpy.linalg.norm(simplexas[blogiausia] - simplexas[geresne]) < e:
			break

	return (simplexas[geresne][0], simplexas[geresne][1]), iteracijos

