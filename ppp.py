#!/usr/bin/env python3

import math
import random

import numpy as np
import networkx as nx
from more_itertools import pairwise
from pprint import pprint

from routing import AtoG

def getppp(routing, source: int, sink: int, safety_period: int) -> set:
    """Obtain the set of properly perturbed paths"""

    ps = routing.paths("An", safety_period, source=sink)

    ecap = int(routing.ECapture("An", start=sink, end=source))

    ppp = set()
    for p in ps:
        consumed = []
        for (i, j) in p:
            if i == source:
                break

            for n in routing.nodes:
                # n is already being used, so don't perturb via it
                if routing.An[i, n] > 0:
                    continue

                possible_paths = [
                    tuple(pairwise(newp))

                    for newp in nx.all_simple_paths(routing.G, source=sink, target=source)

                    # The path starts the same
                    if consumed == list(pairwise(newp))[:len(consumed)]

                    # The path goes via n
                    if newp[len(consumed)] == n
                ]
                
                possible_paths = [
                    allp

                    for allp in possible_paths

                    # The path is longer than the safety period
                    if len(allp) > safety_period

                    # The possible path is not already a path in the routing matrix
                    if all(list(origp[0:ecap]) != list(allp[0:ecap]) for origp in ps)
                ]

                # Reverse the path
                possible_paths = [
                    tuple((e[1], e[0])
                    for e in reversed(allp))
                    for allp in possible_paths
                ]

                ppp = ppp.union(possible_paths)

            consumed.append((i,j))

    return ppp

def generateRs(routing, source: int, sink: int, safety_period: int) -> np.array:
    Rs = routing.Rn.copy()

    ppp = getppp(routing, source, sink, safety_period)

    # Randomly chose one of the properly perturbed paths
    p = random.choice(list(ppp))

    for (i, j) in p:
        for k in routing.nodes:
            if k == i:
                continue

            # Remove this transition
            Rs[k, j] = 0

        # Add this part of the path
        Rs[i, j] = 1

    # Remove paths that do not terminate at the sink

    # Find all the paths that do terminate there
    newps = list(nx.all_simple_paths(AtoG(Rs), source=source, target=sink))

    to_remove = set()

    # Remove paths that terminate at every other node
    # As long as they are not sub-paths of the added path
    for k in routing.nodes:
        if k == sink:
            continue

        badps = list(nx.all_simple_paths(AtoG(Rs), source=source, target=k))

        for badp in badps:
            # If this path is a sub-path of one of the good paths we should not remove it
            if any(badp == newp[0:len(badp)] for newp in newps):
                continue

            to_remove |= set(pairwise(badp))

    # Remove all the identified transitions
    for (i, j) in to_remove:
        Rs[i, j] = 0

    return Rs
