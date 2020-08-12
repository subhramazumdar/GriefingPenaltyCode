import json
import logging
import networkx as nx
import sys
from networkx.algorithms.flow import edmonds_karp
def attack_based_on_cutset(G,deg_node_list):
    #select the multiple source sink pairs based on degree centrality and connect it to super source and super sink
    connect_supper_source_sink(G,deg_node_list)
    
    
    #find the minimum cut set for the flow connecting 50 source to 50 sinks, returns just one cutset
    val,cut=nx.minimum_cut(G, '0', '1', capacity='weight', flow_func=edmonds_karp)
    print("value\n")
    print(val)
    reachable, non_reachable = cut
    print(reachable)
    print(non_reachable)
    cutset = set()
    for u, nbrs in ((n, G[n]) for n in reachable):
         cutset.update((u, v) for v in nbrs if v in non_reachable)
         
    return sorted(cutset)
    

