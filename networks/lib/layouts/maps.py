'''

Map data functions

'''

import os, sys

from lxml import etree
import networkx as nx
from numpy import * 
import math
import random

# Scaled MERCATOR functions (http://wiki.openstreetmap.org/wiki/Mercator)

def merc_x(lon):
    r_major=6378137.000
    return r_major*math.radians(lon)/100000.0
 
def merc_y(lat):
    if lat>89.5:lat=89.5
    if lat<-89.5:lat=-89.5
    r_major=6378137.000
    r_minor=6356752.3142
    temp=r_minor/r_major
    eccent=math.sqrt(1-temp**2)
    phi=math.radians(lat)
    sinphi=math.sin(phi)
    con=eccent*sinphi
    com=eccent/2
    con=((1.0-con)/(1.0+con))**com
    ts=math.tan((math.pi/2-phi)/2)/con
    y=0-r_major*math.log(ts)
    return y/100000.0

def get_graphFromOSMFile2(osm_file_path, time_step):

    datalist = osm2graphData(osm_file_path)
    
    nodes_data = datalist[2]
    edges_data = datalist[3]
        
    G=nx.MultiDiGraph()
        
    for node_data in nodes_data:
        G.add_node(node_data[0],pos = [node_data[3][0],node_data[3][1],0.0])
        
    for edge_data in edges_data:
        nstart  = edge_data[0]
        nend    = edge_data[1]
        
        listOfEdgeOSMPoints = edge_data[-1]
        
        points = []
        for osm_node in listOfEdgeOSMPoints:
            point = translatorNodePos(osm_node, datalist[0], datalist[1])
            points.append(point)
                
        # non-real time and capacity
        aux_time                = 1 + 2*random.random()
        aux_capacity            = 0.25 + 5*random.random()

        time = aux_time        
        output, keys = getEdgeGeometryAndKeys(points,time,time_step)        
        str_geometry            = str(output)
        str_geometry_keys       = str(keys)
                
        G.add_edge(nstart,nend, time = aux_time, capacity = aux_capacity, geometry = str_geometry, geometry_keys = str_geometry_keys )
    
    return G


def get_graphFromOSMFile(osm_file_path):
    
    datalist = osm2graphData(osm_file_path)
    
    nodes_data = datalist[2]
    edges_data = datalist[3]
        
    G=nx.MultiDiGraph()
        
    for node_data in nodes_data:
        G.add_node(node_data[0],pos = [node_data[3][0],node_data[3][1],0.0])
        
    for edge_data in edges_data:
        nstart  = edge_data[0]
        nend    = edge_data[1]
        
        listOfEdgeOSMPoints = edge_data[-1]
        
        points = []
        for osm_node in listOfEdgeOSMPoints:
            point = translatorNodePos(osm_node, datalist[0], datalist[1])
            points.append(point)
        
        time = 1.0
        time_step = 0.1
        
        output, keys = getEdgeGeometryAndKeys(points,time,time_step)        
        
        # non-real time and capacity
        aux_time                = 1 + 2*random.random()
        aux_capacity            = 0.1 + 5*random.random()
        str_geometry            = str(output)
        str_geometry_keys       = str(keys)
        
        G.add_edge(nstart,nend, time = aux_time, capacity = aux_capacity, geometry = str_geometry, geometry_keys = str_geometry_keys )
    
    return G


