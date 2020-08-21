# SLP Divergence

This repository contains the scripts to generate graphs for the paper 'Quantifying Performance of Source Location Privacy Routing via Divergence and Information Loss'.

## Setup

```bash
python3 -m pip install numpy networkx methodtools more_itertools
sudo apt-get install gnuplot-nox
```

## Run

Configure main.py with the nodes and edges of the network and the normal (Rn) and SLP (Rs) routing matrices.

```bash
python3 main.py
```

## Graph

```bash
cd graphs
gnuplot *.gp
```
