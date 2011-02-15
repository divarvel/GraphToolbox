#!/usr/bin/env python
#-*- encoding: utf-8 -*-
#

import sys

class Graph(object):
    """A graph object, and the algos we can apply on it"""

    def __init__(self):
        pass

    def load_data(self, data):
        """OOo style: load Data"""
        self.nodes = data["nodes"]
        self.directed = data["oriented"]
        self.edges = {}

        for start in data["nodes"]:
            self.edges[start] = {}
            for stop in data["nodes"]:
                self.edges[start][stop] = {}

        for edge in data["edges"]:
            self.edges[edge["start"]][edge["stop"]] = edge

    def write_data(self):
        """Build a JSON representation of the graph
        Return JSON datas"""
        data = {"oriented": self.directed, "nodes": self.nodes, "edges": []}

        for start in self.nodes:
            for stop in self.nodes:
                if self.edges[start][stop] != {}:
                    data["edges"].append(self.edges[start][stop])

        return data

    def shortest_path(self, start, stop):
        """Find the shortest path between nodes start and stop
        Returns [start, node1, node2, ..., stop]"""
        return [start, stop]

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
        # Init flow
        for (start, line) in self.edges.iteritems():
            for (stop, edge) in line.iteritems():
                if edge != {}:
                    edge["flow"] = 0

        # Init the loop
        gap = self._gap_graph()
        gap.transitive_closure()

        while gap.edges[start][end] != {}:
            # Shortest path
            path = gap.shortest_path(start, end)

            # Min capacity
            min_capacity = sys.maxint
            for i in range(len(path) - 1):
                capacity = gap.edges[path[i]][path[i + 1]]["capacity"]
                if capacity < min_capacity:
                    min_capacity = capacity

            # Update flow
            for (start, line) in self.edges.iteritems():
                for (stop, edge) in line.iteritems():
                    if edge != {}:
                        if path.count(start) != 0 and path.count(stop) != 0:
                            start_index = path.index(start)
                            stop_index = path.index(stop)
                            if stop_index - start_index == 1:
                                edge["flow"] += min_capacity
                            if stop_index - start_index == -1:
                                edge["flow"] -= min_capacity

            # Update loop
            gap = self._gap_graph()
            gap.transitive_closure()

    def _gap_graph(self):
        """Compute and return the gap graph
        Need self's edges to have a flow value"""

        # New empty gap graph
        gap = Graph()
        gap.directed = True
        gap.nodes = self.nodes
        gap.edges = {}

        for start in gap.nodes:
            gap.edges[start] = {}
            for stop in gap.nodes:
                gap.edges[start][stop] = {}

        # Fill the graph
        for (start, line) in self.edges.iteritems():
            for (stop, edge) in line.iteritems():
                if edge != {}:
                    if edge["flow"] < edge["capacity"]:
                        gap.edges[start][stop]["capacity"] = edge["capacity"] - edge["flow"]
                        gap.edges[start][stop]["cost"] = edge["cost"]
                    if edge["flow"] > 0:
                        gap.edges[stop][start]["capacity"] = edge["flow"]
                        gap.edges[stop][start]["cost"] = -edge["cost"]

        return gap

    def transitive_closure(self):
        """Update the graph to be its transitive closure"""
        for k in self.nodes:
            for i in self.nodes:
                for j in self.nodes:
                    if self.edges[i][k] != {} and self.edges[k][j] != {}:
                        self.edges[i][j]["start"] = i
                        self.edges[i][j]["stop"] = j
                        self.edges[i][j]["capacity"] = 0
                        self.edges[i][j]["cost"] = 0

    def k_coloring(self):
        """Color the graph with n color using the Welsh & Powell algorithm
        Return color number used"""
        working_list = []
        color_count = 0
#        temp_list = []
#        is_neighbour = 0
#        i = 0
        for node in self.nodes:
            working_list.append((node, 0))
            for test_neighbour in self.nodes:
                if self.edges[node][test_neighbour] != {} or self.edges[test_neighbour][node] != {}:
                    working_list[len(working_list)-1] = (working_list[len(working_list)-1][0], working_list[len(working_list)-1][1] + 1)
        working_list = sorted(working_list, key=lambda tup: tup[1])
        working_list.reverse()
        while len(working_list) > 0:
            color_count = color_count + 1
            i = 0
            temp_list = []
            while i < len(working_list):
                node = working_list[i][0]
                is_neighbour = 0
                for j in temp_list:
                    if self.edges[node][j] != {} or self.edges[j][node] != {}:
                        is_neighbour = 1
                if is_neighbour == 1:
                    i = i + 1
                else:
                    self.nodes[node]["color"] = color_count
                    temp_list.append(node)
                    del working_list[i]

        return color_count