def osm2graphData(osm_file_path):
    
    # Process OSM data
    
    context = etree.iterparse(osm_file_path,events=('start','end'))
    event, root = context.next()
    
    nd_idList = []
    nd_posX = []
    nd_posY = []
    nd_type = []
    
    w_listOfNodes = []
    w_listOfWays = []
    w_capacity = []
    w_distance = []
    w_speed = []
    
    ncounter = 0
    wcounter = 0 
    wflag = 0
    nflag = 0
    for event, elem in context:
    
        if event == 'start' and elem.tag=='node':
            
            nd_idList.append(elem.attrib['id'])
            
            auxPosX = float(elem.attrib['lon'])
            auxPosY = float(elem.attrib['lat'])
            
            #posX = auxPosX 
            #posY = auxPosY 
            
            posX = merc_x(auxPosX)
            posY = merc_y(auxPosY)
            
            nd_posX.append(float(posX))
            nd_posY.append(float(posY))
            
            ncounter = ncounter + 1
            
            nflag = 1
            nd_type.append('regular')
        
        if nflag == 1:
            
            if event == 'start' and elem.tag=='tag':
                
                key = elem.attrib['k']
                val = elem.attrib['v']
                
                if (key == 'type'):
                    if (val == 'source'):
                        nd_type[-1] = 'source'
                    if (val == 'sink'):
                        nd_type[-1] = 'sink'
                
                nflag = 0
        
        if event == 'start' and elem.tag=='way':
            
            wflag = 1
            
        if wflag == 1:
            
            if (event == 'start' and elem.tag == 'nd'):
                
                w_listOfNodes.append(elem.attrib['ref'])
            
            if (event == 'start' and elem.tag == 'tag'):
                
                if (elem.attrib['k']=='distance'):
                    w_distance.append(elem.attrib['v'])
                    
                if (elem.attrib['k']=='capacity'):
                    w_capacity.append(elem.attrib['v'])
                
                if (elem.attrib['k']=='speed'):
                    w_speed.append(elem.attrib['v'])    
                
        if (event == 'end' and elem.tag=='way'):
            
            w_listOfWays.append(w_listOfNodes)        
            w_listOfNodes = []
            wflag = 0
        
        elem.clear()
        
    # Clear data and generate lists of nodes and edges data
    
    listOfNodes     = []
    
    for way in w_listOfWays:
        
        listOfNodes.append(way[0])
        listOfNodes.append(way[-1])
        
    listOfNodes = sorted(set(listOfNodes))
    
    ##
    # Data for nodes
    #
    listOfNodes_data = []
    ncounter = 0    
    
    listOfIDLabels = range(len(listOfNodes))
    translateID_OSM = []
    translateID_ID = []
    for node in listOfNodes:
        
        c = nd_idList.index(node)
        
        node_osm_id = node
        node_type   = nd_type[c] 
        node_pos    = [float(nd_posX[c]),float(nd_posY[c]),0.0]
        
        if (node_type == 'source'):
            slabel = 0
        elif (node_type == 'sink'):
            slabel = 1
        else: 
            slabel = listOfIDLabels[-1]
        
        listOfIDLabels.remove(slabel)
        
        node_id = slabel
        
        translateID_OSM.append(node_osm_id)
        translateID_ID.append(node_id)
        
        #### LIST OF NODES DATA
        listOfNodes_data.append([node_id,node_osm_id,node_type,node_pos])
        
        ncounter = ncounter + 1        
    
    ##
    # Data for edges
    #
    listOfEdge_data =[]
    
    for way in w_listOfWays:
        
        c = w_listOfWays.index(way)
        
        osm_id_node_start = way[0]
        osm_id_node_end = way[-1]
        
        node_start_id = translateID_ID[translateID_OSM.index(osm_id_node_start)]
        node_end_id = translateID_ID[translateID_OSM.index(osm_id_node_end)]
        way_capacity = w_capacity[c] 
        way_distance = w_distance[c]
        way_speed = w_speed[c]
        way_listOfNodes = way
        
        
        #### LIST OF EDGE DATA
        listOfEdge_data.append([node_start_id, node_end_id,way_distance,way_speed,way_capacity,way_listOfNodes])


    fullListOfNodes = []
    fullListOfPositions = []
    
    c = 0
    for node in nd_idList:
        fullListOfNodes.append(node)
        fullListOfPositions.append([float(nd_posX[c]),float(nd_posY[c]),0.0])
        c = c + 1
    
    return [fullListOfNodes,fullListOfPositions,listOfNodes_data,listOfEdge_data]

def translatorNodePos(node,fullListOfNodes,fullListOfPos):
    
    c = fullListOfNodes.index(node)
    
    return fullListOfPos[c]

def getEdgeGeometryAndKeys(listOfTranslatedEdgePoints,time,time_step):
    
    points = listOfTranslatedEdgePoints
    
    # start with point analysis
    numberOfDivisionsForEdge = int(floor(time/time_step))
    
    total_dist = 0
    for i in xrange(len(points)-1):
        pi = array(points[i])
        pi1 = array(points[i+1])
        total_dist = total_dist + linalg.norm(pi1 - pi)
     
    delta_dist = total_dist/(1.0*numberOfDivisionsForEdge)
    
    k       = 0
    p       = array(points[k])
    dif     = array(points[k+1]) - array(points[k])
    ndif    = linalg.norm(dif)
    u       = dif/ndif
    step    = delta_dist
     
    total_drec = 0
    drec = 0
    counter = 0
    
    output = []
    keys = [0]
    output.append(points[0])
    while (abs(total_drec - total_dist) > 1E-10):
        q       = p + step*u
        drec    = drec + linalg.norm(q - p)
        if (drec > ndif and k < len(points)-2):
            k           = k + 1
            prev        = p
            p           = array(points[k])
            output.append([p[0],p[1],p[2]])
            drec        = 0
            dif         = array(points[k+1]) - array(points[k])
            ndif        = linalg.norm(dif)
            u           = dif/ndif
            step        = linalg.norm(p - q)
        else:
            output.append([q[0],q[1],q[2]])
            keys.append(len(output)-1)
            total_drec  = total_drec + delta_dist
            p           = q
            step        = delta_dist
        counter = counter + 1
    
    #output.append(points[-1])

    return [output,keys]
