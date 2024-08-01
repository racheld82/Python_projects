LEFT = 0
ROOT = 1
RIGHT = 2


def readDataset(fname):
    with open(fname, "r") as f:
        ds = []
        for line in f:
            s = line.strip().split(",")
            ds.append([float(x) for x in s[:-1]] + [s[-1]])
    return ds


def classes(ds):
    return list(set(row[-1] for row in ds))


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


def majority(ds, classes):
    count = [0] * len(classes)
    for row in ds:
        count[classes.index(row[-1])] += 1
    return classes[count.index(max(count))]


def allTheSameClass(ds):
    cls = ds[0][-1]
    return all(row[-1] == cls for row in ds)


def buildTree(ds, classes, leafSize=1):
    if len(ds) <= leafSize or allTheSameClass(ds):
        return [majority(ds, classes)]

    attr, val = chooseSplit(ds, classes)
    ds_left = [row for row in ds if row[attr] <= val]
    ds_right = [row for row in ds if row[attr] > val]

    if not ds_left or not ds_right:
        return [majority(ds, classes)]

    return [buildTree(ds_left, classes, leafSize), [attr, val], buildTree(ds_right, classes, leafSize)]


def buildClassifier(fname, leafSize=1):
    ds = readDataset(fname)
    cls = classes(ds)
    return buildTree(ds, cls, leafSize)


def classify(dt, instance):
    if len(dt) == 1:
        return dt[0]
    if instance[dt[ROOT][0]] <= dt[ROOT][1]:
        return classify(dt[LEFT], instance)
    return classify(dt[RIGHT], instance)


# Main script
dt = buildClassifier("iris-training.txt", 70)
print(dt)
ds = readDataset("iris-testing.txt")
c = 0
for i in ds:
    if classify(dt, i[:-1]) == i[-1]:
        c += 1
print(c)
