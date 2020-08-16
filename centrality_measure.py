import logging
import networkx as nx
import sys

def filter_snapshot_data(json_data):
    """
    Returns filtered json data by deleting disabled channels or channels without policy data
    """
    # Filter to channels having both peers exposing their policies
    json_data['edges'] = list(filter(lambda x: x['node1_policy'] and x['node2_policy'], json_data['edges']))
    # Filter to non disabled channels
    json_data['edges'] = list(filter(lambda x: not (x['node1_policy']['disabled'] or x['node2_policy']['disabled']), json_data['edges']))
    return json_data


def set_node_capacity(G):
    """
    Returns node's total capacity (sum of the capacities on its adjacent edges)
    """
    #neighbours = G.adj[node]._atlas
    nx.set_node_attributes(G, 0, 'capacity')
    for node in G.nodes:
        for neighbor in G.neighbors(node):
            channel_details = G.get_edge_data(node, neighbor, {'capacity':0})
            G.nodes[node]['capacity'] = G.nodes[node]['capacity'] + int(channel_details['capacity'])
        

        #b['capacity']+=a['capacity']
    #print(nx.neighbors(node))
    #return sum([neighbours[adj_node_id][channel_id]['capacity'] for adj_node_id in neighbours for channel_id in
     #           neighbours[adj_node_id]])

    
    
def set_deg_nodes(G):
    """
    Given a graph, put degree info of each node as an attribute 
    """
    degrees = dict(G.degree())
    nx.set_node_attributes(G, degrees, 'degree')
    

def set_bet_centrality(G):
    """
    Given a graph, put betweenness_centrality info of each node as an attribute 
    """
    measure_of_centrality = nx.betweenness_centrality(G, k=None, normalized=True, weight=None, endpoints=False, seed=None)
    nx.set_node_attributes(G, measure_of_centrality, 'betweenness_centrality')


def mount_attack(G, attacker_node, target_node):
    """
    Given a graph, an attacker node and a node to target, mount a griefing attack using self payment
    """

    # # For testing, let us change outgoing channel capacities of target with neighbors to 0
    # nx.set_node_attributes(G, {target_node:{'capacity':0}})
    # for neighbor in G.neighbors(target_node):
    #     G.edges[target_node, neighbor]['capacity'] = 0

    # Attempt 1: Find all edge disjoint paths. Select two such paths: A->T and T->A. Deplete capacity in this path. 

    paths = nx.edge_disjoint_paths(G, attacker_node, target_node)
    # TODO: check atleast two paths exist. paths is a generator. how to efficiently do this?

    try:
        attacker_to_target_path = next(paths)
        target_to_attacker_path = next(paths)
        target_to_attacker_path.reverse()
        complete_loop = attacker_to_target_path + target_to_attacker_path[1:]
        logging.info('Self loop from attacker to attacker via target: %s', complete_loop)

        attack_capacity = min([int(G.edges[a,b]['capacity']) for a,b in zip(complete_loop[:-1], complete_loop[1:])])
    
        for a,b in zip(complete_loop[:-1], complete_loop[1:]):
            # TODO: change node capacities as well?
            G.edges[a,b]['capacity'] = int(G.edges[a,b]['capacity']) - attack_capacity
            #print(G.edges[a,b]['capacity'])
        
        logging.info('Attack mounted with capacity: %d', attack_capacity)
        
    except StopIteration:
        logging.error('Not enough edge disjoint path between target and attacker.')
    
    # TODO: do so for max possible loops? 

    
def find_attacker (G):
    """
    Given a graph, find the attacker. Returns node id of attacker if found, else '-1'
    Strategy: The node most benefitted in terms of betweenness centrality by removal of target node, is our attacker
    Assumption: Given graph has target removed. Original bet_centrality set as an attribute
    """

    nx.betweenness_centrality(G, k=None, normalized=True, weight=None, endpoints=False, seed=None)
    sort_centrality = sorted(nx.betweenness_centrality(G, k=None, normalized=True, weight=None, endpoints=False, seed=None).items(), key=lambda x: x[1], reverse=True)
    sort_centrality = sort_centrality[:10]
#    print("\n centrality\n")
#    print(sort_centrality)
    
    for node in sort_centrality:
        if (node[1] - G.nodes[node[0]]['betweenness_centrality']) > 0:
            print(node[1], G.nodes[node[0]]['betweenness_centrality'])
            return node[0]
    
    return '-1'
    #for node in G.nodes:
        #G.nodes[node]['betweeneness_centrality']<
    
    
def calculate_profit (G, attacker_node, target_node):
    """ 
    Given a graph, an attacker node and a node to target, calculate the estimated profit that attacker gains
    bcoz of blocking off the target node
    """
    # Idea 1: Assume target node eliminated. Assume components C1, C2 s.t. C1->A->C2. Find max flow from C1->C2. 
    # Problem: What if target node is not eliminated. What if removing T and A does not give components C1,C2? 
    return 0 
    

