#!/usr/bin/python3

import sys

sys.setrecursionlimit(1000000000) # For very big trees

global INF
INF = float('INF')


class intTreeMin:
    '''
    Interval tree that allows query for minimum of given interval.
    '''

    def __init__(self, n, type='int'):
        '''
        Creates new, empty interval tree of specified length.

        :param n: Size of an array on which tree is based.
        :param type: Type of elements in tree. Default type is integer.
        '''
        base = 1
        while base < n:
            base *= 2
        self.tree = []
        for i in range(2 * base):
            self.tree.append([INF, INF])
        self.size = base

    def insert(self, i, n, val=1):
        '''
        Inserts new node to the tree and updates all values in the subtree of
        the new node.

        :param i: Depth of node
        :param n: Index of node
        :param val: Value of node
        '''
        if i < self.size:
            i = self.size + i
            self.tree[i][0] = val
            self.tree[i][1] = n
            while i // 2 != 0:
                i = i // 2
                if self.tree[2 * i][0] < self.tree[2 * i + 1][0]:
                    self.tree[i][0] = self.tree[2 * i][0]
                    self.tree[i][1] = self.tree[2 * i][1]
                else:
                    self.tree[i][0] = self.tree[2 * i + 1][0]
                    self.tree[i][1] = self.tree[2 * i + 1][1]

    def query_min(self, i, j):
        '''
        Returns minimum of interval [i, j] (both ends inclusive) from original
        array. It is used for finding the lowest common ancestor of two nodes.

        :param i: start of the interval (first node in ascending order)
        :param j: end of the interval   (second node in ascending order)
        :return: LCA represented as pair (depth, index of node in original array)

        '''
        i += self.size
        j += self.size
        if self.tree[i][0] < self.tree[j][0]:
            result = self.tree[i][:]
        else:
            result = self.tree[j][:]
        while i // 2 != j // 2:
            if i % 2 == 0:
                if result[0] > self.tree[i + 1][0]:
                    result = self.tree[i + 1][:]
            if j % 2 == 1:
                if result[0] > self.tree[j - 1][0]:
                    result = self.tree[j - 1][:]
            i, j = i // 2, j // 2
        return result


class intTreeSum:
    '''
    Interval tree that allows query for sum of given interval.
    '''

    def __init__(self, n, type='int'):
        base = 1
        while base < n:
            base *= 2
        self.tree = [0] * (2 * base)
        self.size = base

    def insert(self, i, val=1):
        '''
        Inserts new node to the tree and updates all values in the subtree of
        the new node.

        :param i: Index of node.
        :param val: Value of node.
        '''
        if i < self.size:
            i = self.size + i
            self.tree[i] = val
            while i // 2 != 0:
                i = i // 2
                self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

    def update(self, i, val=1):
        '''
        Updates value of weight between node i and it's parent. It also updates
        all values in the subtree of the node i(all sums in the subtree).

        :param i: Index of the node that's being updated.
        :param val: New weight of the node.
        '''
        if i < self.size:
            i = self.size + i
            self.tree[i] = val
            while i // 2 != 0:
                i = i // 2
                self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

    def query(self, i, j):
        '''
        Returns the sum of interval [i, j] (both ends inclusive) from original
        array.

        :param i: Start of the interval (first node in ascending order)
        :param j: End of the interval   (second node in ascending order)
        :return: Number - sum of euler_weights on the path from i to j
        '''
        result = 0
        if i <= j and j < self.size:
            i, j = i + self.size, j + self.size
            result = self.tree[i]
            if i != j: result = result + self.tree[j]
            while i // 2 != j // 2:
                if i % 2 == 0: result += self.tree[i + 1]
                if j % 2 == 1: result += self.tree[j - 1]
                i, j = i // 2, j // 2
        return result


def make_tour(i, euler_tour, euler_weights, lev, levels, weights, tree, order):
    '''
    Creates all necessary euler tours of the initial tree.

    :param i: Helper value for original index of current node used in recursion.
    :param euler_tour: Array that is to be filled with euler tour of the tree.
    :param euler_weights: Array of euler_weights representing each step in euler tour.
    :param lev: Helper value for level of tree used in recursion.
    :param levels: Levels of each node in euler tour.
    :param weights: euler_weights of nodes in original tree.
    :param tree: Array representing original tree.
    :param order: Array representing an order of traversal of the tree.
    '''
    euler_tour.append(i)
    levels.append(lev)

    # downwards path
    euler_weights.append(weights[i])
    order.append(i)

    for child in tree[i - 1]:
        make_tour(child, euler_tour, euler_weights, lev + 1, levels, weights,
                  tree, order)
        euler_tour.append(i)
        levels.append(lev)

    # upwards path
    order.append(i)
    euler_weights.append(-weights[i])


def parse_file():
    '''
    '''
    # ===========INITIALIZE DATA STRUCTURES=============
    line = sys.stdin.readline().split()
    m, n = int(line[0]), int(line[1])
    tree = []
    weights = [0] * (m + 1)
    for i in range(m):
        tree.append([])

    for i in range(2, m + 1):
        line = sys.stdin.readline().split()
        tree[int(line[0]) - 1].append(i)
        weights[i] = int(line[1])

    euler_tour = []
    euler_weights = []
    euler_levels = []
    order = []

    make_tour(1, euler_tour, euler_weights, 0, euler_levels, weights, tree, order)

    print("Order:")
    print(order)

    print("\nEuler tour:")
    print(euler_tour)

    # pozbywam się wag dotyczących korzenia
    euler_weights = euler_weights[1:-1]

    pierwsze_wyst = []
    for i in range(len(tree)):
        pierwsze_wyst.append([])

    for i in range(len(euler_tour)):
        pierwsze_wyst[euler_tour[i] - 1].append(i)

    level_tree = intTreeMin(len(euler_tour))

    for i in range(len(euler_levels)):
        level_tree.insert(i, euler_tour[i], val=euler_levels[i])

    weight_tree = intTreeSum(len(euler_tour))

    for i in range(len(euler_weights)):
        weight_tree.insert(i, val=euler_weights[i])

    # ==========QUERY==========

    edges = []
    for i in range(len(tree)):
        edges.append([][:])
    for i in range(len(order)):
        edges[order[i] - 1].append(i)

    for i in range(n):
        line = sys.stdin.readline().split()
        if line[0] == 'q':

            # pierwsze wystąpienia poszczególnych węzłów w obiegu Eulera
            first_i = pierwsze_wyst[int(line[1]) - 1][0]
            second_i = pierwsze_wyst[int(line[2]) - 1][0]

            mini = min(first_i, second_i)
            maks = max(first_i, second_i)

            lca = level_tree.query_min(mini, maks)
            # pierwsze wystąpnienie lca w obiegu Eulera
            lca_i = pierwsze_wyst[lca[1] - 1][0]

            first_query_min = min(lca_i, first_i)
            first_query_max = max(lca_i, first_i)

            second_query_min = min(lca_i, second_i)
            second_query_max = max(lca_i, second_i)

            # -1, bo nie wliczam prawego końca przedziału
            first = weight_tree.query(first_query_min, first_query_max - 1)
            second = weight_tree.query(second_query_min, second_query_max - 1)

            print(first + second)

        else:
            # pierwsza część zawiera drogę w dół
            weight_tree.update(edges[int(line[1]) - 1][0] - 1, int(line[2]))

            # druga część zawiera drogę powrotną
            weight_tree.update(edges[int(line[1]) - 1][1] - 1, -int(line[2]))


if __name__ == '__main__':
    parse_file()
