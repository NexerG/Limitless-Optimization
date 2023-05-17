import numpy

def GrcNusileid(funkcija, funkcijos_gradientas, x0y0):
	e = 1e-6
	iteracijos = 0
	xy = x0y0

	while 1:
		iteracijos += 1
		grad = funkcijos_gradientas.kviesti(xy)

		def f_(gamma):
			return funkcija.kviesti((xy[0] + gamma * -(grad[0]), xy[1] + gamma * -(grad[1])))

		def linijos_paieska(funkcija, x, d):
			l = 0 
			r = 1
			e = 1e-6
			tau = (numpy.sqrt(5) - 1) / 2
			d_l = r - l
			x1 = r - d_l * tau
			x2 = l + d_l * tau

			while d_l > e:
				if funkcija(x + x2 * d) < funkcija(x + x1 * d):
					l = x1
					d_l = r - l
					x1 = x2
					x2 = l + d_l * tau
				else:
					r = x2
					d_l = r - l
					x2 = x1
					x1 = r - d_l * tau

			return (l + r) / 2

		zingsnis = linijos_paieska(f_, 0, 1)
		xy_laikinas = (xy[0] - zingsnis * grad[0], xy[1] - zingsnis * grad[1])

		if numpy.linalg.norm((xy[0] - xy_laikinas[0], xy[1] - xy_laikinas[1])) < e:
			break

		xy = xy_laikinas

	return xy, iteracijos

