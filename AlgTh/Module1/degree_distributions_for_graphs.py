"""
This program implements functions that compute information 
about the distribution of in-degrees for nodes in graphs.

This is Project #1 of the course titled
"Algorithmic Thinking (Part 1)" offered by 
Rice University through Coursera. This course is
part of the Fundamentals of Computing specialization.

By: Kyle Yasumiishi
Last updated: 2/20/2018
"""

import unittest

# Constants whose values are dictionaries corresponding to graphs

EX_GRAPH0 = {0: set([1,2]),
             1: set([]),
             2: set([])}

EX_GRAPH1 = {0: set([1,4,5]),
             1: set([2,6]),
             2: set([3]),
             3: set([0]),
             4: set([1]),
             5: set([2]),
             6: set([])}

EX_GRAPH2 = {0: set([1,4,5]),
             1: set([2,6]),
             2: set([3,7]),
             3: set([7]),
             4: set([1]),
             5: set([2]),
             6: set([]),
             7: set([3]),
             8: set([1,2]),
             9: set([0,3,4,5,6,7])}

def make_complete_graph(num_nodes):
    """
    Takes the number of nodes num_nodes and returns a
    dictionary corresponding to a complete directed graph
    with the specified number of nodes. A complete graph
    contains all possible edges subject to the restriction
    that self-loops are not allowed.
    """
    
    graph = {}
    
    for node_idx in range(num_nodes):
        edge_heads = set(range(num_nodes))
        edge_heads.remove(node_idx)
        graph[node_idx] = edge_heads

    for node_key in graph.keys():
        assert node_key not in list(graph[node_key]), "Self-loops not allowed."        

    return graph

# Functions for computing degree distributions

def compute_in_degrees(digraph):
    """
    Takes a directed graph digraph (represented as a dictionary)
    and computes the in-degrees for the nodes in the graph. The 
    function should return a dictionary with the same set of
    keys (nodes) as digraph whose corresponding values are the 
    number of edges whose head matches a particular node.
    """

    for node_key in digraph.keys():
        assert node_key not in list(digraph[node_key]), "Self-loops not allowed."        

    in_deg_graph = digraph.fromkeys(digraph, 0)

    for node_key in digraph.keys():
        for edge_head in list(digraph[node_key]):
            if edge_head != node_key:
                in_deg_graph[edge_head] += 1 

    return in_deg_graph

def in_degree_distribution(digraph):
    """
    Takes a directed graph digraph (represented as a dictionary)
    and computes the unnormalized distribution of the in-degrees of
    the graph. The function should return a dictionary whose keys
    correspond to in-degrees of nodes in the graph. The value associated
    with each particular in-degree is the number of nodes with that
    in-degree. In-degrees with no corresponding nodes in the graph
    are not included in the dictionary.
    """

    for node_key in digraph.keys():
        assert node_key not in list(digraph[node_key]), "Self-loops not allowed."

    distribution_graph = {}

    # Compute list of in-degrees in digraph.
    in_deg_graph = compute_in_degrees(digraph)
    in_deg_values = sorted(in_deg_graph.values())
    
    # Set in-degrees as keys of distribution_graph.
    for in_deg in list(set(in_deg_values)):
        distribution_graph[in_deg] = 0

    # Set each key value in distribution_graph as number of nodes in digraph with that in-degree.
    for in_deg_key in distribution_graph.keys():
        distribution_graph[in_deg_key] = in_deg_values.count(in_deg_key)

    return distribution_graph 

###########################################################################

class TestSuite(unittest.TestCase):
    """
    Testcases 
    """

    # Testcases for make_complete_graph function
    def test_make_complete_graph_0(self):
        self.assertEqual(make_complete_graph(0), {}, msg="Digraph with zero nodes should return empty dictionary")

    def test_make_complete_graph_1(self):
        self.assertEqual(make_complete_graph(1), {0: set([])}, 
        msg="Digraph with one node should return dictionary with one key, zero, corresponding to an empty set.")

    def test_make_complete_graph_2(self):
        self.assertEqual(make_complete_graph(2), {0: set([1]), 1: set([0])}, msg="Digraph with two nodes")

    def test_make_complete_graph_3(self):
        self.assertEqual(make_complete_graph(3), {0: set([1,2]), 1: set([0,2]), 2: set([0,1])}, msg="Digraph with three nodes")

    def test_make_complete_graph_4(self):
        self.assertEqual(make_complete_graph(4), {0: set([1,2,3]), 1: set([0,2,3]), 2: set([0,1,3]), 3: set([0,1,2])},
                         msg="Digraph with four nodes")

    # Testcases for compute_in_degrees
    def test_compute_in_degrees_0(self):
        self.assertEqual(compute_in_degrees(EX_GRAPH0), {0: 0, 1: 1, 2: 1})
    
    def test_compute_in_degrees_1(self):
        self.assertEqual(compute_in_degrees(EX_GRAPH1), {0: 1, 1: 2, 2: 2, 3: 1, 4: 1, 5: 1, 6: 1})        

    def test_compute_in_degrees_2(self):
        self.assertEqual(compute_in_degrees(EX_GRAPH2), {0: 1, 1: 3, 2: 3, 3: 3, 4: 2, 5: 2, 6: 2, 7: 3, 8: 0, 9: 0})

    # Testcases for in_degree_distribution

    def test_in_degree_distribution_0(self):
        self.assertEqual(in_degree_distribution(EX_GRAPH0), {0: 1, 1: 2})

    def test_in_degree_distribution_1(self):
        self.assertEqual(in_degree_distribution(EX_GRAPH1), {1: 5, 2: 2})

    def test_in_degree_distribution_2(self):
        self.assertEqual(in_degree_distribution(EX_GRAPH2), {0: 2, 1: 1, 2: 3, 3: 4})

###########################################################################

# suite = unittest.TestLoader().loadTestsFromTestCase(TestSuite)
# unittest.TextTestRunner(verbosity=2).run(suite)    
