

"""
Calculates the Gini index for a dataset split into two subsets at a specified midpoint.
:param: ds: The dataset, a list of lists where each inner list represents a data point.
:param: classes: A list of unique class labels in the dataset.
:param: mid: The index at which to split the dataset.
:return: The Gini index of the split, a measure of impurity.
"""
def gini(ds, classes, mid):
    n = len(ds)
    left = ds[:mid]
    right = ds[mid:]

    def calculate_gini(subset):
        size = len(subset)
        if size == 0:
            return 0
        score = 0.0
        for c in classes:
            proportion = [row[-1] for row in subset].count(c) / size
            score += proportion ** 2
        return 1 - score

    gini_left = calculate_gini(left)
    gini_right = calculate_gini(right)

    gini_total = (len(left) / n) * gini_left + (len(right) / n) * gini_right
    return gini_total


"""
Finds the best attribute and value to split the dataset to minimize the Gini index.:param: 
:param: ds: The dataset, a list of lists where each inner list represents a data point.
:param: classes: A list of unique class labels in the dataset.
:return: A list containing the index of the best attribute to split on and the value at which to split.
"""
def chooseSplit(ds, classes):
    best_gini = float('inf')
    best_split = [0, ds[0][0]]
    for index in range(len(ds[0]) - 1):
        ds.sort(key=lambda x: x[index])
        for mid in range(1, len(ds)):
            gini_index = gini(ds, classes, mid)
            if gini_index < best_gini:
                best_gini = gini_index
                best_split = [index, (ds[mid - 1][index] + ds[mid][index]) / 2]
    return best_split



"""
Recursively builds a decision tree from the dataset.:param: 
:param: ds: The dataset, a list of lists where each inner list represents a data point.
:param: classes: A list of unique class labels in the dataset.
:param: leafSize: The minimum number of data points required to form a leaf node.
:return: A nested list representing the decision tree. Leaf nodes contain the majority class of the subset, 
         and internal nodes contain the attribute index and split value.
"""
def buildTree(ds, classes, leafSize=1):
    if len(ds) <= leafSize or allTheSameClass(ds):
        return [majority(ds, classes)]

    attr, val = chooseSplit(ds, classes)
    ds_left = [row for row in ds if row[attr] <= val]
    ds_right = [row for row in ds if row[attr] > val]

    if not ds_left or not ds_right:
        return [majority(ds, classes)]

    return [buildTree(ds_left, classes, leafSize), [attr, val], buildTree(ds_right, classes, leafSize)]