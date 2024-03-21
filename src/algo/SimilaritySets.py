def similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return 100 * (intersection / union if union != 0 else 0)
