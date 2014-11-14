# -*- coding: utf-8 -*-

import math

__author__ = 'oks'

zoo = []
with open(u'zoo.data.txt', u'r') as f:
    for l in f:
        h = l.strip().split(u',')
        assert len(h) == 18
        zoo.append(h)

# print zoo


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
    return gain, groups

# nodes = []
# for i in xrange(1, 17):
#     nodes.append((i, information_gain(zoo, i)))
# nodes = sorted(nodes, key=lambda x: x[1], reverse=1)
# print nodes

# ----------------- CLASS WORK -------------------- #

attr_names = [
    u'name',
    u'hair',
    u'feathers',
    u'eggs',
    u'milk',
    u'airborne',
    u'aquatic',
    u'predator',
    u'toothed',
    u'backbone',
    u'breathes',
    u'venomous',
    u'fins',
    u'legs',
    u'tail',
    u'domestic',
    u'catsize',
    u'type',
]

label_names = [
    u'?',
    u'mammal',
    u'bird',
    u'reptile',
    u'fish',
    u'amphibian',
    u'insect',
    u'insect',
    u'crustacean',
]


def select_attr(items):
    best_attr = 0
    best_gain = 0.0
    best_groups = {}
    for attr in xrange(1, 17):
        gain, groups = information_gain(items, attr)
        if gain > best_gain:
            best_attr = attr
            best_gain = gain
            best_groups = groups
    return best_attr, best_groups


class Node(object):
    # переопределить __repr__/__str__

    def __init__(self, label, attr=None, children=None):
        self.label = label
        self.attr = attr
        self.children = children

    def guess(self, item):
        if self.label:
            return self.label
        v = item[self.attr]
        if v in self.children:
            return self.children[v].guess(item)
        return u'0'

    def dump(self, level=0):
        """

        :param level: уровень вложенности
        """
        indent = u' ' * level
        if self.label:
            print u'%s -> %s' % (indent, label_names[int(self.label)])
        else:
            print u'%s %s ?' % (indent, attr_names[self.attr])
            for v, t in self.children.iteritems():
                print u'%s %s' % (indent, v)
                t.dump(level + 1)

# list - Node(2)
# not list - Node(None, 3, {...})


def select_label(items):
    # одна ли метка у всех элементов?
    assert len(items)
    label = items[0][17]
    for item in items[1:]:
        if label != item[17]:
            return None
    else:
        return label


def learn(items):
    label = select_label(items)
    if label:
        return Node(label)

    b_attr, b_groups = select_attr(items)
    children = {}
    for k, group in b_groups.iteritems():
        children[k] = learn(group)

    return Node(None, b_attr, children)

tree = learn(zoo[:80])
tree.dump()

for i in zoo[80:]:
    l = tree.guess(i)
    print u'%s %s (%s)' % (i[0], label_names[int(l)], label_names[int(i[17])])

import random


# def random_learn(items):
#     data_divider = random.randint(1, len(items))
#     return data_divider

# --------------- END of CLASS WORK --------------- #

# DECISION TREE - построить дерево и проверить насколько хорошо получилось (данные поделить на две части)
# classes = {}
# from collections import defaultdict
#
#
# def tree():
#     return defaultdict(tree)
#
# dtree = tree()
#
# # [{1: [0, 1]}, {2: u'7'}]
#
#
# def decision_tree(vectors, attr, attrs):
#     es = entropy(vectors)
#
#     if es == 0:
#
#         return
#     else:
#         attrs.pop(0)
#         div_vectors = [v for v in vectors if v[attr] == u'1']
#
#         classes.setdefault(attr, []).append(n_attr)
