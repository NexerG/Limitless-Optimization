import numpy

def GradNusileidimas(gradientas, x0y0, zingsnis):
	e = 1e-6
	iteracijos = 0
	xy = x0y0

	while 1:
		iteracijos += 1

		z = gradientas.call(xy)
		x_laikinas = xy[0] + zingsnis * z[0]
		y_laikinas = xy[1] + zingsnis * z[1]
		xy_laikinas = (x_laikinas, y_laikinas)

		norm = numpy.linalg.norm([ xy[0] - xy_laikinas[0], xy[1] - xy_laikinas[1] ])
		if norm < e:
			break

		xy = xy_laikinas

	return xy, iteracijos