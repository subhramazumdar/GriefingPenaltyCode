import json
import logging
import networkx as nx
import sys
import random
import itertools
import math

from graph_visualization_helpers import plot_graph, set_graph_color, set_node_color

from common import get_id
#from attack_channel import launch_attack_channel
#from attacker_channel_griefing import launch_attack_griefing_channel_penalty
from centrality_measure import set_bet_centrality,set_deg_nodes,set_node_capacity,read_graph,filter_snapshot_data

def launch_attack_channel(G,gamma,per_tx_val,path_length,source,num_corrupted,corruption,val,max_limit,frac,q):
    
    i=0
    count_tx=0
    pay_A=0
    pay_B=0
    min_capacity=30000000000000000000000000000
    min_deposit=30000000000000000000000000000
    factor=False
    for node in source:
        min_capacity=30000000000000000000000000000
        min_deposit=30000000000000000000000000000
        path_now=0
        budget=0
        
        
        #print(per_tx_val)
        #print(factor)
        #print(collateral)
        current=node
        cum_penalty=0
        time=0
        set_corruption=0
        
        if current in num_corrupted:
            set_corruption=1
        
        
            
        list_node=[]
        
        while time<max_limit and path_now<path_length:
            
            prev_current=current
            factor=False
            for node in G.neighbors(current):
                
                
                #loc_penalty=gamma*G.nodes[current]['time']*10*per_tx_val
                if time+G.nodes[prev_current]['time']+G.nodes[node]['time']<=max_limit:
                    
                    if G.edges[prev_current,node]['capacity']>10:
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
        flow=min(per_tx_val,min_capacity)
        
        
        
        
        #print(min_capacity)
        #print(min_deposit)
        #collateral=collateral+(path_now-1)*flow
        #htlc_collateral=htlc_collateral+(path_now-1)*per_tx_val
        #time_new=0
        #value=per_tx_val
        
        #count_float=float(0.9/(0.9+(flow*profit*int(2016/path_length))))
        #print(count_float)
        #print(float(corruption/100))
        lambda_set=float((val*(2016/path_length))/144)
        
        k=float(float(math.exp(-lambda_set)*pow(lambda_set,int(flow/frac)))/math.factorial(int(flow/frac)))
        
        o1=float(int(flow/frac)*k)
        
        fee1=float(o1*(1+0.000001*frac))
        
        k=float((math.exp(-lambda_set)*pow(lambda_set,80000/frac))/math.factorial(int(80000/frac)))
        o2=float((80000/frac)*k)
        fee2=float(o2*(1+0.000001*frac))
        
        x=float((1+0.000001*flow)+fee1+(1-q)*(fee2+154))
        
        y=float(1+0.000001*flow)
        print(str(y)+" "+str(x))
        calc_theta=float(y/x)        
        
        
        #theta2=0.4
        if float(corruption/100)<calc_theta:
            
            
            count_tx=count_tx+1
            if set_corruption==1:
                if random.random() <= (1-q):
                        pay_A=pay_A-fee1-fee2-154
                else:
                        pay_A=pay_A-fee1
                
                pay_B=pay_B+flow+2*fee1+154
                for e in list_node:                    
                    G.edges[e]['capacity']=G.edges[e]['capacity']-flow
        
                    
            else:
                
                    
                pay_A=pay_A+(1+0.000001*flow)    
                pay_B=pay_B+flow
                for e in list_node:
                    G.edges[e]['capacity']=G.edges[e]['capacity']-flow
            
                
        else:
                break
            
        
            
            
        
    
    return pay_A,pay_B,count_tx

def launch_attack(G,per_tx_val,path_length,adv_budget,max_limit):
    
    i=0
    collateral=0
    min_capacity=30000000000000000000000000000
    min_deposit=30000000000000000000000000000
    factor=False
    while adv_budget>0.01:
        min_capacity=30000000000000000000000000000
        min_deposit=30000000000000000000000000000
        path_now=0
        budget=0
        attacker_node=sorted(G.nodes(data=True), key=lambda x: x[1]['capacity'], reverse=True)[:G.number_of_nodes()][i][0]
        print(attacker_node)
        print(i)
        print(adv_budget)
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
                if time+G.nodes[prev_current]['time']+G.nodes[node]['time']<=max_limit:
                    
                    if G.edges[prev_current,node]['capacity']>10:
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
        flow=min(per_tx_val,min_capacity,adv_budget)
        
        
        
        
        #print(min_capacity)
        #print(min_deposit)
        collateral=collateral+(path_now-1)*flow
        #htlc_collateral=htlc_collateral+(path_now-1)*per_tx_val
        #time_new=0
        #value=per_tx_val
        
        
        
        for e in list_node:
            #time_new=time_new+G.nodes[e[0]]['time']print("ok")
        
            G.edges[e]['capacity']=G.edges[e]['capacity']-flow
            
            
        
        
        adv_budget=adv_budget-flow
        
    print(collateral)
    print(adv_budget)
    
    return collateral

        

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
    print(sys.argv[2])
    gamma=float(sys.argv[2])
    
    per_tx_val=int(sys.argv[3])
    path_length=int(sys.argv[4])
    val=int(sys.argv[5])
    G_tmp=G.copy()
    corruption=float(sys.argv[6])
    f1=open(sys.argv[8],"a")
    frac=int(sys.argv[9])
    q=float(sys.argv[10])
    num_corrupted=int(corruption*G.number_of_nodes()/100)
    
    
        
    num_transaction=int(sys.argv[7])
    #path_length=int(sys.argv[6])
    s=[]
    t=[]
    sink=[]
    source=[]
    node_list=[]
    
    num_source=100
    
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
        
    c=[]
    corrupted_nodes=[]
    
    count=0
    while count<num_corrupted:
          r=random.randint(1,G.number_of_nodes()-1)
          if r not in c: 
              c.append(r)
              count=count+1
    
    for item2 in c:    
        corrupted_nodes.append(node_list[item2])
    
    count=0
    p=[]
    
    
    
    print(len(corrupted_nodes))
    G_tmp=G.copy()
    
    
    
    pay_A,pay_B,count_tx=launch_attack_channel(G_tmp,gamma,per_tx_val,path_length,source,corrupted_nodes,corruption,val,2016,frac,q)
    #budget1=launch_attack(G_tmp,per_tx_val,path_length,adv_budget,2016)
    if count_tx==0:
        f1.write(sys.argv[1]+" "+str(per_tx_val)+" "+" "+str(path_length)+" "+str(corruption)+" "+str(0)+" "+str(0)+" "+str(val)+" "+str(frac)+" "+str(q)+"\n")
    else:    
        f1.write(sys.argv[1]+" "+str(per_tx_val)+" "+" "+str(path_length)+" "+str(corruption)+" "+str(float(pay_A/count_tx))+" "+str(float(pay_B/count_tx))+" "+str(val)+" "+str(frac)+" "+str(q)+"\n")
    G_tmp=G.copy()
    
    

    f.close()
    #mount an attack based on cut set
    #cutset_edges=attack_based_on_cutset(G_tmp,deg_node)

    #plot_graph(G)
    

if __name__ == '__main__':
    main()
