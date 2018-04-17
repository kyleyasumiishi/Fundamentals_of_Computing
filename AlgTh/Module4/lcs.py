"""
Longest common subsequence problem
"""

def lcs(seq_x, seq_y):
    """
    Returns the longest subsequences common to seq_x and seq_y.
    """
    while len(seq_x) > 0 and len(seq_y) > 0:
        if seq_x[-1] == seq_y[-1]:
            return lcs(seq_x[:-1], seq_y[:-1]) + seq_x[-1]
        else:
            return max(lcs(seq_x, seq_y[:-1]), lcs(seq_x[:-1], seq_y))
    return ''

print lcs('gac', 'agcat')