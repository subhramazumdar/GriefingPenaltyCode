import json
import logging
import networkx as nx
import sys
import itertools

from graph_visualization_helpers import plot_graph, set_graph_color, set_node_color

from common import get_id
from attack_competitive_best import launch_attack_griefing
from attacker_competitive_best_penalty import launch_attack_griefing_penalty
from centrality_measure import set_bet_centrality,set_deg_nodes,set_node_capacity,read_graph,filter_snapshot_data


        

def main():

    logging.basicConfig(format='\n%(levelname)s: %(message)s', level=logging.INFO)

    

    with open(sys.argv[1]) as f:
        source = json.load(f)

    source = filter_snapshot_data(source)

                
    G=read_graph(source)    
    set_graph_color(G)
    #print('\nThe two top capacity nodes')
    set_node_capacity(G)
    nodes = sorted(G.nodes(data=True), key=lambda x: x[1]['capacity'], reverse=True)
    #print(nodes[:2])
    #cap_node_id = get_id(nodes[:2])
    #print(cap_node_id)
    
    set_deg_nodes(G)
    #print('\nThe two highest connected nodes')
    deg_node = sorted(G.nodes(data=True), key=lambda x:x[1]['degree'])
    #deg_id=get_id(deg_node[:2])
    #print(deg_id)

    set_bet_centrality(G)
    
    

    # set_node_color(G, [target_node, attacker_node], 'red')
    # plot_graph(G)
    
    #TODO Take into account the budget of attacker as well
    G_tmp=G.copy()
    
    
    
    
    #based on fixed budget of attacker, find out the number of nodes which can be attacked
    budget=int(sys.argv[2])
    gamma=float(sys.argv[3])
    per_tx_val=int(sys.argv[4])
    G_tmp=G.copy()
    f1=open(sys.argv[5],"a")
    
    
    roi1=launch_attack_griefing(G_tmp,budget,per_tx_val)
    
    G_tmp=G.copy()
    #select the highest capacity node as the attacker node, for HTLC-GP with griefing
    roi2=launch_attack_griefing_penalty(G_tmp,budget,gamma,per_tx_val)

    #G_tmp=G.copy()
    
    f1.write(sys.argv[1]+" "+sys.argv[2]+" "+str(roi1)+" "+sys.argv[3]+" "+sys.argv[4]+" "+str(roi2)+"\n")
    f1.close()
    
    

    f.close()
    #mount an attack based on cut set
    #cutset_edges=attack_based_on_cutset(G_tmp,deg_node)

    #plot_graph(G)
    

if __name__ == '__main__':
    main()
