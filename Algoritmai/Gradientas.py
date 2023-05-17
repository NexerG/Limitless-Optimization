def gradientas(x, y):
	grad_x = -y/8*(2*x+y-1)
	grad_y = -x/8*(x+2*y-1)
	return grad_x, grad_y
