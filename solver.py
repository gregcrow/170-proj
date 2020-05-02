import networkx as nx
from networkx.algorithms import approximation as ax
from parse import *
from utils import is_valid_network, average_pairwise_distance, average_pairwise_distance_fast
import sys
import os


def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """

    # TODO: your code here!
    v = ax.min_weighted_dominating_set(G)
    T = ax.steiner_tree(G, v)
    if (len(T.nodes) == 0):
    	T_prime = T.copy()
    	T_prime.add_node(0)
    	return T_prime
    return reverse_prune(G, T.copy())


def reverse_prune(G, T):
	averageDist = average_pairwise_distance_fast(T) 
	# print(averageDist)
	if (averageDist == 0):
		return G
	T_prime = T.copy()
	T_set_one = set(T.nodes())
	# print(T_prime.edges(), len(T_prime.edges()))
	for node in T_set_one:
		for neighbor in G.neighbors(node):		
			# if (T_prime.has_edge(edge[0],edge[1])):
			# 	print("Uh-oh")
			if (T.has_edge(node, neighbor)):
				T_prime.remove_edge(node, neighbor)

				if (T_prime.degree(neighbor) == 0):
					T_prime.remove_node(neighbor)

				if (nx.is_connected(T_prime) and nx.is_dominating_set(G, T_prime.nodes)):
					T_prime_dist = average_pairwise_distance_fast(T_prime)
					if (T_prime_dist < averageDist):
						# print(len(T.edges()), len(T_prime.edges()))
						T = T_prime
						averageDist = T_prime_dist
					else:
						T_prime.add_edge(neighbor, node, weight = G.get_edge_data(node, neighbor)['weight'])
				else:
					T_prime.add_edge(neighbor, node, weight = G.get_edge_data(node, neighbor)['weight'])
			# else:
			# 	T_prime.add_edge(neighbor, node, weight = G.get_edge_data(node, neighbor)['weight'])
			# 	T_prime.remove_edge(node)
			# 	if (nx.is_connected(T_prime)):
			# 		T_prime_dist = average_pairwise_distance_fast(T_prime)
			# 		if (T_prime_dist < averageDist):
			# 			T = T_prime
			# 			averageDist = T_prime_dist
			# 	else:
			# 		T_prime.add_node(node)
			# 		for new_neighbor_two in list_neighbors:
			# 			T_prime.add_edge(neighbor, new_neighbor, weight = G.get_edge_data(new_neighbor_two, node)['weight'])
	T_set = set(T.nodes())
	for node in T_set:
		for neighbor in G.neighbors(node):		
			# if (T_prime.has_edge(edge[0],edge[1])):
			# 	print("Uh-oh")
			if (not T.has_node(neighbor)):
				T_prime.add_edge(node, neighbor, weight = G.get_edge_data(node, neighbor)['weight'])
				T_prime_dist = average_pairwise_distance_fast(T_prime) 
				if (T_prime_dist < averageDist):
					T = T_prime
					averageDist = T_prime_dist
				else:
					T_prime.remove_node(neighbor)
	# print(len(T.edges()))	
	# print(len(T.edges))
	return T



# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == "__main__":
    output_dir = "submission"
    input_dir = "inputs"
    for input_path in os.listdir(input_dir):
        graph_name = input_path.split(".")[0]
        G = read_input_file(f"{input_dir}/{input_path}")
        T = solve(G)
        write_output_file(T, f"{output_dir}/{graph_name}.out")
