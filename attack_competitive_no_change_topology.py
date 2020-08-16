import json
import logging
import networkx as nx
import sys
from networkx.algorithms.flow import edmonds_karp

from common import get_id,select_victim,set_source_sink_connection_no_change,check

def mount_griefing_attack_no_change(G, per_tx_val, flow_edges, flow_val,node_potential_target, master_path_set,budget):
    """
    Select an attacker which has not yet utilized the capacity of its outgoing edges fully for routing transaction. It selects a victim node, which routes many transaction through
    itself. It targets the victim so that it can block certain fraction of transactions getting routed through the victim. Such transactions will get routed
    through the attacker after the griefing attack.
    """
    min_val = 0
    diff = 0
    profit = 0
    attacker = "-1"
    attacker_neighbour = "-1"
    length_count = 0
    victim_neighbour = "-1"
    min_capacity = 0
    
    # TODO: can we name j better? 
    for j in flow_edges[node_potential_target].items():
    
        if j[1]>0 and flow_val>j[1] and int(G.edges[j[0], node_potential_target]['capacity']) > j[1] and G.edges[j[0],node_potential_target]['deposit2'] > 0 and min_val < G.nodes[j[0]]['betweenness_centrality'] and j[0] not in master_path_set:        
        
            #  print("node: ")
            #  print(j[0])
            #  print("flow: ")
            #  print(j[1])
            diff = int(G.edges[j[0], node_potential_target]['capacity']) - j[1]
            flow_attack = j[1]
            attacker = j[0]
            min_val = G.nodes[j[0]]['betweenness_centrality']
    
    if attacker == "-1":
        return length_count, min_capacity, profit, flow_edges, flow_val, master_path_set    

    print("Attacker: ")
    print(attacker)
    print(flow_attack)
    
    # TODO: a line about what we are trying to achieve and better naming of j
    victim = "-1"
    for j in flow_edges[node_potential_target].items():
    #    print(j)
        if j[1]>0 and int(G.edges[j[0],node_potential_target]['capacity']) == j[1] and j[0] not in master_path_set:        
            print("Victim: ")
            print("node: ")
            print(j[0])
            print("flow: ")
            print(j[1])
            victim = j[0]
            flow_vict = j[1]
    
            break


    if victim == "-1":
        return length_count, min_capacity, profit, flow_edges, flow_val, master_path_set    
            
    
    for node in G.neighbors(attacker):
        if node != node_potential_target and int(G.edges[node,attacker]['deposit2']) > 0 and node not in master_path_set and node != victim:
            attacker_neighbour = node
            break
    
    
    for node in G.neighbors(victim):
        if node != node_potential_target and int(G.edges[node,victim]['capacity']) > 0 and node not in master_path_set and node != attacker:
            victim_neighbour = node
            break

    
    
    paths = []
    
    if victim_neighbour == "-1" or attacker_neighbour == "-1":
        return length_count, min_capacity, profit, flow_edges, flow_val, master_path_set        
    
    
    paths.append((node_potential_target, victim))
    paths.append((victim, victim_neighbour)) 
    
        
    min_capacity = min(diff,min([int(G.edges[e]['capacity']) for e in paths]), G.edges[attacker_neighbour,attacker]['deposit2'], G.edges[node_potential_target,attacker]['deposit2'], budget) 


    if victim_neighbour != attacker_neighbour:    
        path_list = nx.edge_disjoint_paths(G, victim_neighbour, attacker_neighbour)
        
        # TODO: can we name this better?
        paths1 = []
        while True:
            
            try:
                paths1 = next(path_list)
            except StopIteration:
                return  length_count, min_capacity, profit, flow_edges, flow_val, master_path_set        
            
            # TODO: can we name the check function better? 
            if check(paths1,master_path_set) == True or (attacker in paths1) or (victim in paths1) or (node_potential_target in paths1) or ('0' in paths1) or ('1' in paths1) or  (min([int(G.edges[a,b]['capacity']) for a,b in zip(paths1[:-1], paths1[1:])]) <= 0):
                continue
            else:
                break

            
        min_capacity = min(min([int(G.edges[a,b]['capacity']) for a,b in zip(paths1[:-1], paths1[1:])]), min_capacity)

        for a,b in zip(paths1[:-1], paths1[1:]):
            G.edges[a,b]['capacity'] = int(G.edges[a,b]['capacity']) - min_capacity
            G.edges[a,b]['weight'] = int(G.edges[a,b]['capacity'])
            length_count += 1
    
    
    if min_capacity == 0:
            length_count = 0
            return length_count, min_capacity, profit, flow_edges, flow_val, master_path_set        
    
    if min_capacity < 0:
        # TODO: graceful exit? Atleast a log statement would be better before exiting
        exit(1)

    G.edges[attacker_neighbour,attacker]['deposit2'] = int(G.edges[attacker_neighbour,attacker]['deposit2']) - min_capacity

    G.edges[node_potential_target,attacker]['deposit2'] = int(G.edges[attacker_neighbour,attacker]['deposit2']) - min_capacity

    G.edges[node_potential_target,victim]['capacity'] = int(G.edges[node_potential_target,victim]['capacity']) - min_capacity
    G.edges[node_potential_target,victim]['weight'] = int(G.edges[node_potential_target,victim]['capacity'])

    G.edges[victim_neighbour,victim]['capacity'] = int(G.edges[victim_neighbour,victim]['capacity']) - min_capacity
    G.edges[victim_neighbour,victim]['weight'] = int(G.edges[victim_neighbour,victim]['capacity'])        
    
    # TODO: a line to justify the value 4
    length_count += 4
    #insert(paths1,master_path_set)
    
    master_path_set.append(attacker)
    master_path_set.append(victim)
    master_path_set.append(node_potential_target)

    
    flow_val,flow_edges = nx.maximum_flow(G, '0', '1', capacity = 'weight', flow_func = edmonds_karp)
    
    
    
    if flow_edges[node_potential_target][attacker] > flow_attack:
        profit = (((flow_edges[node_potential_target][attacker] - flow_attack)/per_tx_val)*G.nodes[attacker]['basefee']/1000) + (G.nodes[attacker]['rate']*((flow_edges[node_potential_target][attacker] - flow_attack)))/1000000000
    
    return length_count, min_capacity, profit, flow_edges, flow_val, master_path_set        


            
                    
