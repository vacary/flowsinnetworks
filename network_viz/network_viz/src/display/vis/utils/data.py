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
