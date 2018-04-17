"""
Application 3

This program analyzes the performance of hierarchical clustering and
k-means clustering on various subsets of the county-level cancer risk 
data set from Project 3.

By: Kyle Yasumiishi
Last Updated: 3/9/2018
"""

########################################################################################

# Imports

import random
import project3 as project
import alg_cluster
import time
import matplotlib.pyplot as plt
import urllib2
from copy import deepcopy

########################################################################################

# Provided Code

DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"

def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = urllib2.urlopen(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    print "Loaded", len(data_lines), "data points"
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]

########################################################################################

# Helper Functions

def timer(a_func, arg):
    """
    Returns the running time of function a_func in seconds
    """
    start = time.time()
    a_func(arg)
    end = time.time()
    return end - start

def gen_random_clusters(num_clusters):
    """
    Returns a list of clusters that correspond to one
    randomly generated point in the square with corners
    (+-1, +-1).
    """
    random_clusters = []
    for dummy_idx in range(num_clusters):
        horiz = float(random.randrange(-1000, 1000)) / 1000
        vert = float(random.randrange(-1000, 1000)) / 1000
        random_clusters.append(alg_cluster.Cluster(set(), horiz, vert, 0, 0))
    return random_clusters

def compute_distortion(cluster_list, data_table):
    """
    Takes a list of clusters cluster_list and uses cluster_error function
    to compute its distortion.

    Given a list of clusters, the distortion of the clustering is the sum of
    the errors associated with its clusters.
    """
    distortion = 0.0
    for cluster in cluster_list:
        distortion += cluster.cluster_error(data_table)
    return distortion

def gen_cluster_list(data_table, clustering_type, num_clusters, num_iterations=None):
    """
    Generates and returns a list of clusters from a data table 
    using the given clustering type (i.e., hierarchical or kmeans),
    number of desired clusters num_clusters, and number of iterations num_iterations
    for k-means clustering.
    """
    # Create list of clusters from data_table.
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    # Computes hierarchical or kmeans clustering.
    if clustering_type == "hierarchical":
        cluster_list = project.hierarchical_clustering(singleton_list, num_clusters)
    elif clustering_type == "kmeans":
        cluster_list = project.kmeans_clustering(singleton_list, num_clusters, num_iterations)	
    return cluster_list

def gen_all_distortions(data_table, cluster_list, clustering_type, min_size, max_size):
    """
    Returns a list of the distortions of cluster_list for 
    cluster outputs of min_size to max_size.
    
    data_table: either a 111, 290, or 896 county data set
    cluster_list = a list of 20 clusters
    clustering_type: either "hierarchical" or "kmeans"
    min_size: the minimum number of desired cluster outputs
    max_size: the maximum number of desired cluster outputs
    """
    all_distortions = []
    for size in range(min_size, max_size + 1):
        # Create deepcopy of clustering_list since hierarchical clustering mutates its cluster_list input.
        copy_list = deepcopy(cluster_list)
        assert (copy_list[x].fips_codes() == cluster_list[x].fips_codes() for x in range(len(cluster_list))), "copy_list != cluster_list"
        # Compute hierarchical or kmeans clustering.
        if clustering_type == "hierarchical":
            clustering = project.hierarchical_clustering(copy_list, size)
            assert (clustering[x].fips_codes() == copy_list[x].fips_codes() for x in range(len(clustering))), "clustering != copy_list"
        elif clustering_type == "kmeans":
            clustering = project.kmeans_clustering(copy_list, size, 5)
        # Compute distortion and append to all_distortions list.
        distortion = compute_distortion(clustering, data_table)
        all_distortions.append(distortion)
    return all_distortions 

########################################################################################

# Application Questions

def question1():
    """
    Computes the running times of the functions slow_closest_pair and fast_closest_pair
    for lists of clusters of size 2 to 200 and plots the results.
    """
    # Compute running times.
    slow_running_times = []
    fast_running_times = []
    for cluster_size in range(2, 201):
        random_clusters = gen_random_clusters(cluster_size)
        slow_running_times.append(timer(project.slow_closest_pair, random_clusters))
        fast_running_times.append(timer(project.fast_closest_pair, random_clusters))

    # Plot results.
    xvals = range(2, 201)
    plt.plot(xvals, slow_running_times, '-r', label='slow')
    plt.plot(xvals, fast_running_times, '-g', label='fast')
    plt.xlabel("Number of Initial Clusters")
    plt.ylabel("Running Time (Seconds)")
    plt.title("Running Time Analysis: slow_closest_pair vs. fast_closest_pair (Desktop Python)")
    plt.legend(loc="upper right")
    plt.show()

def question7():
    """
    Use compute_distortion to compute distortions of the two clusterings
    in questions 5 and 6.
    """
    data_table = load_data_table(DATA_111_URL)
    # Question 5 clustering
    hier_cluster = gen_cluster_list(data_table, "hierarchical", 9)
    # Question 6 clustering 
    k_cluster = gen_cluster_list(data_table, "kmeans", 9, 5)
    # Compute distortions for hierarchical and kmeans clustering.
    hier_distortion = compute_distortion(hier_cluster, data_table)
    k_distortion = compute_distortion(k_cluster, data_table)
    print "hierarchical distortion:", hier_distortion
    print "kmeans distortion:", k_distortion

def question10():
    """
    This function:
    1) Computes the distortion of the list of clusters produced by
    hierarchical clustering and k-means clustering (using 5 iterations)
    on the 111, 290, and 896 county data sets, respectively, where the
    number of output clusters ranges from 6 to 20 (inclusive).
    2) Creates three plots (one for each data set) that compare the 
    distortion of the clusterings produced by both methods.
    """
    data = [load_data_table(DATA_111_URL), load_data_table(DATA_290_URL), load_data_table(DATA_896_URL)]
    h_distortion = []
    k_distortion = []

    # Compute distortions for hierarchical and kmeans clusterings. 
    for idx in range(len(data)):
        h_cluster = gen_cluster_list(data[idx], "hierarchical", 20)
        k_cluster = gen_cluster_list(data[idx], "kmeans", 20, 5)
        h_distortion.append(gen_all_distortions(data[idx], h_cluster, "hierarchical", 6, 20))
        k_distortion.append(gen_all_distortions(data[idx], k_cluster, "kmeans", 6, 20))

    # Create closure function for plotting distortions.
    def plot(data_idx):
        num_counties = len(data[data_idx])
        xvals = range(6, 21)
        plt.plot(xvals, k_distortion[data_idx], '-r', label='kmeans')
        plt.plot(xvals, h_distortion[data_idx], '-g', label='hierarchical')
        plt.xlabel("Number of Clusters")
        plt.ylabel("Distortion (10^12)")
        plt.title("Distortion on Data Set of " + str(num_counties) + " Points (Desktop Python)")
        plt.legend(loc="upper right")
        plt.show()
    
    # Plot results.
    plot(0)
    plot(1)
    plot(2)

########################################################################################

# question1()
# question7()
# question10()