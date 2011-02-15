#!/usr/bin/env python
#-*- encoding: utf-8 -*-
#

import json
from optparse import OptionParser
from Graph import Graph

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
            elif action == "maxflow":
                if len(args) >= 4:
                    # Maximum flow between two nodes
                    print "Compute maximum flow between %s and %s" % (args[2],
                                                                     args[3])
                    self.graph.max_flow(args[2], args[3])

                    for start in self.graph.edges:
                        for stop in self.graph.edges:
                            edge = self.graph.edges[start][stop]

                            if edge != {} and edge["flow"] >= 0:
                                print "(%s %s) %s"  % (start,
                                                       stop,
                                                       edge["flow"])
            elif action == "closure":
                print "Transitive closure"
                self.graph.transitive_closure()
                self._write_graph("test.json")
            elif action == "kcoloring":
                print "Welsh & Powell k-coloring"
                self.graph.k_coloring()
                self._write_graph("test.json")

    def _load_graph(self, path):
        " Create a new graph from the input file "
        self.graph = Graph()
        with open(path) as fp:
            self.graph.load_data(json.load(fp))

    def _write_graph(self, path):
        """Write the graph in a JSON file"""
        with open(path, 'w') as fp:
            json.dump(self.graph.write_data(), fp, indent = 4)

if __name__ == '__main__':
    main = GraphToolbox()
