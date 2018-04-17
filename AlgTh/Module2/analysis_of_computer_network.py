"""
Graph exploration (that is, "visiting" the nodes and edges of a
graph) is a powerful and necessary tool to elucidate properties of
graphs and quantify statistics on them. For example, by exploring a
graph, we can compute its degree distribution, pairwise distances 
among nodes, its connected components, and centrality measures 
of its nodes and edges. As we saw in the Homework and Project, 
breadth-first search can be used to compute the connected 
components of a graph.

In this Application, we will analyze the connectivity of a computer
network as it undergoes a cyber-attack. In particular, we will
simulate an attack on this network in which an increasing number
of servers are disabled. In computational terms, we will model the
network by an undirected graph and repeatedly delete nodes from
this graph. We will then measure the resilience of the graph in 
terms of the size of the largest remaining connected component as
a function of the number of nodes deleted.

By: Kyle Yasumiishi
Last Updated: 3/5/2018
"""

#################################################################################

# Imports

from itertools import combinations
import random
import unittest
import provided_code as provided
import degree_distributions_for_graphs as project1
import cc_and_graph_resilience as project2
import matplotlib.pyplot as plt
import time
import gc

#################################################################################

# Graphs

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"

def make_computer_network_graph():
    """
    Loads the text representation for the example network as an 
    undirected graph (with 1239 nodes and 3047 edges).
    """
    return provided.load_graph(NETWORK_URL)

def make_ER_graph(num_nodes, probability):
    """
    Takes the number of nodes num_nodes and probability
    and returns a dictionary corresponding to a 
    randomly generated undirected graph with the 
    specified number of nodes. Self-loops are not allowed.
    """
    graph = {}
    nodes = set(list(range(num_nodes)))
    for node in nodes:
        graph[node] = set([])
    for (nodei, nodej) in combinations(nodes, 2):
        if nodei != nodej:
            random_decimal = float(random.randrange(0, 1000)) / 1000
            if random_decimal < probability:
                graph[nodei].add(nodej)
                graph[nodej].add(nodei)
    for node in graph.keys():
        assert node not in list(graph[node]), "Self-loops not allowed"
    return graph

def make_UPA_graph(num_final_nodes, num_existing_nodes):
    """
    This function:
    1) Implements UPA algorithm.
    2) Computes UPA graph using the final number of nodes, num_final_nodes,
    and a fixed number of existing nodes to which a new node is connected
    during each iteration, num_existing_nodes.
    """
    # Make a complete graph on num_existing_nodes
    graph = project1.make_complete_graph(num_existing_nodes)
    # Implement UPA algorithm 
    UPATrial_graph = provided.UPATrial(num_existing_nodes)
    for node in range(num_existing_nodes, num_final_nodes):
        graph[node] = UPATrial_graph.run_trial(num_existing_nodes)
        for edge in graph[node]:
            graph[edge].add(node)
    return graph

#################################################################################

# Helper functions

def get_num_edges(ugraph):
    """
    Returns the number of edges in an undirected graph ugraph. 
    Considers each edge in the undirected graph once, not twice.
    """
    value_list = []
    sets_of_values = ugraph.values()
    for val_set in sets_of_values:
        for val in val_set:
            value_list.append(val)
    return (len(value_list)) / 2

def random_order(graph):
    """
    Takes a graph and returns a list of nodes in the graph in some random order.
    """
    keys = graph.keys()
    random.shuffle(keys)
    return keys

def get_degree_sets(graph):
    """
    Creates a list whose kth element is the set of nodes 
    of degree k. Determines degree for each node in graph
    and adds node to its respective set in the list.
    """
    num_nodes = len(graph.keys())
    degree_sets = [set([]) for dummy in range(num_nodes)]
    for node in graph:
        deg = len(graph[node])
        degree_sets[deg].add(node)
    return degree_sets

