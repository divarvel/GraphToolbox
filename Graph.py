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

    def max_flow(self, start, stop):
        """Compute the maximum flow between nodes start and end
        Returns maximum_flow"""

        for start_id in self.edges:
            for stop_id in self.edges:
                if self.edges[start_id][stop_id] != {} \
                   and not self.edges[start_id][stop_id].has_key("flow"):
                    self.edges[start_id][stop_id]["flow"] = 0;

        self.nodes[start]["marked"] = "+"

        path = self._max_flow_find_path(start, stop, [])
        while path != None:
            flow = min(remaining_capacity for (edge, remaining_capacity) in path)
            for (edge, remaining_capacity) in path:
                edge["flow"] += flow
                if self.edges[edge["stop"]][edge["start"]] == {}:
                    self.edges[edge["stop"]][edge["start"]]["flow"] = 0
                    self.edges[edge["stop"]][edge["start"]]["capacity"] = -edge["capacity"]
                self.edges[edge["stop"]][edge["start"]]["flow"] -= flow
            path = self._max_flow_find_path(start, stop, [])

    def _max_flow_find_path(self, start, stop, path):
        if start == stop:
            return path

        for node_id in self.edges[start]:
            if self.edges[start][node_id] != {}:
                edge = self.edges[start][node_id]
                remaining_capacity = edge["capacity"] - edge["flow"]
                if remaining_capacity > 0 \
                   and not (edge, remaining_capacity) in path:
                    new_path = self._max_flow_find_path(node_id,
                                                        stop,
                                                        path +
                                                        [(edge, remaining_capacity)])

                    if new_path != None:
                        return new_path


    def max_flow_min_cost(self, start, end):
        """Compute the maximum flow with minimum cost between nodes start and end
        Returns (maximum_flow, minimum_cost)"""
        pass

    def transitive_closure(self):
        " Update the graph to be its transitive closure "
        pass
        for node in self.graph.nodes:
            for edge in self.graph.edges:
                if edge.start == node:
                    pass


    def k_coloring(self, n):
        " Color the graph with n color "
        pass
