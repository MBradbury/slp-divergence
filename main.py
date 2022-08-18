#!/usr/bin/env python3

import numpy as np
from pprint import pprint

from routing import RoutingMatrix, tstr, tnorm, AtoG
from divergence import RoutingDivergenceMatrix
import ppp

import matplotlib.pyplot as plt
import networkx as nx

def drawrmat(R, name):
    G = AtoG(R)

    nx.draw_networkx(G, pos=node_coords)
    nx.draw_networkx_edge_labels(G, pos=node_coords, edge_labels=nx.get_edge_attributes(G, 'weight'))

    plt.savefig(f"{name}.pdf")
    plt.clf()

# Define the network structure

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

# The protectionless routing matrix
Rn = np.array([
    [0, 1, 0, 1, 0  , 0  , 0, 0  , 0  ],
    [0, 0, 1, 0, 0.5, 0  , 0, 0  , 0  ],
    [0, 0, 0, 0, 0  , 0.5, 0, 0  , 0  ],
    [0, 0, 0, 0, 0.5, 0  , 1, 0  , 0  ],
    [0, 0, 0, 0, 0  , 0.5, 0, 0.5, 0  ],
    [0, 0, 0, 0, 0  , 0  , 0, 0  , 0.5],
    [0, 0, 0, 0, 0  , 0  , 0, 0.5, 0  ],
    [0, 0, 0, 0, 0  , 0  , 0, 0  , 0.5],
    [0, 0, 0, 0, 0  , 0  , 0, 0  , 0  ],
])

drawrmat(Rn, "Rn")

# The SLP routing matrix of interest
Rs = np.array([
    [0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 1, 0, 0, 0],
])

drawrmat(Rs, "Rs")

r = RoutingMatrix(nodes, edges, Rn, Rs)

print("N Transitions:", list(map(tstr, r.trans("An"))))
print("S Transitions:", list(map(tstr, r.trans("As"))))

source = 0

# Generate set of properly perturbed paths
p = ppp.getppp(r, source=source, sink=4, safety_period=4)
print("Properly perturbed paths=")
pprint(p)

# Generate the SLP routing matrix from the set of ppps
gRs = ppp.generateRs(r, source=source, sink=4, safety_period=4)
print(gRs)
drawrmat(gRs, "gRs")
gr = RoutingDivergenceMatrix(nodes, edges, Rn, gRs)

def ecaptab(routing, name, A, end):
    print(f"E[C({name})]")
    for node in routing.nodes:
        print(f"{node+1} {routing.ECapture(A, start=node, end=end)}")

# The expected time to capture the source
# when the attacker starts at different nodes in the network
ecaptab(r, "N", "An", end=source)
ecaptab(r, "S", "As", end=source)

def ecappr(routing, name, A, end, max_safety):
    print(f"E[CPr({name})]")
    with open(f"graphs/ECPr{name}.dat", "w") as f:
        print(f"#node safety pr", file=f)
        for node in routing.nodes:
            for safety in range(max_safety+1):
                print(f"{node+1:^4} {safety:^4}" + " ".join(
                    f"{h:.1f} "
                    for h in [routing.Edelta(A, start=node, end=end, safety=safety)]
                ).rstrip(), file=f)
    with open(f"graphs/ECPr{name}.dat", "r") as f:
        for line in f:
            print(line.strip())

ecappr(r, "N", "An", end=source, max_safety=14)
ecappr(r, "S", "As", end=source, max_safety=14)


dr = RoutingDivergenceMatrix(nodes, edges, Rn, Rs)

# Validate the single probabilities
print("Checking probability validity...")
check_time = 4
for node in dr.nodes:
    pn = {
        tnorm(n): dr.PrN("An", n, check_time, start=node)
        for n in dr.trans("An")
        if dr.PrN("An", n, check_time, start=node) > 0
    }

    psum = sum(pn.values())

    print("An", node+1, psum, pn)
    assert psum == 1

    pn = {
        tnorm(f): dr.PrN("As", f, check_time, start=node)
        for f in dr.trans("As")
        if dr.PrN("As", f, check_time, start=node) > 0
    }

    psum = sum(pn.values())

    print("As", node+1, psum, pn)
    assert psum == 1
print("Finished checking validity!")

print("MAX H", dr.maxH())

def h_table(name: str, Aname: str):
    with open(f"graphs/H{name}.dat", "w") as f:
        print(f"#H({name})" + " ".join(f"{node+1:^4}" for node in dr.nodes).rstrip(), file=f)
        for t in range(1, 16):
            print(f"{t:^4}" + " ".join(
                f"{h:.1f} " #if h != 0 else "    "
                for node in dr.nodes
                for h in [dr.H(Aname, t, start=node)]
            ).rstrip(), file=f)
    with open(f"graphs/H{name}.dat", "r") as f:
        for line in f:
            print(line.strip())

# Show the entropy for the two matrices
h_table("N", "An")
h_table("S", "As")

def divergence_table(fnname: str, name: str, A1name: str, A2name: str):
    with open("graphs/JSD.dat", "w") as f:
        print(f"#{fnname}({name})" + " ".join(f"{node+1:^4}" for node in dr.nodes).rstrip(), file=f)
        for t in range(1, 11):
            print(f"{t:^9}" + " ".join(
                f"{h:.1f} " #if h != 0 else "    "
                for node in dr.nodes
                for h in [dr.DJS(A1name, A2name, t, t, start=node)]
            ).rstrip(), file=f)
    with open("graphs/JSD.dat", "r") as f:
        for line in f:
            print(line.strip())

def divergence_3d_table(fnname: str, name: str, A1name: str, A2name: str):
    with open("graphs/JSD3D.dat", "w") as f:
        print(f"#{fnname}({name})" + " ".join(f"{node+1:^4}" for node in dr.nodes).rstrip(), file=f)
        for t1 in range(1, 11):
            for t2 in range(1, 11):
                print(f"{t1:^4} {t2:^4}" + " ".join(
                    f"{h:.1f} " #if h != 0 else "    "
                    for node in dr.nodes
                    for h in [dr.DJS(A1name, A2name, t1, t2, start=node)]
                ).rstrip(), file=f)
    with open("graphs/JSD3D.dat", "r") as f:
        for line in f:
            print(line.strip())

# Create the Jensen-Shannon Divergence table for when the transition time is the same
divergence_table("DJS", "S||N", "As", "An")

# Create the Jensen-Shannon Divergence table for different transition times
divergence_3d_table("DJS", "S||N", "As", "An")
