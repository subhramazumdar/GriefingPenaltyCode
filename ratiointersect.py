import json
import logging
import networkx as nx
import sys
import itertools

from graph_visualization_helpers import plot_graph, set_graph_color, set_node_color

from common import get_id
#from attack_channel import launch_attack_channel
#from attacker_channel_griefing import launch_attack_griefing_channel_penalty
from centrality_measure import set_bet_centrality,set_deg_nodes,set_node_capacity,read_graph,filter_snapshot_data

def launch_attack_channel(G,gamma,per_tx_val,path_length,max_limit):
    
    path_now=0
    budget=0
    attacker_node=sorted(G.nodes(data=True), key=lambda x: x[1]['capacity'], reverse=True)[:1][0][0]
    current=attacker_node
    cum_penalty=0
    time=0
    while time<max_limit and path_now<path_length:
            time=time+G.nodes[current]['time']
            prev_current=current
            for node in G.neighbors(current):
                
                if G.edges[node,current]['capacity']>=per_tx_val and G.edges[node,current]['deposit2']>=per_tx_val and time+G.nodes[node]['time']<=max_limit:
                    current=node
                
                    path_now=path_now+1
                    break
            if prev_current==current:
                break
    flow=per_tx_val
    cum_penalty=flow*gamma*time*10
    while flow+cum_penalty>per_tx_val:
        flow=flow*0.99
        cum_penalty=flow*gamma*time*10
        
    a=flow/per_tx_val
    b=cum_penalty/per_tx_val
    #cum_penalty=cum_penalty+gamma*G.nodes[current]['time']*10*per_tx_val
    return a,b

        

def main():

    logging.basicConfig(format='\n%(levelname)s: %(message)s', level=logging.INFO)

    
    print(sys.argv[1])
    with open(sys.argv[1]) as f:
        source = json.load(f)

    source = filter_snapshot_data(source)

                
    G=read_graph(source)    
   # set_graph_color(G)
    #print('\nThe two top capacity nodes')
    set_node_capacity(G)
    nodes = sorted(G.nodes(data=True), key=lambda x: x[1]['capacity'], reverse=True)
    #print(nodes[:2])
    #cap_node_id = get_id(nodes[:2])
    #print(cap_node_id)
    
    #set_deg_nodes(G)
    #print('\nThe two highest connected nodes')
    #deg_node = sorted(G.nodes(data=True), key=lambda x:x[1]['degree'])
    #deg_id=get_id(deg_node[:2])
    #print(deg_id)

    #set_bet_centrality(G)
    
    

    # set_node_color(G, [target_node, attacker_node], 'red')
    # plot_graph(G)
    
    #TODO Take into account the budget of attacker as well
    G_tmp=G.copy()
    
    
    
    
    #based on fixed budget of attacker, find out the number of nodes which can be attacked
    
    gamma=float(sys.argv[2])
    per_tx_val=int(sys.argv[3])
    path_length=int(sys.argv[4])
    G_tmp=G.copy()
    f1=open(sys.argv[5],"a")
    
    
    ratio1,ratio2=launch_attack_channel(G_tmp,gamma,per_tx_val,path_length,2016)
    
    f1.write(sys.argv[1]+" "+str(per_tx_val)+" "+str(gamma)+" "+str(path_length)+" "+str(ratio1)+" "+str(ratio2)+"\n")
    G_tmp=G.copy()
    
    

    f.close()
    #mount an attack based on cut set
    #cutset_edges=attack_based_on_cutset(G_tmp,deg_node)

    #plot_graph(G)
    

if __name__ == '__main__':
    main()
