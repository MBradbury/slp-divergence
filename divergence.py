import math

import numpy as np
from more_itertools import pairwise
from methodtools import lru_cache

from routing import RoutingMatrix, AtoG

class RoutingDivergenceMatrix(RoutingMatrix):
    @lru_cache(maxsize=None)
    def pathsWithPr(self, Aname: str, time_limit: int, source: int) -> list:
        A = self.get(Aname)
        G = AtoG(A)

        ps = self.findPaths(G, source=source, depth_limit=time_limit)

        ppaths = []
        for path in ps:
            path = list(pairwise(path))

            pr = 1
            for i, j in path:
                pr *= A[i, j]

            ppaths.append((path, pr))

        assert sum(pr for (path, pr) in ppaths) == 1

        return ppaths

    @lru_cache(maxsize=None)
    def PrN(self, Aname: str, n: int, t1: int, start: int) -> float:
        """Probability that transition `n` is taken at `t1`, given the attacker started at `start`"""
        A = self.get(Aname)

        nodes = list(range(A.shape[0]))

        assert t1 > 0
        assert start in nodes

        # Calculate two different ways to validate

        result1 = A[n] * np.linalg.matrix_power(A, (t1-1))[start, n[0]]

        paths = self.pathsWithPr(Aname, t1, source=start)

        result = sum(
            pr
            for (path, pr) in paths
            if path[t1-1] == n
        )

        assert np.isclose(result, result1)

        try:
            assert 0 <= result <= 1
        except AssertionError:
            print(n, t1, start, result)
            raise

        return result

    def maxH(self, transitions=None) -> float:
        if transitions is None:
            transitions = self.Lall

        return math.log2(len(transitions))

    @lru_cache(maxsize=None)
    def H(self, Aname: str, t: int, start: int) -> float:
        assert t > 0

        L = self.trans(Aname)

        h = 0.0
        for l in L:
            pn = self.PrN(Aname, l, t, start=start)

            if pn == 0:
                continue

            h += pn * math.log2(pn)

        h = -h

        # Make negative 0, regular zero
        if h == -0.0:
            h = 0.0

        assert 0.0 <= h <= self.maxH()

        return h

    @lru_cache(maxsize=None)
    def DJS(self, A1: str, A2: str, t1: int, t2: int, start: int) -> float:
        assert t1 > 0
        assert t2 > 0

        h = 0.0
        for l in self.trans(A1) | self.trans(A2):
            pn = 0.5 * self.PrN(A1, l, t1, start=start)
            ps = 0.5 * self.PrN(A2, l, t2, start=start)

            pc = pn + ps

            # Avoid passing 0 to log2
            if pc == 0:
                continue

            h += pc * math.log2(pc)

        h = -h

        h1 = self.H(A1, t1, start=start)
        h2 = self.H(A2, t2, start=start)

        h = h - (0.5 * h1 + 0.5 * h2)

        # Make negative 0, regular zero
        if h == -0.0:
            h = 0.0

        # Bounded above by 1 due to log2
        assert 0 <= h <= 1

        return h