def find_attacker_and_target (G):
    """
    Given a graph, find the perfect attacker and target node pair and return their pubkeys
    Assumption: bet_centrality set as an attribute
    """

    
    
    
    
    centrality_id = sorted(G.nodes(data=True), key=lambda x:x[1]['betweenness_centrality'], reverse=True)
    
    # select a victim node with high betweeneness_centrality and attacker node with low betweeneness_centrality. The logic behind this is to ensure that attacker_node is the one which previously didn't get many transactions request and hence earned low processing fee
    #victim_node=centrality_id[0][0]
    for node in centrality_id:
        if G.nodes[node[0]]['betweenness_centrality'] == 0:
            attacker_node = node[0]
    return attacker_node


def connect_supper_source_sink(G, centrality_node_list, attack_node=None):
    """
    select last 50 minimum degree nodes as source
    """
    count = 0
    
    for edge in centrality_node_list:
        if G.nodes[edge[0]]['degree']>1:
            break
        count = count+1                
    
    # consider all the nodes which have degree 1, divide the set into 2 parts, one forming source set and other sink set
    # TODO: better names for a and b
    a = int(count/2)
    b = int(count/2+1)
    logging.info("Number of source-sink pairs\n")
    print(a)
    multi_source = get_id(centrality_node_list[:a])
    multi_sink = get_id(centrality_node_list[b:count])
    
    #print(multi_source)
    #print(multi_sink)
        
    
    
    #do not include attacker node in the set
    if attack_node in multi_source:
        multi_source.remove(attack_node)
        
    #do not include victim node in the set    
    if attack_node in multi_sink:
        multi_sink.remove(attack_node)
    
    #select the next 50 minimum degree nodes as sinl
    
    
    #super source 0 and super sink 1
    G.add_node('0')
    G.add_node('1')
    
    #add edges of very large capacity to super source and super sink
    for node in multi_source:
        G.add_edge('0', node, capacity=300000000000000000000)

    for node in multi_sink:
        G.add_edge(node, '1', capacity=300000000000000000000)        
    
    for edge in G.edges:
        G.edges[edge]['weight'] = int(G.edges[edge]['capacity'])
    
    return multi_source

def read_graph(source):
    """
    Read a graph from source and filter out the data to form a networkx graph object
    Source is assumed to be a dictionary formed from reading json data as supplied in snapshot
    """

    G = nx.Graph()
    
    for node in source['nodes']:
        G.add_node(node['pub_key'], alias=node['alias'])
        
    #    print('Adding node with pubkey', node['pub_key'])

    # print(G.nodes)
    # 

    for edge in source['edges']:
        G.add_edge(edge['node1_pub'], edge['node2_pub'], capacity=edge['capacity'],time1=edge['node1_policy']['time_lock_delta'],time2=edge['node2_policy']['time_lock_delta'],base1=edge['node1_policy']['fee_base_msat'],base2=edge['node2_policy']['fee_base_msat'],feerate1=edge['node1_policy']['fee_rate_milli_msat'],feerate2=edge['node2_policy']['fee_rate_milli_msat'],channel_id=edge['channel_id'])

    # print('total edges:', G.number_of_edges())
    
    # Removing isolated nodes
    #print(nx.number_of_isolates(G))
    G.remove_nodes_from(list(nx.isolates(G)))

    
    c = max(nx.connected_components(G), key=len)
    G=G.subgraph(c).copy() 
    print('total nodes:', G.number_of_nodes())
    print('total edges:', G.number_of_edges())
    
    nx.set_edge_attributes(G,0,'deposit2')
    nx.set_node_attributes(G,0,'time')
    nx.set_node_attributes(G,0,'basefee')
    nx.set_node_attributes(G,0,'rate')
    # making channels dual funded by splitting capacities equally
    for edge in G.edges:
        G.edges[edge]['capacity'] = int(G.edges[edge]['capacity'])/2
        G.edges[edge]['deposit2'] = int(G.edges[edge]['capacity'])
        if int(G.edges[edge]['time1'])>0 and int(G.edges[edge]['time2'])>0 :
            G.nodes[edge[0]]['time'] = int(G.edges[edge]['time1'])
            G.nodes[edge[1]]['time'] = int(G.edges[edge]['time2'])
            
            if G.nodes[edge[0]]['basefee'] == 0:
                G.nodes[edge[0]]['basefee'] = int(G.edges[edge]['base1'])
            
            if G.nodes[edge[1]]['basefee'] == 0:
                G.nodes[edge[1]]['basefee'] = int(G.edges[edge]['base2'])
                
            if G.nodes[edge[0]]['rate'] == 0:    
                G.nodes[edge[0]]['rate'] = int(G.edges[edge]['feerate1'])
                
            if G.nodes[edge[1]]['rate'] == 0:        
                G.nodes[edge[1]]['rate'] = int(G.edges[edge]['feerate2'])
            
    return G