def fast_targeted_order(graph):
    """
    Returns a list of the nodes in graph in decreasing order of their degrees.
    """
    # copy the graph
    new_graph = provided.copy_graph(graph)

    num_nodes = len(new_graph.keys())
    degree_sets = get_degree_sets(graph)
    order = []
    
    # Iterates through the list degree_sets in order of
    # decreasing degree. When this method encounters a
    # non-empty set, the nodes in this set must be of 
    # maximum degree. This method then repeatedly chooses
    # an arbitrary node, arb_node, from this set, 
    # deletes arb_node from the graph, and updates degree_sets appropriately.
    for node in range((num_nodes - 1), -1, -1):
        while len(degree_sets[node]) > 0:
            arb_node = degree_sets[node].pop()
            for neighbor in new_graph[arb_node]:
                deg = len(new_graph[neighbor])
                degree_sets[deg].remove(neighbor)
                degree_sets[deg - 1].add(neighbor)
            order.append(arb_node)
            provided.delete_node(new_graph, arb_node)

    return order

def timer(a_func, arg):
    """
    Returns the running time of function a_func in seconds.
    """
    start = time.time()
    a_func(arg)
    end = time.time()
    return end - start

#################################################################################

# Application Questions

def question1():
    """
    In question 1, we will examine the resilience of the computer network
    under an attack in which servers are chosen at random. We will then compare
    the resilience of the network to the resilience of ER and UPA graphs of
    similar size.
    """
    # Determine the probability such that the ER graph has approx. the same
    # number of edges as the computer network. Likewise, compute an integer such 
    # that the number of edges in the UPA graph is close to the number of edges
    # in the computer network. Each graph should have the same number of nodes, 1239.
    ER_prob =  .004
    UPA_num_existing_nodes = 3
    
    ER_graph = make_ER_graph(1239, ER_prob)
    UPA_graph = make_UPA_graph(1239, UPA_num_existing_nodes)
    network_graph = make_computer_network_graph()

    # Compute random attack order for each graph.
    ER_random = random_order(ER_graph)
    UPA_random = random_order(UPA_graph)
    network_random = random_order(network_graph)

    # Compute the resilience of each graph.
    ER_resilience = project2.compute_resilience(ER_graph, ER_random)
    UPA_resilience = project2.compute_resilience(UPA_graph, UPA_random)
    network_resilience = project2.compute_resilience(network_graph, network_random)

    # Plot the results
    xvals = range(len(network_resilience))
    ER_yvals = ER_resilience
    UPA_yvals = UPA_resilience
    network_yvals = network_resilience

    plt.title("Question 1: Resilience of Computer Network, ER Graph, and UPA Graph")
    plt.xlabel("Number of Nodes Removed")
    plt.ylabel("Size of Largest Connected Component")

    plt.plot(xvals, ER_yvals, '-b', label='ER Graph (p=.004)')
    plt.plot(xvals, UPA_yvals, '-r', label='UPA Graph (m=3)')
    plt.plot(xvals, network_yvals, '-g', label='Computer Network')
    plt.grid(which='major', axis='both')
    plt.legend(loc='upper right')
    plt.show()

def question3():
    """
    Analyze the running time of targeted_order and fast_targeted_order on 
    UPA graphs of size n with m = 5. Uses the time module to compute the 
    running times of these functions. Plots these running times (vertical axis)
    as a function of the number of nodes n (horizontal axis) using a standard
    plot.
    """
    # Calculate the running times of targeted_order and fast_targeted_order.
    targeted_order_running_times = []
    fast_targeted_order_running_times = []
    for num_final_nodes in range(10, 1000, 10):
        UPA_graph = make_UPA_graph(num_final_nodes, 5)
        targeted_order_running_times.append(timer(provided.targeted_order, UPA_graph))
        fast_targeted_order_running_times.append(timer(fast_targeted_order, UPA_graph))

    # Plot the results.
    xvals = range(10, 1000, 10)
    targeted_yvals = targeted_order_running_times
    fast_targeted_yvals = fast_targeted_order_running_times

    plt.title("Running Times of Targeted Order Vs. Fast Targeted Order (Desktop Python 2.7)")
    plt.xlabel("Number of Nodes n")
    plt.ylabel("Running Time (seconds)")

    plt.plot(xvals, targeted_yvals, '-b', label='targeted_order')
    plt.plot(xvals, fast_targeted_yvals, '-r', label='fast_targeted_order')
    plt.grid(which='major', axis='both')
    plt.legend(loc='upper right')
    plt.show()

