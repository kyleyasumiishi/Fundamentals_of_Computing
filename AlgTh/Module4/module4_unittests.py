"""
Unit Tests for Project 4 and Application 4.

By: Kyle Yasumiishi
Last Updated: 3/13/2018
"""

import unittest
import project4

class TestSuite(unittest.TestCase):
    """
    Test cases
    """

    def test_build_scoring_matrix(self):
        scores_0 = project4.build_scoring_matrix(set(['a','b','c']), 10, 4, -1)
        self.assertEqual(sorted(scores_0.keys()), ['-','a','b','c'])
        self.assertEqual(scores_0['a']['a'], 10)
        self.assertEqual(scores_0['a']['b'], 4)
        self.assertEqual(scores_0['a']['-'], -1) 
        scores_1 = project4.build_scoring_matrix(set(['a','b','c','-']), 10, 4, -1)
        self.assertEqual(sorted(scores_1.keys()), ['-','a','b','c'])
        self.assertEqual(scores_1['a']['a'], 10)
        self.assertEqual(scores_1['a']['b'], 4)
        self.assertEqual(scores_1['a']['-'], -1) 

    def test_compute_alignment_matrix(self):
        scoring_matrix_0 = project4.build_scoring_matrix(set(['a','b','c']), 10, 5, -1)
        alignment_0 = project4.compute_alignment_matrix('a', 'cab', scoring_matrix_0, global_flag=True)
        alignment_1 = project4.compute_alignment_matrix('a', 'cab', scoring_matrix_0, global_flag=False)
        self.assertEqual(alignment_0, [[0, -1, -2, -3], [-1, 5, 9, 8]])
        self.assertEqual(alignment_1, [[0, 0, 0, 0], [0, 5, 10, 9]])
        scoring_matrix_1 = project4.build_scoring_matrix(set(['a','b','c']), 10, 5, -1)
        alignment_2 = project4.compute_alignment_matrix('cc', 'cab', scoring_matrix_1, global_flag=True)
        alignment_3 = project4.compute_alignment_matrix('cc', 'cab', scoring_matrix_1, global_flag=False)
        self.assertEqual(alignment_2, [[0, -1, -2, -3], [-1, 10, 9, 8], [-2, 9, 15, 14]])
        self.assertEqual(alignment_3, [[0, 0, 0, 0], [0, 10, 9, 8], [0, 10, 15, 14]])


suite = unittest.TestLoader().loadTestsFromTestCase(TestSuite)
unittest.TextTestRunner(verbosity=1).run(suite)