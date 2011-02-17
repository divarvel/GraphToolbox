#!/usr/bin/env python
#-*- encoding: utf-8 -*-
#

import sys, json

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

        #Initialization
        T = []
        self.nodes[start]["dynamicCost"] = 0



        for node_id in self.nodes:
            T.append(node_id)
            #self.nodes[node_id]["dynamicPred"]=start
            boolean = 0
            if self.edges[start][node_id] != {} and node_id != start:
                self.nodes[node_id]["dynamicCost"]=self.edges[start][node_id]["cost"]
                boolean = 1
                continue
            if boolean == 0 and node_id != start:
                self.nodes[node_id]["dynamicCost"] = sys.maxint

        #Main Loop
        while len(T) != 0:

            minimum_id = T[0]
            for node_id in T:
                if self.nodes[minimum_id]["dynamicCost"] > self.nodes[node_id]["dynamicCost"]:
                    minimum_id = node_id


            for node_id in self.nodes:
                    if self.edges[minimum_id][node_id] != {} and self.nodes[node_id]["dynamicCost"] >= self.nodes[minimum_id]["dynamicCost"]+self.edges[minimum_id][node_id]["cost"]:
                        self.nodes[node_id]["dynamicCost"] = self.nodes[minimum_id]["dynamicCost"] + self.edges[minimum_id][node_id]["cost"]
                        self.nodes[node_id]["dynamicPred"] = minimum_id
            T.remove(minimum_id)
        #Computation of the result list of nodes, from stop to start
        finalnode_id = stop
        result = []
        try:
            while finalnode_id!=start:
                result.insert(0,finalnode_id)
                finalnode_id = self.nodes[finalnode_id]["dynamicPred"]
            result.insert(0,start)
        except KeyError:
            result=[]
            print("There is no path between " + start + " and " + stop)

        return result



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
        closure = self._gap_graph()
        closure.transitive_closure()

        while closure.edges[start][end] != {}:
            # Shortest path
            path = gap.ford_bellman(start, end)

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
            closure = self._gap_graph()
            closure.transitive_closure()

    def _gap_graph(self):
        """Compute and return the gap graph
        Need self's edges to have a flow value"""

        # New empty gap graph
        gap = Graph()
        gap.directed = True
        gap.nodes = {}
        for node in self.nodes:
            gap.nodes[node] = {}

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
                        gap.edges[start][stop]["start"] = start
                        gap.edges[start][stop]["stop"] = stop
                        gap.edges[start][stop]["capacity"] = edge["capacity"] - edge["flow"]
                        gap.edges[start][stop]["cost"] = edge["cost"]
                    if edge["flow"] > 0:
                        gap.edges[stop][start]["start"] = stop
                        gap.edges[stop][start]["stop"] = start
                        gap.edges[stop][start]["capacity"] = edge["flow"]
                        gap.edges[stop][start]["cost"] = -edge["cost"]

        return gap

    def ford_bellman(self, start, stop):
        """Shortest path with Ford-Bellman algorithm
        Return [start, node1, node2, ..., stop]"""
        # Init
        for (node_name, node) in self.nodes.iteritems():
            node["pred"] = ""
            if node_name == start:
                node["cost"] = 0
            else:
                node["cost"] = sys.maxint

        # Update
        for i in range(len(self.nodes)):
            for (begin, line) in self.edges.iteritems():
                for (end, edge) in line.iteritems():
                    if edge != {}:
                        begin_node = self.nodes[begin]
                        end_node = self.nodes[end]
                        if begin_node["cost"] + edge["cost"] < end_node["cost"]:
                            end_node["cost"] = begin_node["cost"] + edge["cost"]
                            end_node["pred"] = begin

        # Check for negative cycles
        for (begin, line) in self.edges.iteritems():
            for (end, edge) in line.iteritems():
                if edge != {}:
                    begin_node = self.nodes[begin]
                    end_node = self.nodes[end]
                    if begin_node["cost"] + edge["cost"] < end_node["cost"]:
                        return []

        # Retrieve path
        path = [stop]
        while path[0] != start:
            path.insert(0, self.nodes[path[0]]["pred"])

        return path

    def transitive_closure(self):
        """Update the graph to be its transitive closure"""
        for k in self.nodes:
            for i in self.nodes:
                for j in self.nodes:
                    if self.edges[i][k] != {} and self.edges[k][j] != {}:
                        self.edges[i][j]["start"] = i
                        self.edges[i][j]["stop"] = j

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
