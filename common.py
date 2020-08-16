import json
import logging
import networkx as nx
import sys
from networkx.algorithms.flow import edmonds_karp


def set_source_sink_connection_no_change(G, node_potential_victim):
    """
    For attackign strategy, attacker uses the existing channels: For a given hub node, select the neighbours of hub havving degree one as the set of source nodes. Select all the nodes at a distance 
    of two from the hub node, which are also neighbours of hub node having degree more than 1, as the set of sink. Connect the set of sources with a super source and set of sinks with a super sink.
    Compute maximum flow from super source to super sink.
    """
    set_source = []
    set_choice = []
    set_sink = []
    master_set = []
    
    capacity = 0
    # select the set of source and sink, balanced in terms of capacity of edges
    for neighbor in G.neighbors(node_potential_victim) :
        # include only degree 1 nodes in set of source
        if G.nodes[neighbor]['degree'] == 1:
            
            set_source.append(neighbor)
            capacity = capacity + int(G.edges[node_potential_victim,neighbor]['capacity'])
            
        master_set.append(neighbor)
            
    # select the target for connecting to attacker node as the one having edge capacity > the capacity of edge connecting victim to node node_select
            
    
    
    
    # add edges of very large capacity to super source and super sink
    for node in G.nodes:            
        if node not in master_set:
            set_sink.append(node)
    
    set_sink.remove(node_potential_victim)                    
    
    G.add_node('0')
    G.add_node('1')
    
    for node in set_source:
        G.add_edge('0', node,capacity = 300000000000000000000)

    for node in set_sink:
        G.add_edge('1', node,capacity = 300000000000000000000)
    
    #print("sinks:")
    #print(set_sink)
    
def check(path, master_path):
    """
    Check whether the node has already been affected by griefing attack mounted previously
    """
    for node in path:
        if node in master_path:
            return True
    return False    


def select_victim(G,node):
    """
    select the victim node as the one having more than 1/2 the neighbours of degree 1
    """
    
    node_potential_victim = "-1"
    
    
    
    count = 0
    deg_chosen = G.nodes[node]['degree']
    print(deg_chosen)
    for neighbor in G.neighbors(node) :
        if G.nodes[neighbor]['degree'] == 1:
            count = count+1
        if count > 1:
            node_potential_victim = node
            break
            
    print(count)            
    return node_potential_victim

def set_source_sink_connection(G, node_potential_victim, attacker):
    """
    For attackign strategy, attacker establishes new chanels: For a given hub node, select the neighbours of hub having degree one as the source node and rest of
    the neighbours as the set of sink. Select the set of source and set of sink such that weight (summation of capacity of edges) of each set is equivalent. Connect the set of sources with a super source and set of sinks with a super sink.
    Compute maximum flow from super source to super sink.
    """
    set_source = []
    set_sink = []
    
    val_wt = G.nodes[node_potential_victim]['capacity']
    wt = 0
    
    # select the set of source and sink, balanced in terms of capacity of edges
    for neighbor in G.neighbors(node_potential_victim) :
        # include only degree 1 nodes in set of source
            
        if neighbor != attacker:   
            if G.nodes[neighbor]['degree'] == 1 and (wt + int(G.edges[node_potential_victim,neighbor]['capacity'])) <= val_wt/2:
                wt = wt + int(G.edges[node_potential_victim,neighbor]['capacity'])
                set_source.append(neighbor)
                
            else: #include the rest in the sink set
                set_sink.append(neighbor) 
        
            
            
                
    # select the target for connecting to attacker node as the one having edge capacity > the capacity of edge connecting victim to node node_select
            
    G.add_node('0')
    G.add_node('1')
    
    
    
    # add edges of very large capacity to super source and super sink
    for node in set_source:
        G.add_edge('0', node, capacity = 300000000000000000000)

    for node in set_sink:
        G.add_edge(node, '1', capacity = 300000000000000000000)        
    
    
    return set_source,set_sink

def call_flow(G, node_potential_victim, attacker_node):
    """
    execute maximum flow
    """

    flow_val,flow_edges = nx.maximum_flow(G, '0', '1', capacity = 'weight', flow_func = edmonds_karp)
    
    
    logging.info("The maximum flow in the network: ")    
    print(flow_val)

    tot_flow_vict = 0
    # calculate the flow through the victim node
    for edge in flow_edges[node_potential_victim].items():
    #    print(j)
        tot_flow_vict = tot_flow_vict + edge[1]
    
    tot_flow_attacker = 0
    # calculate the flow through the attacker node
    for edge in flow_edges[attacker_node].items():
    #    print(j)
        tot_flow_attacker = tot_flow_attacker + edge[1]
    
    return tot_flow_vict, tot_flow_attacker
 
def get_id(nodes):
    """
    Input: list of graph nodes
    Output: list of pub_key corresponding to given nodes
    """
    node_pubkeys  =  []
    for node in nodes:
        node_pubkeys.append(node[0])
    return node_pubkeys              
