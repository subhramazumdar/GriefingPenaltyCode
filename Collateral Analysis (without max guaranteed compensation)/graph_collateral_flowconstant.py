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

def launch_attack_channel(G,gamma,per_tx_val,path_length,adv_budget,fraction,max_limit):
    
    i=0
    collateral=0
    min_capacity=30000000000000000000000000000
    min_deposit=30000000000000000000000000000
    
    factor=False
    count=0
    while adv_budget>0.01:
        min_capacity=30000000000000000000000000000
        min_deposit=30000000000000000000000000000
        path_now=0
        budget=0
        attacker_node=sorted(G.nodes(data=True), key=lambda x: x[1]['capacity'], reverse=True)[:G.number_of_nodes()][i][0]
        #print(attacker_node)
        #print(i)
        #print(adv_budget)
        #print(per_tx_val)
        #print(factor)
        #print(collateral)
        current=attacker_node
        cum_penalty=0
        time=0
        list_node=[]
        
        while time<max_limit and path_now<path_length:
            
            prev_current=current
            factor=False
            for node in G.neighbors(current):
                
                
                loc_penalty=gamma*G.nodes[current]['time']*10*per_tx_val
                if time+G.nodes[prev_current]['time']+G.nodes[node]['time']<=max_limit and G.edges[prev_current,node]['htlc']<=481:
                    
                    if G.edges[prev_current,node]['capacity']>=per_tx_val:
                        if min_capacity>G.edges[prev_current,node]['capacity']:
                            min_capacity=G.edges[prev_current,node]['capacity']
                    else:
                        #print("Round")
                        continue
                    
                    if G.edges[prev_current,node]['deposit2']>=cum_penalty+loc_penalty:
                        if min_deposit>G.edges[prev_current,node]['deposit2']:    
                            min_deposit=G.edges[prev_current,node]['deposit2']
                    else:
                        #print("Round")
                        continue        
                    
                    factor=True    
                    current=node
                    list_node.append((current,prev_current))
                    cum_penalty=cum_penalty+loc_penalty
                    path_now=path_now+1
                    break
            
            if factor==True:    
                time=time+G.nodes[prev_current]['time']        
            else:
                i=i+1
                if i==G.number_of_nodes():
                    i=0
                    path_length=int(path_length*0.75)
                    break
            if prev_current==current:
                break
        #list_node.remove(current)            
        if factor==False:
            print("ok")
            continue
        start_node=current
        #value=min(per_tx_val,min_deposit+min_capacity,adv_budget)
        flow=per_tx_val
        if flow>(adv_budget):
            flow=(adv_budget)/2
        cum_penalty=min(cum_penalty,adv_budget-fraction*flow)
        flow=cum_penalty/(10*gamma*time)
        #flow=value/(1+gamma*10*time)
        #print(flow)
        
        if (adv_budget-(cum_penalty+flow))<0.01:
            break
        
        #print(flow)
        #flow=min(flow,min_capacity)
        #value=min(value,flow+gamma*10*time*flow)
        
        
        #print(min_capacity)
        #print(min_deposit)
        collateral=collateral+(path_now-1)*flow
        #htlc_collateral=htlc_collateral+(path_now-1)*per_tx_val
        #time_new=0
        #value=per_tx_val
        
        value=cum_penalty
        count=count+1
        for e in list_node:
            #time_new=time_new+G.nodes[e[0]]['time']print("ok")
            G.edges[e]['deposit2']=G.edges[e]['deposit2']-value    
            G.edges[e]['capacity']=G.edges[e]['capacity']-flow
            G.edges[e]['htlc']=G.edges[e]['htlc']+2
            
            collateral=collateral+value
            value=value-flow*gamma*10*G.nodes[e[1]]['time']
            
        
        collateral=collateral-cum_penalty
        
        adv_budget=adv_budget-(cum_penalty+flow)
      #  print(adv_budget)
        
    print(collateral)
    print(adv_budget)
    
    return collateral,count

