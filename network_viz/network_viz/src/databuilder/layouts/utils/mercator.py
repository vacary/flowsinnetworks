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
# Mercator transformation functions
#
import math

def merc_x(lon):
    
    r_major = 6378137.000
    
    return r_major*math.radians(lon)/100.0
 
def merc_y(lat):
    
    if lat > 89.5:lat = 89.5
    if lat < -89.5:lat = -89.5
    r_major = 6378137.000
    r_minor = 6356752.3142
    temp = r_minor/r_major
    eccent = math.sqrt(1-temp**2)
    phi = math.radians(lat)
    sinphi = math.sin(phi)
    con = eccent*sinphi
    com = eccent/2
    con = ((1.0-con)/(1.0+con))**com
    ts = math.tan((math.pi/2-phi)/2)/con
    y = 0-r_major*math.log(ts)
    
    return y/100.0
