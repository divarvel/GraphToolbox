#!/usr/bin/env python
#-*- encoding: utf-8 -*-
#

import sys, os, json, Graph
from optparse import OptionParser


class GraphToolbox(object):
    """Implement some well known graph-related algos"""
    def __init__(self):
        " Parse the commands provided by the user"

        parser = OptionParser()
        parser.add_option("-f", "--file", dest="filename",
                                            help="use the graph stored in FILE",
                          metavar="FILE")

        parser.add_option("-a", "--action", dest="action",
                                            help="action to perform on the graph")

        (options, args) = parser.parse_args()

        self._load_graph(options['filename'])

    def _load_graph(self, path):
        " Create a new graph from the input file "
        graph = new Graph()
        with(fp = open(path)):
            graph.loadData(json.load(fp))

        return graph

if __name__ == '__main__':
    main = new GraphToolbox()
