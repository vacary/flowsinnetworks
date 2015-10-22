
import numpy as np
import scipy.interpolate as interpolate
#import matplotlib.pyplot as plt

def getPointsFromBSplineInterpolation(controlPoints,degree,numberOfPoints):

    controlPoints = np.array(controlPoints)
    n_points = len(controlPoints)
    x = controlPoints[:,0]
    y = controlPoints[:,1]
    
    t = range(len(x))
    ipl_t = np.linspace(1.0, len(controlPoints) - degree,numberOfPoints)
    
    x_tup = interpolate.splrep(t, x, k=degree, per=1)
    y_tup = interpolate.splrep(t, y, k=degree, per=1)
    x_list = list(x_tup)
    xl = x.tolist()
    x_list[1] = [0.0] + xl + [0.0, 0.0, 0.0, 0.0]
    
    y_list = list(y_tup)
    yl = y.tolist()
    y_list[1] = [0.0] + yl + [0.0, 0.0, 0.0, 0.0]
    
    x_i = interpolate.splev(ipl_t, x_list)
    y_i = interpolate.splev(ipl_t, y_list)
    
    output = []
    
    output.append([controlPoints[0][0],controlPoints[0][1],0.0])
    
    for c in xrange(len(x_i)):
        point = [x_i[c],y_i[c],0.0]
        output.append(point)
        
    output.append([controlPoints[-1][0],controlPoints[-1][1],0.0])
    
    return output

def getControlPointsFromGVizData(geometry):
    
    geometry_list = geometry[3:-3].replace(' ','').replace("'",'').split('],[')
    controlPoints = []

    pos_x = []
    pos_y = []
    for str_point in geometry_list:
        aux = str_point.split(',')
        point = [float(aux[0]),float(aux[1])]    
        controlPoints.append(point)
    
    return controlPoints