def question4():
    """
    This function:
    1) Uses fast_targeted_order to compute a targeted attack order for 
    each of the three graphs (computer network, ER, UPA) from Question 1.
    2) Uses compute_resilience to compute the resilience of each graph.
    3) Plots the computed resiliences as three curves in a single standard plot.
    """
    # Three graphs. The probability argument (.004) for make_ER_graph and 
    # num_existing_nodes argument (3) for make_UPA_graph are same as in question1. 
    network_graph = make_computer_network_graph()
    ER_graph = make_ER_graph(1239, .004)
    UPA_graph = make_UPA_graph(1239, 3)

    # Computes a targeted attack order for each of the three graphs.
    network_order = fast_targeted_order(network_graph)
    ER_order = fast_targeted_order(ER_graph)
    UPA_order = fast_targeted_order(UPA_graph)

    # Computes graph resilience for each of the three graphs.
    network_resilience = project2.compute_resilience(network_graph, network_order) 
    ER_resilience = project2.compute_resilience(ER_graph, ER_order)
    UPA_resilience = project2.compute_resilience(UPA_graph, UPA_order)

    # Plot the computed resiliences.
    xvals = range(len(network_resilience))
    ER_yvals = ER_resilience
    UPA_yvals = UPA_resilience
    network_yvals = network_resilience

    plt.title("Question 4: Graph and Network Resilience Under Connectivity-Based Attack")
    plt.xlabel("Number of Nodes Removed")
    plt.ylabel("Size of Largest Connected Component")

    plt.plot(xvals, ER_yvals, '-b', label='ER Graph (p=.004)')
    plt.plot(xvals, UPA_yvals, '-r', label='UPA Graph (m=3)')
    plt.plot(xvals, network_yvals, '-g', label='Computer Network')
    plt.grid(which='major', axis='both')
    plt.legend(loc='upper right')
    plt.show()

#################################################################################

# Unit Tests

m2_graph0 = {0: set([1]), 1: set([0]), 2: set([])}
m2_graph1 = {0: set([1,2,3]), 1: set([0,4,5]), 2: set([0]), 3: set([0]),
             4: set([1,6]), 5: set([1]), 6: set([4])}

class TestSuite(unittest.TestCase):
    """
    Testcases
    """

    def test_make_ER_graph(self):
        ER_graph1 = make_ER_graph(10, 0)
        ER_graph1_values = []
        for val in ER_graph1.values():
            ER_graph1_values.append(val)

        ER_graph2 = make_ER_graph(10, 1)
        ER_graph2_values = []
        for val in ER_graph2.values():
            ER_graph2_values.append(val)

        self.assertEqual(ER_graph1_values.count(set([])), 10)
        self.assertEqual(ER_graph2_values.count(set([])), 0)

    def test_get_degree_sets(self):
        m2_graph0_local = {0: set([1]), 1: set([0]), 2: set([])}
        m2_graph1_local = {0: set([1,2,3]), 1: set([0,4,5]), 2: set([0]), 3: set([0]),
                     4: set([1,6]), 5: set([1]), 6: set([4])}
        self.assertEqual(get_degree_sets(m2_graph0_local), [set([2]), set([0, 1]), set([])])
        self.assertEqual(get_degree_sets(m2_graph1_local), [set([]), set([2,3,5,6]), set([4]), set([0,1]), 
                                                            set([]), set([]), set([])])

    def test_fast_targeted_order(self):
        self.assertEqual(fast_targeted_order(m2_graph0), provided.targeted_order(m2_graph0))
        self.assertEqual(fast_targeted_order(m2_graph1), provided.targeted_order(m2_graph1))

# suite = unittest.TestLoader().loadTestsFromTestCase(TestSuite)
# unittest.TextTestRunner(verbosity=0).run(suite)

#################################################################################

# Calls to Functions

# question1()
# gc.disable()
# question3()
# gc.enable()
# question4()
