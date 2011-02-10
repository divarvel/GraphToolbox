#!/usr/bin/env python
#-*- encoding: utf-8 -*-
#

class Graph(object):
    """ A graph object, and the algos we can apply on it """

    def __init__(self):
        pass

    def load_data(self, data):
        " OOo style: load Data "
        self.nodes = data["nodes"]
        self.directed = data["oriented"]
        self.edges = {}

        for start in data["nodes"]:
            self.edges[start] = {}
            for stop in data["nodes"]:
                self.edges[start][stop] = {}

        for edge in data["edges"]:
            self.edges[edge["start"]][edge["stop"]] = edge

    def shortest_path(self, start, end):
        """Find the shortest path between nodes start and end
        Returns [start, node1, node2, ..., end]"""
        pass

    def max_flow(self, start, end):
        """Compute the maximum flow between nodes start and end
        Returns maximum_flow"""
        pass

    def max_flow_min_cost(self, start, end):
        """Compute the maximum flow with minimum cost between nodes start and end
        Returns (maximum_flow, minimum_cost)"""
        pass

    def transitive_closure(self):
        """Update the graph to be its transitive closure"""
        for k in self.nodes:
            for i in self.nodes:
                for j in self.nodes:
                    if self.edges[i][j] != {} or\
                       (self.edges[i][k] != {} and self.edges[k][j] != {}):
                        self.edges[i][j]["start"] = i
                        self.edges[i][j]["stop"] = j
                        self.edges[i][j]["capacity"] = 0
                        self.edges[i][j]["cost"] = 0

    def k_coloring(self, n):
        " Color the graph with n color "
        pass