def launch_attack_griefing_no_change(G,budget_provided,per_tx_val,f):
    """
    Till the budget is exhausted, go on selecting an attacker-victim pair 
    """
    
    centrality_node = sorted(G.nodes(data = True), key = lambda x:x[1]['betweenness_centrality'], reverse = True)
    
    centrality_id = get_id(centrality_node)

    #used_victim = []
    profit = 0
    count = 0
    budget = 0
    master_path_set = []
    path_length = 0
    while len(centrality_id) > 0 and budget_provided > 0:
        attacker_money = 0
        node_potential_target = select_victim(G, centrality_id[0])
        
        
        if node_potential_target == "-1":
            
            centrality_id.remove(centrality_id[0])    
            continue
        
        print("Node potential: ")
        print(node_potential_target)
        
        set_source_sink_connection_no_change(G, node_potential_target)
        
        for edge in G.edges:
            G.edges[edge]['weight'] = int(G.edges[edge]['capacity'])
   
        flow_val,flow_edges = nx.maximum_flow(G, '0', '1',capacity = 'weight', flow_func = edmonds_karp)
    
    
        logging.info("The maximum flow in the network: ")    
        print(flow_val)
        
        
        # calculate the flow through the victim node
        length_count, budget_partial, profit_partial, flow_edges, flow_val, master_path_set = mount_griefing_attack_no_change(G, per_tx_val, flow_edges, flow_val, node_potential_target, master_path_set, budget_provided)
        if profit_partial > 0:
            profit = profit+profit_partial
            budget_provided -= budget_partial
            count += 1
            path_length += length_count
            print("Profit:")
            print(profit)
       
        
        centrality_id.remove(node_potential_target)
        G.remove_node('0')

        G.remove_node('1')
        
    
    return budget_provided, profit, path_length/count
    
