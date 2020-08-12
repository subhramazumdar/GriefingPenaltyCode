import json
import logging
import networkx as nx
import sys

from common import get_id,set_source_sink_connection,call_flow,select_victim  

def mount_griefing(G,attacker_node,node_potential_victim,set_source,set_sink_remain,budget=30000):
    """
    Exhaust several channels of the victim
    """
    while budget>0:
        node_select="-1"
        min_wt=300000000000000000000
        for j in set_source :            
            #select a neighbour of victim node from the source set whose channel has to be exhausted
            if int(G.edges[node_potential_victim,j]['capacity'])>0 and min_wt>int(G.edges[node_potential_victim,j]['capacity']):
                min_wt=int(G.edges[node_potential_victim,j]['capacity'])
                #node_select is the node whose flow must be routed through the attacker instead of victim, select the node having minimum weighted edge to the victim
                node_select=j
                
        if node_select=="-1":
            return budget
        set_source.remove(node_select)
        #if budget is inadequate then reset minimum capacity to be blocked
        if budget < 2*min_wt:
            
                min_wt=budget/2
            
            
    
        target_select="-1"
        #select a neibour of the victim node from the sink set
        for k in set_sink_remain:
            if int(G.edges[node_potential_victim,k]['capacity'])>=min_wt:
                target_select=k
                set_sink_remain.remove(target_select)
                break
        
        #if no such neighbour of victim node exist then abort
        if target_select=="-1":
            return budget
        #add edge from attacker node to one of the neighbour of victim
        G.add_edge(target_select,attacker_node,capacity=min_wt,deposit2=min_wt)
        #add edge from attacker node to one of the neighbour of victim node_select
        G.add_edge(attacker_node,node_select,capacity=min_wt,deposit2=min_wt)
        
        budget=budget-2*min_wt
    
        #form the self loop connecting attacker to victim node
        paths=[]
        #change deposit of edges connected to attacker
        paths.append((attacker_node,node_select))
        G.edges[attacker_node,node_select]['deposit2']=int(G.edges[attacker_node,node_select]['deposit2'])-min_wt
        G.edges[attacker_node,node_select]['weight']=int(G.edges[attacker_node,node_select]['capacity'])
        #print(G.edges[attacker_node,node_select])
        #change weight of edge connected to victim
        paths.append((node_select,node_potential_victim))
        G.edges[node_select,node_potential_victim]['capacity']=int(G.edges[node_select,node_potential_victim]['capacity'])-min_wt
        G.edges[node_select,node_potential_victim]['weight']=int(G.edges[node_select,node_potential_victim]['capacity'])
        
        #change weight of edge connected to victim
        paths.append((node_potential_victim,target_select))
        G.edges[node_potential_victim,target_select]['capacity']=int(G.edges[node_potential_victim,target_select]['capacity'])-min_wt
        G.edges[node_potential_victim,target_select]['weight']=int(G.edges[node_potential_victim,target_select]['capacity'])
        
        #change deposit of edges connected to attacker
        paths.append((target_select,attacker_node))
        G.edges[target_select,attacker_node]['deposit2']=int(G.edges[target_select,attacker_node]['deposit2'])-min_wt
        G.edges[target_select,attacker_node]['weight']=int(G.edges[target_select,attacker_node]['capacity'])
        
        #logging.info("The path chosen for griefing attack:")
        #print(paths)
        logging.info("Bottleneck capacity of the path: ")
        print(min_wt)
        
        
        
        
        
        
    
    
    return budget


def attack_best_case_earning(G,attacker_node,node_potential_victim,budget=30000):    
    """
    estimate the earning of attacker node for a given victim
    """
    vict_money=0
    attack_money=0
    set_source,set_sink=set_source_sink_connection(G,node_potential_victim,attacker_node)
    for edge in G.edges:
            G.edges[edge]['weight']=int(G.edges[edge]['capacity'])

    vict_money,attack_money=call_flow(G,node_potential_victim,attacker_node)   
    logging.info("Flow through attacker before griefing: ")
    print(attack_money)
    
    original_budget=budget
    """
    mount griefing attack by exhausting several channels of the chosen victim nodes till the budget becomes 0 or till no condition mentioned in the function holds true
    """
    budget=mount_griefing(G,attacker_node,node_potential_victim,set_source,set_sink,budget)
    
    attack_money=0  
    #if there is no change in budget then attack did not get mounted
    #for edge in G.edges:
    #        G.edges[edge]['weight']=int(G.edges[edge]['capacity'])
    if budget<original_budget:
        #estimate the flow after the attack
        vict_money,attack_money=call_flow(G,node_potential_victim,attacker_node)

        logging.info("Flow through attacker after griefing: ")
        print(attack_money)
        #calculate processing fee as base fee(1 sat)+ rate of processing(0.001)*flow through edge
        #attack_money=1+0.001*attack_money
    else:
        logging.info("No attack possible")        
    
    #remove super source and super sink
    G.remove_node('0')
    G.remove_node('1')

    #return the profit earned by attacker                
    return attack_money,budget


def launch_attack_griefing(G,budget,per_tx_val):
    """
    Till budget becomes 0, find the victim and mount griefing attack
    """
    attacker_node=sorted(G.nodes(data=True), key=lambda x: x[1]['capacity'], reverse=True)[:1][0][0]
    
    #sort nodes based on betweeneness_centrality, select top 10 nodes as candidate for griefing attack
    centrality_node=sorted(G.nodes(data=True), key=lambda x:x[1]['betweenness_centrality'],reverse=True)
    
    centrality_id=get_id(centrality_node[:10])
    if attacker_node in centrality_id:
        centrality_id.remove(attacker_node)
    #used_victim=[]
    profit=0
    original_budget=budget
    while budget>0 and len(centrality_id)>0:
        attacker_money=0
        """
        choose the victim
        """
        node_potential_victim=select_victim(G,centrality_id[0])
        
        if node_potential_victim=="-1":
            centrality_id.remove(centrality_id[0])
        
            continue
        
        logging.info("The victim node: ")
        print(node_potential_victim)
    
        logging.info("The attacker node: ")
        print(attacker_node)
     
        #estimate the earning of griefer after attack for a given attacker,victim pair
        attacker_money,budget=attack_best_case_earning(G,attacker_node,node_potential_victim,budget)
        logging.info("Budget: ")
        print(budget)
        
        profit=profit+attacker_money
        
        #used_victim.append(node_potential_victim)
        #remove the node from the set
        centrality_id.remove(node_potential_victim)
         
    
    profit=((profit/per_tx_val)*G.nodes[attacker_node]['basefee']/1000)+((G.nodes[attacker_node]['rate']*profit)/1000000000)
    
    
    logging.info("Budget of attacker: ")
    print(original_budget)
    logging.info("Earning of attacker : ")
    print(profit)
    return profit
