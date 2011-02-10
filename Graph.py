#!/usr/bin/env python
#-*- encoding: utf-8 -*-
#

class Graph(object):
    """ A graph object, and the algos we can apply on it """

    def __init__(self):
        pass

    def load_data(self, data):
        " OOo style: load Data "
        self.graph = data
        self.edges = {}
        for edge in self.graph["edges"]:
            self.edges[edge["start"]] = {}
            self.edges[edge["start"]][edge["stop"]] = edge

        print self.edges["id1"]["id2"]

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
        " Update the graph to be its transitive closure "
        pass


    def k_coloring(self, n):
        " Color the graph with n color "
        pass
