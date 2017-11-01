# flowsinnetworks is a program dedicated to modeling and simulation
# of dynamic equilibrium of flows in networks
#
# Copyright 2016 INRIA, INRIA Chile
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# contact vincent.acary@inria.fr
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

