import json
import logging
import networkx as nx
import sys
from networkx.algorithms.flow import edmonds_karp


def set_source_sink_connection_no_change(G,node_potential_victim):
    
    set_source=[]
    set_choice=[]
    set_sink=[]
    master_set=[]
    
    capacity=0
    #select the set of source and sink, balanced in terms of capacity of edges
    for j in G.neighbors(node_potential_victim) :
        
        
           #include only degree 1 nodes in set of source
            
            
            if G.nodes[j]['degree']==1:
                
                set_source.append(j)
                capacity=capacity+int(G.edges[node_potential_victim,j]['capacity'])
                
            master_set.append(j)
            
            
                
  
    #select the target for connecting to attacker node as the one having edge capacity > the capacity of edge connecting victim to node node_select
            
    
    
    
    #add edges of very large capacity to super source and super sink
    
    
    for j in G.nodes:            
        if j not in master_set:
            set_sink.append(j)
    
    set_sink.remove(node_potential_victim)                    
    
    G.add_node('0')
    G.add_node('1')
    
    for node in set_source:
        G.add_edge('0',node,capacity=300000000000000000000)

    for node in set_sink:
        G.add_edge('1',node,capacity=300000000000000000000)
    
    #print("sinks:")
    #print(set_sink)
    
def check(path,master_path):
        
        for j in path:
            if j in master_path:
                return True
        return False    



    

def select_victim(G,node):
        
    
    node_potential_victim="-1"
    #select the victim node as the one having more than 1/2 the neighbours of degree 1
    
    count=0
    deg_chosen=G.nodes[node]['degree']
    print(deg_chosen)
    for j in G.neighbors(node) :
                if G.nodes[j]['degree']==1:
                    count=count+1
                if count>1:
                    node_potential_victim=node
                    
                    break
            
    print(count)            
    return node_potential_victim

def set_source_sink_connection(G,node_potential_victim,attacker):
    set_source=[]
    set_sink=[]
    
    val_wt=G.nodes[node_potential_victim]['capacity']
    wt=0
    
    
    #select the set of source and sink, balanced in terms of capacity of edges
    for j in G.neighbors(node_potential_victim) :
        
        
           #include only degree 1 nodes in set of source
            
         if j!=attacker:   
            if G.nodes[j]['degree']==1 and (wt+int(G.edges[node_potential_victim,j]['capacity']))<=val_wt/2:
                wt=wt+int(G.edges[node_potential_victim,j]['capacity'])
                set_source.append(j)
                
            else: #include the rest in the sinl set
                set_sink.append(j) 
        
            
            
                
    #select the target for connecting to attacker node as the one having edge capacity > the capacity of edge connecting victim to node node_select
            
    G.add_node('0')
    G.add_node('1')
    
    
    
    #add edges of very large capacity to super source and super sink
    for node in set_source:
        G.add_edge('0',node,capacity=300000000000000000000)

    for node in set_sink:
        G.add_edge(node,'1',capacity=300000000000000000000)        
    
    
    return set_source,set_sink

def call_flow(G,node_potential_victim,attacker_node):
    """
    execute maximum flow
    """

    flow_val,flow_edges=nx.maximum_flow(G,'0','1',capacity='weight', flow_func=edmonds_karp)
    
    
    logging.info("The maximum flow in the network: ")    
    print(flow_val)

    tot_flow_vict=0
    #calculate the flow through the victim node
    for j in flow_edges[node_potential_victim].items():
    #    print(j)
        tot_flow_vict=tot_flow_vict+j[1]
    
    tot_flow_attacker=0
    #calculate the flow through the attacker node
    for j in flow_edges[attacker_node].items():
    #    print(j)
        tot_flow_attacker=tot_flow_attacker+j[1]
    
    return tot_flow_vict,tot_flow_attacker
 
def get_id(nodes):
    """
    Input: list of graph nodes
    Output: list of pub_key corresponding to given nodes
    """
    node_pubkeys = []
    for node in nodes:
        node_pubkeys.append(node[0])
    return node_pubkeys              
