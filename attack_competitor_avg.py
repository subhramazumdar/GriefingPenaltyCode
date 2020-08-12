import json
import logging
import networkx as nx
import sys
from networkx.algorithms.flow import edmonds_karp
def attack_based_on_diff_flow(G,deg_node_list):
    #find attacker node with betweeneness_centrality 0
    attacker_node = find_attacker_and_target(G)
    #select the multiple source sink pairs based on degree centrality and connect it to super source and super sink
    multi_source=connect_supper_source_sink(G,deg_node_list,attacker_node)
    #find max flow in the modified graph 
    flow_val,flow_edges=nx.maximum_flow(G,'0','1',capacity='weight', flow_func=edmonds_karp)
    
    #select the victim node as the one receiving flow from one of the source node 
    
    for j in flow_edges.items():
        if j[0] in multi_source:
            #select the channel to be exhausted, attacker wants to spend the least amount 
            #our target is to select the edge with the least flow, indirectly implying minimum capacity of the edge??
            list_edge=sorted(flow_edges[j[0]].items(),key=lambda x: x[1],reverse=True)
            
            if list_edge[0][1]>0:
               # print(G.edges[j[0],list_edge[0][0]]['capacity'])
                target_node=list_edge[0][0]
                
                #the neigbour of victim with which attacker will form a channel
                node_select=j[0]
                #the flow through channel which will be exhausted
                flow_select=list_edge[0][1]
                
                break
    

    logging.info("The victim node: ")
    print(target_node)
    logging.info("The attacker node: ")
    print(attacker_node)
    tot_flow=0
    #calculate the flow through the victim node
    for j in flow_edges[target_node].items():
    #    print(j)
        tot_flow=tot_flow+j[1]
    logging.info("The flow through victim node: ")
    print(tot_flow)
    
    tot_flow=0
    #calculate the flow through the attacker node
    for j in flow_edges[attacker_node].items():
    #    print(j)
        tot_flow=tot_flow+j[1]
    logging.info("The maximum flow in the network before griefing: ")    
    print(flow_val)
    logging.info("The flow through the attacker node: ")
    print(tot_flow)
    
    #sort the flow through each outgoing edge from the victim node in ascending order
    list_edge=sorted(flow_edges[target_node].items(),key=lambda x: x[1])
    #print(list_edge)
   
                       
   #select another node connected to victim which has capacity greater or equal to the capacity of the target channel to be exhausted                    
    for j in list_edge:
            if j[0]!=node_select and int(G.edges[j[0],target_node]['capacity'])>=int(G.edges[node_select,target_node]['capacity']):
                logging.info("The other node with which the victim must form a channel for mouting griefing attack: ")
                
                target_select=j[0]
                print(target_select)
                break
    
    logging.info("The target channel: ")
    print((node_select,target_node))
    
    logging.info("Flow throught the target channel(which attacker intends to block: ")
    print(flow_select)
    
    
    #Set the capacity of the edge which the attacker forms with the neighbour of victim node. After locking the capacity of the target channel to exhausted, this channel will still have a resdidual capacity of value "flow_select" which will allow for the transaction to be routed via attacker
    cap1=G.edges[node_select,target_node]['weight']+flow_select
    cap=G.edges[node_select,target_node]['weight']
    #print(cap1)
    
   #add edge from attacker node to neighbour victim node node, this neighbor is one end of the channel to be exhausted  
    
    #add edge from attacker node to another neighbour of victim node
    G.add_edge(target_select,attacker_node,capacity=cap)
    G.add_edge(attacker_node,node_select,capacity=cap1)
    
    
            
    
    path=[]
    
    #form the self loop connecting attacker to victim node
    path.append((attacker_node,node_select))
    
    
    #G.edges[attacker_node,node_select]['weight']=G.edges[attacker_node,node_select]['weight']-attack_capacity
    path.append((node_select,target_node))
    
    #G.edges[node_select,target_node]['weight']=G.edges[node_select,target_node]['weight']-attack_capacity
    path.append((target_node,target_select))
    
    #G.edges[target_node,target_select]['weight']=G.edges[target_node,target_select]['weight']-attack_capacity
    path.append((target_select,attacker_node))
    
    #G.edges[target_select,attacker_node]['weight']=G.edges[target_select,attacker_node]['weight']-attack_capacity
    logging.info("The path for mounting the griefing attack: ")
    print(path)
    
    
    attack_capacity = min([int(G.edges[e]['capacity']) for e in path])
    #find the bottlneck capacity of the path
    
    logging.info("Bottleneck capacity of the path:")
    print(attack_capacity)
    
    #reduce the capacity of path after mounting the attack
    for e in path:
            G.edges[e]['capacity']=int(G.edges[e]['capacity'])-attack_capacity
            
            
    
    for edge in G.edges:
        G.edges[edge]['weight']=int(G.edges[edge]['capacity'])
        
    #Find the maximum flow in the graph after exhausting capacity of the targte channel    
    flow_val,flow_edges=nx.maximum_flow(G,'0','1',capacity='weight', flow_func=edmonds_karp)
    
    new_tot_flow=0
    for j in flow_edges[attacker_node].items():
         new_tot_flow=new_tot_flow+j[1]
  
        
    logging.info("The maximum flow in the network after griefing: ")    
    print(flow_val)
    logging.info("The flow through the attacker node: ")
    print(new_tot_flow)
    
    diff=new_tot_flow-tot_flow
    print("\nGain of attacker: "+str(diff)+"\n")
    
    for j in flow_edges[target_node].items():
    #    print(j)
        tot_flow=tot_flow+j[1]
    logging.info("The flow through victim node: ")
    print(tot_flow)
    
