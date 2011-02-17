#!/usr/bin/env python
#-*- encoding: utf-8 -*-
#

import json, os
from optparse import OptionParser
from Graph import Graph

class GraphToolbox(object):
    """Implement some well known graph-related algos"""

    def __init__(self):
        """Parse the commands provided by the user"""

        # Get options
        parser = OptionParser()
        (options, args) = parser.parse_args()

        # Check options count
        if len(args) < 2:
            GraphToolbox.print_help()
            return

        # The first arg is the input file
        if os.path.exists(args[0]):
            self._load_graph(args[0])
        else:
            print "File", args[0], "does not exist"
            return

        action = args[1]
        if action == "dijkstra": # Shortest path between 2 nodes
            if len(args) >= 4:
                print "Shortest path between %s and %s" % (args[2], args[3])
                path = self.graph.shortest_path(args[2], args[3])
                print path
        elif action == "fordbellman":
            if len(args) >=4:
                print "Shortest (Ford-Bellman) path between %s and %s" % (args[2], args[3])
                path = self.graph.ford_bellman(args[2], args[3])
                print path
        elif action == "maxflow":
            if len(args) >= 4: # Maximum flow between two nodes
                print "Compute maximum flow between %s and %s" % (args[2],
                                                                  args[3])
                self.graph.max_flow(args[2], args[3])

                for (start, line) in self.graph.edges.iteritems():
                    for (stop, edge) in line.iteritems():
                        if edge != {} and edge["flow"] >= 0:
                            print "(%s %s) %s"  % (start, stop, edge["flow"])
        elif action == "maxflowmincost": # Maximum flow with minimal cost
            if len(args) >= 4:
                print "Compute maximum flow with minimal cost", \
                      "between %s and %s" % (args[2], args[3])
                self.graph.max_flow_min_cost(args[2], args[3])

                for (start, line) in self.graph.edges.iteritems():
                    for (stop, edge) in line.iteritems():
                        if edge != {} and edge["flow"] >= 0:
                            print "(%s %s) %s"  % (start, stop, edge["flow"])
        elif action == "closure": # Transitive closure
            print "Transitive closure"
            self.graph.transitive_closure()
            self._write_graph("test.json")
        elif action == "kcoloring": # kcoloring of the graph
            print "Welsh & Powell k-coloring"
            print "Number of color found:", self.graph.k_coloring()
            self._write_graph("test.json")
        else:
            print "Unknow action:", action
            GraphToolbox.print_help()

    def _load_graph(self, path):
        """Create a new graph from the input file"""
        self.graph = Graph()
        with open(path) as fp:
            self.graph.load_data(json.load(fp))

    def _write_graph(self, path):
        """Write the graph in a JSON file"""
        with open(path, 'w') as fp:
            json.dump(self.graph.write_data(), fp, indent = 4)

    @staticmethod
    def print_help():
        """Display help message"""
        print "Arguments:"
        print "    input_file action action_specific_arguments"
        print "Actions and specific arguments:"
        print "    [dijkstra|fordbellman|maxflow|maxflowmincost] start_node stop_node"
        print "    [closure|kcoloring]"

if __name__ == '__main__':
    main = GraphToolbox()
