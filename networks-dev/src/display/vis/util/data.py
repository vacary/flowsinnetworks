#
# Auxiliary functions to manage network data

def get_points_from_string_list(str_list):
    
    str_list = str_list[2:-2].replace(' ','').replace("'",'').split('],[')
    points = []

    pos_x = []
    pos_y = []
    for str_point in str_list:
        aux = str_point.split(',')
        point = [float(aux[0]),float(aux[1]),float(aux[2])]    
        points.append(point)
    
    return points

def get_int_array_from_string_list(str_list):

    str_list = str_list[1:-1]
    
    output = [int(elm) for elm in str_list.split(',')]
    
    return output

def getFloatListFromStrList(str_list):

    str_list = str_list[1:-1]
    
    output = [float(elm) for elm in str_list.split(',')]
    
    return output

def get_array_from_string_list(str_list):

    str_list = str_list[1:-1]
    
    output = [float(elm) for elm in str_list.split(',')]
    
    return output
