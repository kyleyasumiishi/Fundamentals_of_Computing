"""
This program analyzes the structure of graphs generated
by citation patterns from scientific papers. 

Specifically, it helps answer the five questions of 
Application #1 of the course titled "Algorithmic Thinking (Part 1)"
offered by Rice University through Coursera. This course is
part of the Fundamentals of Computing specialization.

By: Kyle Yasumiishi
Last updated: 2/23/2018
"""

import unittest
import urllib2
import matplotlib.pyplot as plt
import math
import random
import degree_distributions_for_graphs as project

################### Provided code ######################

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

class DPATrial:
    """
    Simple class to encapsulate optimized trials for DPA algorithm
    
    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a DPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_node trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors

# CONSTANTS

CITATION_GRAPH = load_graph(CITATION_URL)

################### My code ######################

def question1(citation_graph):
    """
    This function:
    1) Computes the in-degree distribution for citation_graph.
    2) Normalizes the in-degree distribution.
    3) Prints a log/log plot of the points in the normalized distribution.
    """
    in_deg_dist = project.in_degree_distribution(citation_graph)
    total_nodes = float(sum(in_deg_dist.values()))
    x_vals = in_deg_dist.keys()
    y_vals = [y / total_nodes for y in in_deg_dist.values()]
    plt.loglog(x_vals, y_vals, 'ro')
    plt.title("Question 1: Log/Log Plot of Distribution of Citations")
    plt.xlabel("Number of Citations")
    plt.ylabel("Normalized Distribution of Papers")
    plt.axis([10**0,10**4,10**-5,10**0])
    plt.show()

def question3(citation_graph):
    """
    This function prints the number of nodes and 
    average out-degree of the citation_graph.
    """
    num_nodes = len(citation_graph)
    num_values = float(sum(len(val) for val in citation_graph.values()))
    avg_out_deg = num_values / num_nodes
    print "Number of nodes:", num_nodes
    print "Number of values:", num_values
    print "Average out-degree:", avg_out_deg, "or", math.ceil(avg_out_deg)

def num_nodes_and_edges(graph_url):
    """
    This function prints the combined total number of nodes and edges.
    Used to compare with output of question3 function.
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
 
    num_items = 0
    for line in graph_lines:
        wordlist = line.split()
        num_items += len(wordlist)
    print num_items

def question4(num_final_nodes,num_existing_nodes):
    """
    This function:
    1) Implements DPA algorithm.
    2) Computes DPA graph using the final number of nodes, num_final_nodes,
    and a fixed number of existing nodes to which a new node is connected
    during each iteration, num_existing_nodes.
    3) Plots the in-degree distribution for the DPA graph.
    """

    # Make a complete graph on num_existing_nodes
    graph = project.make_complete_graph(num_existing_nodes)
    
    # Implement DPA algorithm and computes DPA graph
    DPATrial_graph = DPATrial(num_existing_nodes)
    for node in range(num_existing_nodes, num_final_nodes):
        graph[node] = DPATrial_graph.run_trial(num_existing_nodes)

    # Computes in-degree distribution of graph, normalizes it, and prints plot
    in_deg_dist = project.in_degree_distribution(graph)
    total_nodes = float(sum(in_deg_dist.values()))
    x_vals = in_deg_dist.keys()
    y_vals = [y / total_nodes for y in in_deg_dist.values()]
    plt.loglog(x_vals, y_vals, 'go')
    plt.title("Question 4: Log/Log Plot of DPA Graph's In-Degree Distribution")
    plt.xlabel("In Degree (Log)")
    plt.ylabel("Normalized Distribution of Nodes (Log)")
    plt.show()

    
    

################### Calls to functions ######################

question1(CITATION_GRAPH)
question3(CITATION_GRAPH)
# num_nodes_and_edges(CITATION_URL)
question4(27770,13)










