from itertools import product, tee

import numpy as np
import networkx as nx
from methodtools import lru_cache
from more_itertools import pairwise

def Amat(R: np.array) -> np.array:
    R = R.T.copy()

    # Need to add transitions that keep the attacker at a node if there are no outwards edges
    for row in range(R.shape[0]):
        if R[row,:].sum() == 0:
            R[row, row] = 1.0
    R.flags.writeable = False
    return R

def AtoG(A: np.array) -> nx.DiGraph:
    nodes = list(range(A.shape[0]))

    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_weighted_edges_from([
        (i, j, A[i, j])
        for i, j in product(nodes, nodes)
        if A[i, j] > 0
    ])
    return G

def tnorm(t):
    return (t[0]+1, t[1]+1)

def tstr(t):
    return str(tnorm(t))

class RoutingMatrix:
    def __init__(self, nodes: set, edges: list, Rn: np.array, Rs: np.array=None):
        self.nodes = nodes
        self.edges = edges

        self.G = nx.DiGraph()
        self.G.add_nodes_from(self.nodes)
        self.G.add_edges_from(self.edges)

        self.Lall = list(product(self.nodes, self.nodes))

        self._check_rmat(Rn)

        self.Rn = Rn.copy()
        self.An = Amat(Rn)

        self._check_amat(self.An)

        if Rs is not None:
            self._check_rmat(Rs)

            self.Rs = Rs.copy()
            self.As = Amat(Rs)

            self._check_amat(self.An)

    def _check_rmat(self, R):
        # Transitions that cannot be taken are not in the matrices
        if not all(R[i, j] == 0 for i in self.nodes for j in self.nodes if (i, j) not in self.edges):
            raise RuntimeError("There are no transitions")

        # Columns Sum to <= 1
        if not all(R[:, j].sum() <= 1 for j in range(len(self.nodes))):
            raise RuntimeError("Columns do not sum to 1")

    def _check_amat(self, A):
        # Rows Sum to 1
        if not all(A[i, :].sum() == 1 for i in range(len(self.nodes))):
            raise RuntimeError("Rows do not sum to 1")

    def get(self, name):
        if name not in ("An", "As", "Rn", "Rs"):
            raise RuntimeError(f"Invalid matrix name {name}")

        return getattr(self, name, None)

    def findPaths(self, G, source: int, depth_limit: int) -> list:
        if depth_limit == 0:
            return [[source]]
        ps = [
            [source] + path
            for neighbor in G.neighbors(source)
            for path in self.findPaths(G, source=neighbor, depth_limit=depth_limit-1)
        ]

        assert all(len(path) == depth_limit + 1 for path in ps)

        return ps

    @lru_cache(maxsize=None)
    def paths(self, Aname: str, time_limit: int, source: int) -> list:
        A = self.get(Aname)
        G = AtoG(A)

        ps = self.findPaths(G, source=source, depth_limit=time_limit)

        ppaths = []
        for path in ps:
            path = list(pairwise(path))

            ppaths.append(path)

        return ppaths

    @lru_cache(maxsize=None)
    def trans(self, Aname: str, start=None) -> set:
        """Get the possible transitions in R"""
        A = self.get(Aname)

        L = set()
        if start is None:
            for i in range(A.shape[0]):
                for j in range(A.shape[1]):
                    if A[i, j] != 0:
                        L.add((i, j))
        else:
            G = AtoG(A)
            L = set(nx.edge_dfs(G, source=start))

        return L

    ##########################################################

    def hitting_probability(self, A: np.array, i: int, end: int) -> float:
        nodes = list(range(A.shape[0]))

        if i == end:
            return 1.0
        else:
            return sum(
                A[i, j] * self.hitting_probability(A, j, end) if A[i, j] != 0 else 0.0
                for j in nodes
                if i != j
            )

    def expected_hitting_time(self, A: np.array, i: int, end: int) -> float:
        if self.hitting_probability(A, i, end) < 1:
            return float("inf")

        nodes = list(range(A.shape[0]))

        if i == end:
            return 0.0
        else:
            return 1 + sum(
                A[i, j] * self.expected_hitting_time(A, j, end) if A[i, j] != 0 else 0
                for j in nodes
                if i != j
            )

    @lru_cache(maxsize=None)
    def ECapture(self, Aname: str, start: int, end: int):
        """The expected capture time when the attacker starts at `start` and ends at `end`"""
        A = self.get(Aname)
        nodes = list(range(A.shape[0]))

        assert start in nodes
        assert end in nodes

        return self.expected_hitting_time(A, start, end)

    ##########################################################
