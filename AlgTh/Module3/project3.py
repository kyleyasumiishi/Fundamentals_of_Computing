"""
Student template code for Project 3
Student will implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane

By: Kyle Yasumiishi
Last Updated: 3/8/2018
"""

import math
# import alg_clusters_matplotlib
import alg_cluster


######################################################
# Code for closest pairs of clusters

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters
    
    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))

def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    # Set minimum distance min_dist to infinity.
    min_dist = (float("inf"), -1, -1)

    # Compute distance between every cluster to find pair with smallest distance.
    for idx1 in range(len(cluster_list)):
        for idx2 in range(len(cluster_list)):
            if cluster_list[idx1] != cluster_list[idx2]:
                dist = pair_distance(cluster_list, idx1, idx2)
                if dist[0] < min_dist[0]:
                    min_dist = dist
    
    return min_dist

def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    # Set minimum distance min_dist to infinity.
    min_dist = (float("inf"), -1, -1)

    num_clusters = len(cluster_list)

    # Base case
    if num_clusters <= 3:
        min_dist = slow_closest_pair(cluster_list)
    # Recursive case
    else:
        # Divide.
        mid = int(math.floor(num_clusters / 2))
        left_clusters = cluster_list[: mid]
        right_clusters = cluster_list[mid :]
        # Conquer.
        closest_left = fast_closest_pair(left_clusters) 
        closest_right = fast_closest_pair(right_clusters)
        left1 = cluster_list.index(left_clusters[closest_left[1]])
        left2 = cluster_list.index(left_clusters[closest_left[2]])
        right1 = cluster_list.index(right_clusters[closest_right[1]])
        right2 = cluster_list.index(right_clusters[closest_right[2]])
        # Merge.
        if closest_left[0] < closest_right[0]:
            min_dist = (closest_left[0], left1, left2)
        else:
            min_dist = (closest_right[0], right1, right2)
        # Check if the two closest clusters reside on either side of mid.
        mid_l = cluster_list[mid - 1].horiz_center()
        mid_r = cluster_list[mid].horiz_center()
        horiz_center = .5 * (mid_l + mid_r)
        min_dist = min(min_dist, closest_pair_strip(cluster_list, horiz_center, min_dist[0]))
    
    return min_dist

def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.       
    """
    # Create list of clusters in vertical strip.
    strip_clusters = [cluster for cluster in cluster_list if abs(cluster.horiz_center() - horiz_center) < half_width]
    
    # Sort clusters by vertical position.
    strip_clusters.sort(key = lambda cluster: cluster.vert_center())

    # Set minimum distance min_dist to infinity.
    min_dist = (float("inf"), -1, -1)

    num_clusters = len(strip_clusters)

    # For each cluster, inspect the next three to find the closest. 
    for idx_u in range(num_clusters - 2 + 1):
        for idx_v in range(idx_u + 1, min(idx_u + 4, num_clusters)):
            dist = pair_distance(strip_clusters, idx_u, idx_v)
            if dist[0] < min_dist[0]:
                idx1 = cluster_list.index(strip_clusters[idx_u])
                idx2 = cluster_list.index(strip_clusters[idx_v])
                min_dist = pair_distance(cluster_list, idx1, idx2)

    return min_dist
            
######################################################################
# Code for hierarchical clustering

def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    while len(cluster_list) > num_clusters:
        # Sort clusters by horizontal position.
        cluster_list.sort(key = lambda cluster: cluster.horiz_center())
        # Find closest pair of clusters.
        closest_pair = fast_closest_pair(cluster_list)
        cluster1 = cluster_list[closest_pair[1]]
        cluster2 = cluster_list.pop(closest_pair[2])
        # Merge clusters.
        cluster1.merge_clusters(cluster2)

    return cluster_list

######################################################################
# Code for k-means clustering

    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """
    # Create copy of cluster_list, sorted in descending order of clusters' populations.
    sorted_cluster_list = sorted(cluster_list, key = lambda cluster: cluster.total_population(), reverse = True)        

    # Position initial clusters at the location of clusters with largest populations.
    centers = [alg_cluster.Cluster(set(), cluster.horiz_center(), cluster.vert_center(), 0, 0) 
               for cluster in sorted_cluster_list[:num_clusters]]

    for dummy_idx in range(num_iterations):
        # Initialize num_clusters empty clusters.
        k_clusters = [alg_cluster.Cluster(set(), 0, 0, 0, 0) for dummy_idx in range(num_clusters)]
        # For every cluster, merge cluster into the closest k_cluster.
        for cluster in cluster_list:
            min_dist = float('inf')
            for center in centers:
                if cluster.distance(center) < min_dist:
                    min_dist = cluster.distance(center)
                    closest = centers.index(center)
            k_clusters[closest].merge_clusters(cluster)
        # Update centers.
        centers = [alg_cluster.Cluster(set(), cluster.horiz_center(), cluster.vert_center(), 0, 0) 
                   for cluster in k_clusters]

    return k_clusters


