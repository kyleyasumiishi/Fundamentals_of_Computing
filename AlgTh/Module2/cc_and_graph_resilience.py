"""
For the Project component of Module 2, you will first write Python
code that implements breadth-first search. Then, you will use this
function to compute the set of connected components (CCs) of an
undirected graph as well as determine the size of its largest
connected component. Finally, you will write a function that
computes the resilience of a graph (measured by the size of its 
largest connected component) as a sequence of nodes are deleted
from the graph.

You will use these functions in the Application component of Module
2 where you will analyze the resilience of a computer network,
modeled by a graph. As in Module 1, graphs will be represented 
using dictionaries.

By: Kyle Yasumiishi
Last Updated: 3/2/2017
"""

import unittest
from collections import deque

# Breadth-first search

def bfs_visited(ugraph, start_node):
    """
    Takes the undirected graph ugraph and the node
    start_node and returns the set consisting of
    all nodes that are visited by a breadth-first search
    that starts at start_node.
    """
    queue = deque()
    visited = set([start_node])
    queue.appendleft(start_node)
    while len(queue) > 0:
        current_node = queue.pop()
        if current_node in ugraph.keys():
            for neighbor in ugraph[current_node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.appendleft(neighbor)
    return visited

# Connected components

def cc_visited(ugraph):
    """
    Takes the undirected graph ugraph and returns
    a list of sets, where each set consists of all 
    the nodes (and nothing else) in a connected component,
    and there is exactly one set in the list for each 
    connected componenent in ugraph and nothing else.
    """
    remaining_nodes = ugraph.keys()
    connected_components = []
    while len(remaining_nodes) > 0:
        for node in remaining_nodes:
            visited_nodes = bfs_visited(ugraph, node)
            connected_components.append(visited_nodes)
            for visited_node in visited_nodes:
                if visited_node in remaining_nodes:
                    remaining_nodes.remove(visited_node)
    return connected_components

def largest_cc_size(ugraph):
    """
    Takes the undirected graph ugraph and returns the
    size (an integer) of the largest connect component
    in ugraph.
    """
    largest_cc = 0
    connected_components = cc_visited(ugraph)
    for connected_component in connected_components:
        if len(connected_component) > largest_cc:
            largest_cc = len(connected_component)
    return largest_cc

# Graph resilience

def compute_resilience(ugraph, attack_order):
    """
    Takes the undirected graph ugraph, a list of
    nodes attack_order and iterates through the nodes
    in attack_order. For each node in the list, the 
    function removes the given node and its edges from
    the graph and then computes the size of the largest
    connected component for the resulting graph.
    The function should return a list whose k + 1th entry
    is the size of the largest connect component in the graph
    after the removal of the first k nodes in attack_order.
    The first entry (indexed by zero) is the size of the largest
    connected component in the original graph. 
    """
    largest_cc_list = []
    largest_cc_list.append(largest_cc_size(ugraph))
    for node in attack_order:
        if node in ugraph:
            # Remove node and edges from graph
            for edge in ugraph[node]:
                ugraph[edge] = set([val for val in ugraph[edge] if val != node])
            del ugraph[node]
            # Appends size of largest cc to largest_cc_list
            largest_cc_list.append(largest_cc_size(ugraph))
    return largest_cc_list

##############################################################

# Example graphs used for testing

UGRAPH_0 = {0: set([1,2,3]),
                    1: set([0,2]),
                    2: set([0,1,3]),
                    3: set([0,2])}

UGRAPH_1 = {0: set([1,2]),
            1: set([0,4]),
            2: set([0]),
            3: set([]),
            4: set([1,5]),
            5: set([4]),
            6: set([])}

GRAPH0 = {0: set([1]),
          1: set([0, 2]),
          2: set([1, 3]),
          3: set([2])}

GRAPH5 = {"dog": set(["cat"]),
          "cat": set(["dog"]),
          "monkey": set(["banana"]),
          "banana": set(["monkey", "ape"]),
          "ape": set(["banana"])}

class TestSuite(unittest.TestCase):
    """
    Testcases
    """

    # Testcases for bfs-visited
    def test_bfs_visited(self): 
        self.assertEqual(bfs_visited(UGRAPH_0, 0), set([0,1,2,3]))
        self.assertEqual(bfs_visited(UGRAPH_1, 0), set([0,1,2,4,5]))
        self.assertEqual(bfs_visited(UGRAPH_1, 3), set([3]))
        self.assertEqual(bfs_visited(UGRAPH_1, 1), set([0,1,2,4,5]))
        self.assertEqual(bfs_visited(GRAPH0, 0), set([0,1,2,3]))
        self.assertEqual(bfs_visited(GRAPH5, "dog"), set(["dog", "cat"]))
        self.assertEqual(bfs_visited(GRAPH5, "banana"), set(["banana", "ape", "monkey"]))

    # Testcases for cc_visited
    def test_cc_visited(self):
        self.assertEqual(cc_visited(GRAPH5), [set(["banana", "ape", "monkey"]), set(["dog", "cat"])])
        self.assertEqual(cc_visited(UGRAPH_1), [set([0,1,2,4,5]), set([6]), set([3])])

    # Testcases for largest_cc_size
    def test_largest_cc_size(self):
        GRAPH5_copy = dict(GRAPH5)
        ugraph_1_copy = dict(UGRAPH_1)
        self.assertEqual(largest_cc_size(GRAPH5_copy), 3)
        self.assertEqual(largest_cc_size(ugraph_1_copy), 5)

    # Testcases for compute_resilience
    def test_compute_resilience(self):
        GRAPH5_copy1, GRAPH5_copy2 = dict(GRAPH5), dict(GRAPH5)
        ugraph_1_copy = dict(UGRAPH_1)
        self.assertEqual(compute_resilience(GRAPH5_copy1, ["cat"]), [3, 3])
        self.assertEqual(compute_resilience(GRAPH5_copy2, ["banana"]), [3, 2])
        self.assertEqual(compute_resilience(ugraph_1_copy, [2, 4]), [5, 4, 2])

#############################################################

# Run tests

suite = unittest.TestLoader().loadTestsFromTestCase(TestSuite)
unittest.TextTestRunner(verbosity=0).run(suite)