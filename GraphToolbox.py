#!/usr/bin/env python
#-*- encoding: utf-8 -*-
#

import sys, os, json
from optparse import OptionParser

class Graph(object):
    """ A graph object, and the algos we can apply on it """
    def __init__(self):
        pass
    def load_data(self, data):
        " OOo style: load Data "
        self.graph = data

    def shortest_path(self, start, end):
        " Find the shortest path between two nodes "
        pass

    def max_flow(self, start, end):
        " Compute the maximum flow between two nodes "
        pass

    def max_flow_min_cost(self, start, end):
        " Compute the maximum flow with minimal cost between two nodes "
        pass

    def transitive_closure(self):
        " Update the graph to be its transitive closure "
        pass

	def k_coloring(self, n):
		" Color the graph with n color "
		pass

class GraphToolbox(object):
    """Implement some well known graph-related algos"""
    def __init__(self):
        " Parse the commands provided by the user"

        parser = OptionParser()
        (options, args) = parser.parse_args()

        #The first arg is the input file
        self._load_graph(args[0])

        if len(args) > 1:
            action = args[1]
            if action == "path":
                if len(args) >= 4:
                    # Shortest path between 2 nodes
                    print "Shortest path between %s and %s" % (args[2], args[3])
                    path = self.graph.shortest_path(args[2], args[3])

    def _load_graph(self, path):
        " Create a new graph from the input file "
        self.graph = Graph()
        with open(path) as fp:
            self.graph.load_data(json.load(fp))

if __name__ == '__main__':
    main = GraphToolbox()
