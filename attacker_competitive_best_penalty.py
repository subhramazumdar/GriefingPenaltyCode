import json
import logging
import networkx as nx
import sys
import itertools
from common import get_id,set_source_sink_connection,call_flow,select_victim

def mount_griefing_penalty(G,attacker_node,node_potential_victim,set_source,set_sink_remain,gamma,budget=30000):
    """
    Exhaust several channels of the victim
    """
    loss=0
    count_impacted=0
    coll_temp=0
    calc_budget=0
    while budget>0:
        min_wt=300000000000000000000
        node_select="-1"
        for j in set_source :            
            #select a neighbour of victim node from the source set whose channel has to be exhausted
            if int(G.edges[node_potential_victim,j]['capacity'])>0 and min_wt>int(G.edges[node_potential_victim,j]['capacity']):
                min_wt=int(G.edges[node_potential_victim,j]['capacity'])
                #node_select is the node whose flow must be routed through the attacker instead of victim, select the node having minimum weighted edge to the victim
                node_select=j
                
    
        #if budget is inadequate then abort
        if node_select=="-1":
            return budget,loss,count_impacted,coll_temp,calc_budget
            
        set_source.remove(node_select)
        target_select="-1"
        #select a neibour of the victim node from the sink set
        for k in set_sink_remain:
            if int(G.edges[node_potential_victim,k]['capacity'])>=min_wt:
                target_select=k
                set_sink_remain.remove(target_select)
                break
        
        #if no such neighbour of victim node exist then abort
        if target_select=="-1":
            return budget,loss,count_impacted,coll_temp,calc_budget
        
        time_attacker=G.nodes[attacker_node]['time']+G.nodes[node_select]['time']+G.nodes[target_select]['time']+G.nodes[node_potential_victim]['time']
        time_node_select=time_attacker-G.nodes[node_select]['time']
        time_victim_select=time_node_select-G.nodes[node_potential_victim]['time']
        time_target_select=time_victim_select-G.nodes[target_select]['time']
        
<<<<<<< HEAD
=======
        time_attacker=G.nodes[attacker_node]['time']+G.nodes[node_select]['time']+G.nodes[target_select]['time']+G.nodes[node_potential_victim]['time']
        time_node_select=time_attacker-G.nodes[node_select]['time']
        time_victim_select=time_node_select-G.nodes[node_potential_victim]['time']
        time_target_select=time_victim_select-G.nodes[target_select]['time']
        
>>>>>>> f23777b23c71a8a44a319067145af9d5a763228b
        
        #if budget is inadequate then reset minimum capacity to be blocked
        
        if budget < (2*min_wt):
            
                min_wt=budget/2
            
        penalty=gamma*10*(time_attacker+time_node_select+time_target_select+time_victim_select)*min_wt
        
        change_wt=min_wt
        while penalty>=min_wt:
            change_wt=change_wt*0.95
            penalty=gamma*10*(time_attacker+time_node_select+time_target_select+time_victim_select)*change_wt
            
        #print(penalty)
        #print(min_wt)
    
        
        
        #add edge from attacker node to one of the neighbour of victim
        
        
        
        
        G.add_edge(target_select,attacker_node,capacity=min_wt,deposit2=min_wt)
        #add edge from attacker node to one of the neighbour of victim labeled as  "node_select"
        G.add_edge(attacker_node,node_select,capacity=min_wt,deposit2=min_wt)
        calc_budget=calc_budget+min_wt
        budget=budget-2*min_wt
    
        #form the self loop connecting attacker to victim node
        paths=[]
        #change deposit of edges connected to attacker
        paths.append((attacker_node,node_select))
        G.edges[attacker_node,node_select]['deposit2']=int(G.edges[attacker_node,node_select]['deposit2'])-change_wt
        G.edges[attacker_node,node_select]['capacity']=int(G.edges[attacker_node,node_select]['capacity'])-(gamma*10*time_attacker*change_wt)
        G.edges[attacker_node,node_select]['weight']=int(G.edges[attacker_node,node_select]['capacity'])
        
        
     #   print(G.edges[attacker_node,node_select])
        #change weight of edge connected to victim
        paths.append((node_select,node_potential_victim))
        G.edges[node_select,node_potential_victim]['capacity']=int(G.edges[node_select,node_potential_victim]['capacity'])-change_wt
        G.edges[node_select,node_potential_victim]['deposit2']=G.edges[node_select,node_potential_victim]['deposit2']-(gamma*10*time_attacker*change_wt+gamma*10*time_node_select*change_wt)
        G.edges[node_select,node_potential_victim]['weight']=int(G.edges[node_select,node_potential_victim]['capacity'])
        
        #change weight of edge connected to victim
        paths.append((node_potential_victim,target_select))
        G.edges[node_potential_victim,target_select]['capacity']=int(G.edges[node_potential_victim,target_select]['capacity'])-change_wt
        G.edges[node_potential_victim,target_select]['deposit2']=G.edges[node_potential_victim,target_select]['deposit2']-(gamma*10*time_attacker*change_wt+gamma*10*time_node_select*change_wt+gamma*10*time_victim_select*change_wt)
        G.edges[node_potential_victim,target_select]['weight']=int(G.edges[node_potential_victim,target_select]['capacity'])
        
        #change deposit of edges connected to attacker
        paths.append((target_select,attacker_node))
        G.edges[target_select,attacker_node]['deposit2']=int(G.edges[target_select,attacker_node]['deposit2'])-change_wt
        G.edges[target_select,attacker_node]['capacity']=int(G.edges[target_select,attacker_node]['capacity'])-(penalty)
        G.edges[target_select,attacker_node]['weight']=int(G.edges[target_select,attacker_node]['capacity'])
        
        loss=loss+(penalty-gamma*10*time_attacker*change_wt)
        count_impacted=count_impacted+penalty
        #coll_temp=coll_temp+3*change_wt+gamma*10*time_attacker*change_wt+gamma*10*time_node_select*change_wt+gamma*10*time_victim_select*change_wt+(gamma*10*time_attacker*change_wt+gamma*10*time_node_select*change_wt)+(gamma*10*time_attacker*change_wt)
        coll_temp=coll_temp+change_wt

        #print(penalty-gamma*10*time_attacker*change_wt)
        
      #  print(time_attacker)
      #  print(time_node_select)
      #  print(time_target_select)
      #  print(time_victim_select)
      #  print(gamma)
      #  print("penalty: ")
      #  print(penalty)
      #  print(gamma*10*time_attacker*change_wt)
     #   print(loss)
     #   print(min_wt)
     #   print(change_wt)
  
        
       # logging.info("The path chosen for griefing attack:")
       # print(paths)
        #logging.info("Bottleneck capacity of the path: ")
        #print(min_wt)
        
        
        
        
    return budget,loss,count_impacted,coll_temp,calc_budget


