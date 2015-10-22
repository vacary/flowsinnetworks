#
# Event-driven parsing for osm files

# Standard library imports
import sys
import os
import random

from databuilder.layouts.utils.mercator import merc_x
from databuilder.layouts.utils.mercator import merc_y

#Non standard library imports
from lxml import etree
import networkx as nx
#import matplotlib.pyplot as plt

class Node:
    
    def __init__(self, id, type, lon, lat):
        
        self.id = id
        self.lon = lon
        self.lat = lat
        self.type = type
        self.numberOfRefs = 0
    
    def increase_number_of_refs(self):
        
        self.numberOfRefs = self.numberOfRefs + 1
    
class OsmNetwork:
    
    def __init__(self, osm_file_path):
        
        self.G = nx.MultiDiGraph()
        self.source = ''
        self.sink = ''
         
        self.osm_nodes = {}
        
        try:
            self._initialize(osm_file_path)
        except:
            print (sys.exc_info())
            print '[MSG] Osm file process error.'
    
    def _initialize(self, osm_file_path):
        
        self.get_number_of_references_by_node(osm_file_path)
        
        self.build_graph_G(osm_file_path)
        
        self.remove_non_reachable_G_nodes_from_source()

    def get_number_of_references_by_node(self, osm_file_path):

        # Build osm nodes dictionary
        
        for event, element in etree.iterparse(osm_file_path):
                        
            if (element.tag == 'node'):
                
                self.save_osm_node(event, element)
        
        # Get number of references for each node
        
        for event, element in etree.iterparse(osm_file_path):
            
            if (element.tag == 'way'):
                
                is_required_way = self.is_required_way(event, element)

                if (is_required_way):

                    listOfNds= list(element.iterfind("nd"))

                    for elm in listOfNds:
                        
                        osm_node_id = elm.attrib['ref']
                        self.osm_nodes[osm_node_id].increase_number_of_refs()
        
    def build_graph_G(self, osm_file_path):
                
        # Detect and add nodes (and edges) to the networkx MultiDiGraph

        for event, element in etree.iterparse(osm_file_path):
            
            if (element.tag == 'way'):
                
                is_required_way = self.is_required_way(event, element)
    
                if (is_required_way):
    
                    self.add_edge_and_nodes_to_G(event, element)
    
    def add_edge_and_nodes_to_G(self, event, element):
        
        listOfNds = list(element.iterfind("nd"))
            
        if (len(listOfNds) > 1):
            
            # all the edges associated with a way share
            # capacity and name parameters
            capacity = self.get_edge_capacity(event, element)
            name = unicode(self.get_edge_name(event, element))
            
            #name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
            
            # edges associated with a way does not have the same geometry or time
            geometry = []
            edge_tail = listOfNds[0].attrib['ref']
            
            for elm in listOfNds:
                
                #--- node processing ---
                osm_node_id = elm.attrib['ref']
                
                #add position to edge geometry
                pos_x = merc_x(self.osm_nodes[osm_node_id].lon)
                pos_y = merc_y(self.osm_nodes[osm_node_id].lat)
                pos_z = 0.0
                
                geometry.append([pos_x, pos_y, pos_z])
                
                #--- edge processing ---
                # detect and add edge
                if (self.osm_nodes[osm_node_id].numberOfRefs > 1 or elm == listOfNds[-1] ):
                    
                    edge_head = osm_node_id
                    
                    if (edge_head != edge_tail):
                    
                        time = self.get_edge_time(event, element)
                    
                        self.G.add_edge(edge_tail, edge_head, time=time, capacity=capacity, geometry=str(geometry), name=name)
                        self.G.add_node(edge_tail, pos = str(geometry[0]), nlabel= str(edge_tail))                        
                        self.G.add_node(edge_head, pos = str(geometry[-1]), nlabel= str(edge_head))
                        
                        geometry = [geometry[-1]]
                        edge_tail = edge_head
                
                
    def get_edge_time(self, event, element):
        
        default_time = 1.0 + 0.5*random.random()
        
        # set time

        time = default_time

        return time
        
        
    def get_edge_capacity(self, event, element):
            
        default_capacity = 0.1 + 2*random.random()
            
        # set capacity from osm data
        
        local_iter = element.iterfind("tag")
        
        attr = {}
        for elm in local_iter:
            attr[elm.attrib["k"]] = elm.attrib["v"]
        
        if ('lanes' in attr):
            try:
                capacity = 1.0*float(attr['lanes'])
                # oneway = "no" case is not considered in this code
            except:
                capacity = default_capacity
        else:
            capacity = default_capacity
        
        return capacity
        
    def get_edge_name(self, event, element):
        
        default_name = ''
        
        # set edge name (street name) from osm data
        
        local_iter = element.iterfind("tag")
        
        attr = {}
        for elm in local_iter:
            attr[elm.attrib["k"]] = elm.attrib["v"]
        
        if ('name' in attr):
            name = attr['name']
        else:
            name = default_name
                
        return name

    def is_required_way(self, event, element):
        
        ans = False
        
        local_iter = element.iterfind("tag")
        
        attr = {}
        for elm in local_iter:
            attr[elm.attrib["k"]] = elm.attrib["v"]

        if ('highway' in attr):
            
            if (attr['highway'] in ['primary','secondary','tertiary','residential','motorway','primary_link','motorway_link']):

                ans = True

        return ans

    def save_osm_node(self, event, element):
        
        id = element.attrib['id']
        lon = float(element.attrib['lon'])
        lat = float(element.attrib['lat'])
        
        local_iter = element.iterfind("tag")
        
        attr = {}
        for elm in local_iter:
            attr[elm.attrib["k"]] = elm.attrib["v"]        
        
        type = 'regular'
        
        if ('type' in attr):
            
            type = attr['type']
            
            if (type == 'source'):

                self.source = id
            
            if (type == 'sink'):

                self.sink = id
                
        node = Node(id, type, lon, lat)
        self.osm_nodes[id] = node
        
    def get_network_graph_data(self):
        
        data = [None,None,None]
        
        if (self.source == ''):
            
            print '[MSG] Missing source node'
        
        elif (self.sink == ''):
            
            print '[MSG] Missing sink node'
            
        else:
            
            data = [self.G, self.source, self.sink]
        
        return data
    
    def remove_non_reachable_G_nodes_from_source(self):
        
        reachablesFromSource = nx.descendants(self.G, self.source)
        nodesToRemove = []
        
        for node in self.G.nodes_iter():
            if (node not in reachablesFromSource):
                if (node != self.source):
                    nodesToRemove.append(node)
        
        for node in nodesToRemove:
            self.G.remove_node(node)        
        