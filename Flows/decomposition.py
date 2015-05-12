from math import *

def decomposition(f,a,h,t):
	"Decompose function f in steps of size h"
	return f(floor((t-a)/h)*h+a)

def g(t):
	return (sin(t))

def build_inputflow(f,a,b,h):
	n=int((b-a)/h)+1
	timeofevent=[]	
	inputflow=[]
	for i in range (n):
		inputflow.append(f(a+i*h))
		timeofevent.append(i*h)

	return timeofevent, inputflow