def launch_attack(G,per_tx_val,path_length,adv_budget,max_limit):
    
    i=0
    collateral=0
    min_capacity=30000000000000000000000000000
    min_deposit=30000000000000000000000000000
    factor=False
    count=0
    while adv_budget>0.01:
        min_capacity=30000000000000000000000000000
        min_deposit=30000000000000000000000000000
        path_now=0
        budget=0
        attacker_node=sorted(G.nodes(data=True), key=lambda x: x[1]['capacity'], reverse=True)[:G.number_of_nodes()][i][0]
        #print(attacker_node)
        #print(i)
        #print(adv_budget)
        #print(per_tx_val)
        #print(factor)
        #print(collateral)
        current=attacker_node
        cum_penalty=0
        time=0
        list_node=[]
        
        while time<max_limit and path_now<path_length:
            
            prev_current=current
            factor=False
            for node in G.neighbors(current):
                
                
                #loc_penalty=gamma*G.nodes[current]['time']*10*per_tx_val
                if time+G.nodes[prev_current]['time']+G.nodes[node]['time']<=max_limit and G.edges[prev_current,node]['htlc']<483:
                    
                    if G.edges[prev_current,node]['capacity']>=per_tx_val:
                        if min_capacity>G.edges[prev_current,node]['capacity']:
                            min_capacity=G.edges[prev_current,node]['capacity']
                    else:
                        #print("Round")
                        continue
                    
                    
                    factor=True    
                    current=node
                    list_node.append((current,prev_current))
                    #cum_penalty=cum_penalty+loc_penalty
                    path_now=path_now+1
                    break
            
            if factor==True:    
                time=time+G.nodes[prev_current]['time']        
            else:
                i=i+1
                if i==G.number_of_nodes():
                    i=0
                    path_length=int(path_length*0.75)
                    break
            if prev_current==current:
                break
        #list_node.remove(current)            
        if factor==False:
            
            continue
        start_node=current
        flow=min(per_tx_val,adv_budget)
        
        if (adv_budget-flow)<0.01:
            break
        
        
                
        
        #print(min_capacity)
        #print(min_deposit)
        collateral=collateral+(path_now-1)*flow
        #htlc_collateral=htlc_collateral+(path_now-1)*per_tx_val
        #time_new=0
        #value=per_tx_val
        
        
        count=count+1
        for e in list_node:
            #time_new=time_new+G.nodes[e[0]]['time']print("ok")
        
            G.edges[e]['capacity']=G.edges[e]['capacity']-flow
            G.edges[e]['htlc']=G.edges[e]['htlc']+1
            
        
        
        adv_budget=adv_budget-flow
        
    print(collateral)
    print(adv_budget)
    
    return collateral,count

        

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
    adv_budget=int(sys.argv[5])
    factor=float(sys.argv[6])
    f1=open(sys.argv[7],"a")
    
    
    budget,count=launch_attack_channel(G_tmp,gamma,per_tx_val,path_length,adv_budget,1,2016)
    budget1,count1=launch_attack(G_tmp,per_tx_val,path_length,adv_budget,2016)
    
    #f1.write(sys.argv[1]+" "+str(per_tx_val)+" "+str(adv_budget)+" "+str(budget)+" "+str(budget1)+" "+str(count)+" "+str(count1)+"\n")
    f1.write(sys.argv[1]+" "+str(path_length)+" "+str(adv_budget)+" "+str(gamma)+" "+str(factor)+" "+str(budget*factor)+" "+str(count)+" "+str(budget1*factor)+" "+str(count1)+"\n")
    G_tmp=G.copy()
    
    

    f.close()
    #mount an attack based on cut set
    #cutset_edges=attack_based_on_cutset(G_tmp,deg_node)

    #plot_graph(G)
    

if __name__ == '__main__':
    main()