def attack_best_case_earning_penalty(G,attacker_node,node_potential_victim,gamma,budget=30000):    
    """
    estimate the earning of attacker node for a given victim as well as the penalty incurred
    """
    vict_money=0
    attack_money=0
    attack_money_prev=0
    vict_money_prev=0
    
    set_source,set_sink=set_source_sink_connection(G,node_potential_victim,attacker_node)
    for edge in G.edges:
            G.edges[edge]['weight']=int(G.edges[edge]['capacity'])

    vict_money_prev,attack_money_prev=call_flow(G,node_potential_victim,attacker_node)   
    logging.info("Flow through attacker before griefing: ")
    print(attack_money_prev)
    logging.info("Flow through victim before griefing: ")
    print(vict_money_prev)
    
    original_budget=budget
    """
    mount griefing attack by exhausting several channels of the chosen victim nodes till the budget becomes 0 or till no condition mentioned in the function holds true
    """
    budget,loss,count_impacted,coll_temp,calc_budget=mount_griefing_penalty(G,attacker_node,node_potential_victim,set_source,set_sink,gamma,budget)
    
    #if there is no change in budget then attack did not get mounted
    
    if budget<original_budget and coll_temp>0:
        #estimate the flow after the attack
        vict_money,attack_money=call_flow(G,node_potential_victim,attacker_node)

        logging.info("Flow through attacker after griefing: ")
        print(attack_money)
        logging.info("Flow through victim after griefing: ")
        print(vict_money)
        
    else:
        logging.info("No attack possible")        
    
    #remove super source and super sink
    G.remove_node('0')
    G.remove_node('1')
    
    #return the profit earned by attacker                
    return attack_money,loss,budget,count_impacted,coll_temp,calc_budget


def launch_attack_griefing_penalty(G,budget,gamma,per_tx_val):
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
    total_loss=0
    collateral=0
    total_penalty=0
    original_budget=budget
    total_budget=0
    last_budget=budget
    while budget>0 and len(centrality_id)>0:
        attacker_money=0
        """
        choose a victim
        """
        node_potential_victim=select_victim(G,centrality_id[0])
        
        if node_potential_victim=="-1":
            
            centrality_id.remove(centrality_id[0])
            continue
        
        logging.info("The victim node: ")
        print(node_potential_victim)
    
        logging.info("The attacker node: ")
        print(attacker_node)
     
        #estimate the earning of griefer after attack,loss incurred for a given attacker,victim pair    
        attacker_money,loss,budget,count_impacted,coll_temp,calc_budget=attack_best_case_earning_penalty(G,attacker_node,node_potential_victim,gamma,budget)
        if budget==last_budget:
            continue
        else:
           last_budget=budget
        logging.info("Budget: ")
        print(budget)
        #profit made
        profit=profit+attacker_money
        collateral=collateral+coll_temp
        total_penalty=total_penalty+count_impacted
        total_budget=total_budget+calc_budget
        #penalty paid
        total_loss+=loss
        #remove the node from the set
        centrality_id.remove(node_potential_victim)
         
    #print(profit)
    #print(loss)
    profit=((profit/per_tx_val)*G.nodes[attacker_node]['basefee']/1000)+((G.nodes[attacker_node]['rate']*profit)/1000000000)-total_loss   
    
    logging.info("Budget of attacker: ")
    print(original_budget)
    logging.info("Earning of attacker : ")
    print(profit)
    return profit,collateral,total_penalty,total_budget
