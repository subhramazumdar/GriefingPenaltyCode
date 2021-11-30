import json
import logging
import networkx as nx
import sys
import itertools
import random
from graph_visualization_helpers import plot_graph, set_graph_color, set_node_color

from common import get_id
#from attack_channel import launch_attack_channel
#from attacker_channel_griefing import launch_attack_griefing_channel_penalty
from centrality_measure import set_bet_centrality,set_deg_nodes,set_node_capacity,read_graph,filter_snapshot_data

def cal_time(G,get_path):
    time=0
    for i in range(len(get_path)-1):
        time=time+G.nodes[get_path[i]]['time']
    
    return time


def launch_attack(G,per_tx_val,source,sink,path_length,track):
    
    i=0
    collateral=0
    min_capacity=30000000000000000000000000000
    min_deposit=30000000000000000000000000000
    flag=0
    holding=0
    txtot=0
    holdingtot=0
    count=0
    budget=0
    success=0
    set_path=[]
    c=0
    counter=0
    
    for node in source:
        
        #print(node)
            temp_source=node
            counter=0
            
            while counter<track:
            
                set_path=[]
                temp_source=node
                set_path.append(temp_source)
        
                count=0
                val=0
                
                while count<path_length:
         #       print("count "+str(count))
                    for node1 in G.neighbors(temp_source):
                        flag=0
                        if int(G.edges[temp_source,node1]['capacity'])>=per_tx_val:
                        
                            G.edges[temp_source,node1]['capacity']=int(G.edges[temp_source,node1]['capacity'])-per_tx_val
                        
                            set_path.append(node1)
                            temp_source=node1
                        
                        #print(G.edges[temp_source,node1]['capacity'])
                        #G.edges[temp_source,node1]['deposit2']=int(G.edges[temp_source,node1]['deposit2'])-val
                            count=count+1
                            flag=1
                            break
                    if flag==0:
                        break
            
            
                if count==path_length:
                    c=c+1
                    holdingtot=holdingtot+(path_length-1)*(per_tx_val)
                   
                
                
                counter=counter+1
            #print(count)
        
        
    return c,holdingtot


def gp_launch_attack(G,per_tx_val,source,sink,path_length,gamma,track):
    
    i=0
    collateral=0
    min_capacity=30000000000000000000000000000
    min_deposit=30000000000000000000000000000
    flag=0
    holding=0
    txtot=0
    count=0
    budget=0
    holdingtot=0
    success=0
    set_path=[]
    c=0
    counter=0
    
    for node in source:
        
        #print(node)
            temp_source=node
            counter=0
            
            while counter<track:
            
                set_path=[]
                temp_source=node
                set_path.append(temp_source)
        
                count=0
                val=0
                totalval=0
                
                while count<path_length:
         #       print("count "+str(count))
                
                    for node1 in G.neighbors(temp_source):
                        flag=0
                        if int(G.edges[temp_source,node1]['capacity'])>=per_tx_val and int(G.edges[temp_source,node1]['deposit2'])>=val+gamma*per_tx_val*(((path_length-count)*41+80)*10):
                        
                            G.edges[temp_source,node1]['capacity']=int(G.edges[temp_source,node1]['capacity'])-per_tx_val
                            G.edges[temp_source,node1]['deposit2']=int(G.edges[temp_source,node1]['deposit2'])-(val+gamma*per_tx_val*(((path_length-count)*41+80)*10))
                            set_path.append(node1)
                            temp_source=node1
                            val=val+gamma*per_tx_val*(((path_length-count)*41+80)*10)
                            totalval=totalval+val
                        #print(G.edges[temp_source,node1]['capacity'])
                        #G.edges[temp_source,node1]['deposit2']=int(G.edges[temp_source,node1]['deposit2'])-val
                            count=count+1
                            flag=1
                            break
                    if flag==0:
                        break
            
            
                if count==path_length:
                    c=c+1
                    
                    holdingtot=holdingtot+totalval+(path_length-1)*per_tx_val-val
                    txtot=txtot+per_tx_val
                counter=counter+1
            #print(count)
           
    #return c,holding,txtot,holdingtot
    return c,holdingtot       

        

def main():

    logging.basicConfig(format='\n%(levelname)s: %(message)s', level=logging.INFO)

    
    print(sys.argv[1])
    with open(sys.argv[1]) as f:
        source = json.load(f)

    source = filter_snapshot_data(source)

    chan_ratio=0
    G=read_graph(source,chan_ratio)    
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
    
    zeta=float(sys.argv[2])
    
    per_tx_val=int(sys.argv[3])
    
    G_tmp=G.copy()
    #adv_budget=int(sys.argv[5])
    gamma=float(sys.argv[4])
    num_transaction=int(sys.argv[5])
    path_length=int(sys.argv[6])
    
    s=[]
    t=[]
    sink=[]
    source=[]
    node_list=[]
    f1=open(sys.argv[7],"a")
    
    num_source=100
    num_sink=int(num_transaction/num_source)
    print(num_source)
    
    count=0
    while count<num_source:
          r=random.randint(1,G.number_of_nodes()-1)
          if r not in s: 
              s.append(r)
              count=count+1
    
              
          
    for node in G.nodes:
        node_list.append(node)
        
    for item in s:
        
        source.append(node_list[item])
    
    G_tmp=G.copy()
    #num_corrupted=int(corruption*G.number_of_nodes()/100)
    num_corrupted=0
    c=[]
    corrupted_nodes=[]
    count=0
    
    print(path_length)
    success1,holdingtot1=gp_launch_attack(G_tmp,per_tx_val,source,sink,path_length,gamma,num_transaction/1000)    
    G_tmp=G.copy()
    success2,holdingtot2=launch_attack(G_tmp,per_tx_val,source,sink,path_length,num_transaction/1000)    
    
    #print(holding,success)
    #=gp_launch_attack(G_tmp,per_tx_val,source,sink,corrupted_nodes,path_length,gamma)    
    #print(success1,hold,txtot,success2)
    #for item in source:
     #   print(item)
    #for item in sink:
    #    print(item)
    
    
    
    #budget=launch_attack_channel(G_tmp,gamma,per_tx_val,path_length,adv_budget,2016)
    #budget1=
    
    f1.write(sys.argv[1]+" "+str(path_length)+" "+str(gamma)+" "+" "+str(zeta)+" "+str(num_transaction)+" "+str(success2)+" "+str(holdingtot2)+" "+str(success1)+" "+str(holdingtot1)+" "+"\n")
    #
    
    

    f.close()
    #mount an attack based on cut set
    #cutset_edges=attack_based_on_cutset(G_tmp,deg_node)

    #plot_graph(G)
    

if __name__ == '__main__':
    main()
