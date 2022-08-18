#!/usr/bin/env python3

import numpy as np
import networkx as nx
from pprint import pprint
from collections import defaultdict

source = 0
target = 8

# Set of all nodes
nodes = {0, 1, 2, 3, 4, 5, 6, 7, 8}

node_coords = {
    0: (0, 0),
    1: (1, 0),
    2: (2, 0),
    3: (0, 1),
    4: (1, 1),
    5: (2, 1),
    6: (0, 2),
    7: (1, 2),
    8: (2, 2),
}

# Set of unidirectional edges between nodes
edges = {
    (0, 1), (0, 3),
    (1, 0), (1, 2), (1, 4),
    (2, 1), (2, 5),
    (3, 0), (3, 4), (3, 6),
    (4, 1), (4, 3), (4, 5), (4, 7),
    (5, 2), (5, 4), (5, 8),
    (6, 3), (6, 7),
    (7, 4), (7, 6), (7, 8),
    (8, 5), (8, 7)
}


G = nx.DiGraph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

def get_paths(G, source, target):
    paths = nx.all_shortest_paths(G, source=source, target=target)
    paths = [list(nx.utils.pairwise(path)) for path in paths]
    return paths

Q = get_paths(G, source, target)
pprint(Q)

def make_R(G, Q):
    from_nodes = defaultdict(set)
    edges_taken = set()
    for path in Q:
        for (x, y) in path:
            from_nodes[y].add(x)
            edges_taken.add((x, y))

    pprint(from_nodes)
    pprint(edges_taken)
    
    R = np.zeros((len(nodes), len(nodes)))

    for node_from in G.nodes():
        for node_to in G.nodes():
            if (node_from, node_to) in edges_taken and len(from_nodes[node_to]) > 0:
                ratio = 1/len(from_nodes[node_to])
            else:
                ratio = 0

            print(node_from, node_to, ratio)

            R[node_from, node_to] = ratio

    return R

R = make_R(G, Q)
print(R)
