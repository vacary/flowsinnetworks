'''

Map data functions

'''

import os, sys

from lxml import etree
import networkx as nx
from numpy import * 
import random

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
        
        # non-real time and capacity
        aux_time        = 1 + 2*random.random()
        aux_capacity    = 0.1 + 5*random.random()
        
        G.add_edge(nstart,nend, time = aux_time, capacity = aux_capacity)
    
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
            nd_posX.append(elem.attrib['lon'])
            nd_posY.append(elem.attrib['lat'])
            
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

