import json
import logging
import networkx as nx
import sys
import itertools

from graph_visualization_helpers import plot_graph, set_graph_color, set_node_color


def filter_snapshot_data(json_data):
    """
    Returns filtered json data by deleting disabled channels or channels without policy data
    """
    # Filter to channels having both peers exposing their policies
    json_data['edges'] = list(filter(lambda x: x['node1_policy'] and x['node2_policy'], json_data['edges']))
    # Filter to non disabled channels
    json_data['edges'] = list(filter(lambda x: not (x['node1_policy']['disabled'] or x['node2_policy']['disabled']), json_data['edges']))
    return json_data



        

def main():

    logging.basicConfig(format='\n%(levelname)s: %(message)s', level=logging.INFO)

    G = nx.Graph()

    with open(sys.argv[1]) as f:
        source = json.load(f)

    source = filter_snapshot_data(source)

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
    # Setting color for nodes
    set_graph_color(G)
    
    f.close()
    #based on fixed budget of attacker, find out the number of nodes which can be attacked
    #budget=int(sys.argv[2])
    
    #select the highest capacity node as the attacker node
    #launch_attack_griefing_no_change(G_tmp)
    #mount an attack based on cut set
    #cutset_edges=attack_based_on_cutset(G_tmp,deg_node)

    plot_graph(G)
    

if __name__ == '__main__':
    main()
