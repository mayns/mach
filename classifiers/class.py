# -*- coding: utf-8 -*-

import math

__author__ = 'oks'

zoo = []
with open(u'zoo.data.txt', u'r') as f:
    for l in f:
        h = l.strip().split(u',')
        assert len(h) == 18
        zoo.append(h)

print zoo


def entropy(items):
    labels = {}
    for item in items:
        label = item[17]
        labels.setdefault(label, 0)
        labels[label] += 1
    e = 0.0
    for n in labels.values():
        # probability
        p = float(n) / len(items)
        e += - p * math.log(p)
    return e

# print entropy(zoo)
mammals = [i for i in zoo if i[17] == u'1']
# print mammals
# print entropy(mammals)

# ENTROPY MAX VALUE


def information_gain(items, i):
    groups = {}
    gain = entropy(items)
    for item in items:
        value = item[i]
        groups.setdefault(value, []).append(item)
    for group in groups.values():
        p = float(len(group)) / len(items)
        e = entropy(group)
        gain -= p*e
    return gain

nodes = []
for i in xrange(1, 17):
    nodes.append((i, information_gain(zoo, i)))
nodes = sorted(nodes, key=lambda x: x[1], reverse=1)
print nodes

# DECISION TREE - построить дерево и проверить насколько хорошо получилось (данные поделить на две части)
classes = {}
tree = []
predicates = []


def decision_tree(vectors, i):
    classes[i] = {}
    es = entropy(vectors)
    if es == 0:
        classes[i] = dict(vectors[17])
        tree.append(classes)
        return tree
    else:
