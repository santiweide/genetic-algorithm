# 解决地图上色问题：保证相邻两个州的颜色不一样
import unittest
import datetime
import genetic
import csv


# csv格式形如AA,BB;CC表示AA州的邻居有BB州、CC州。同时BB和CC也会作为一列在csv中出现。
# 我们使用字典存储这个图。
def load_data(file_name):
    with open(file_name, "r") as infile:
        reader = csv.reader(infile)
        lookup = {row[0]: row[1].split(";") for row in reader if row}
    return lookup


# 创建邻接表Rule存储
# 为hash做准备，要重写equal函数__eq__
class Rule:
    Node = None
    Adjacent = None

    def __init__(self, node, adjacent):
        if node < adjacent:
            node, adjacent = adjacent, node
        self.Node = node
        self.Adjacent = adjacent

    def __eq__(self, other):
        return self.Node == other.Node and \
               self.Adjacent == other.Adjacent

    def __hash__(self):
        return hash(self.Node) * 397 ^ hash(self.Adjacent)

    def __str__(self):
        return self.Node + " -> " + self.Adjacent

    def IsValid(self, genes, node_index_lookup):
        index = node_index_lookup[self.Node]
        adjacent_state_index = node_index_lookup[self.Adjacent]
        return genes[index] != genes[adjacent_state_index]


def build_rules(items):
    rules_added = {}

    for state, adjacent in items.items():
        for adjacent_state in adjacent:
            if adjacent_state == '':
                continue
            rule = Rule(state, adjacent_state)
            if rule in rules_added:
                rules_added[rule] += 1
            else:
                rules_added[rule] = 1

    # 也要检查是否满足无向图特性~你连我那么我也连你！
    for k, v in rules_added.items():
        if v != 2:
            print("rule {0} is not bidirectional".format(k))

    return rules_added.keys()


def display(candidate, start_time):
    time_diff = datetime.datetime.now() - start_time
    print("{0}\t{1}\t{2}".format(
        ''.join(map(str, candidate.Genes)),
        candidate.Fitness,
        str(time_diff)))


def get_fitness(genes, rules, state_index_lookup):
    rules_passed = sum(1 for rule in rules
                       if rule.IsValid(genes, state_index_lookup))
    return rules_passed


class GraphColoringTests(unittest.TestCase):
    def test(self):
        states = load_data("continents.csv")
        rules = build_rules(states)
        optimal_value = len(rules)
        state_index_lookup = {key: index
                              for index, key in enumerate(sorted(states))}

        colors = ["Orange", "Yellow", "Green", "Blue"]
        color_lookup = {color[0]: color for color in colors}
        gene_set = list(color_lookup.keys())

        start_time = datetime.datetime.now()

        def fnDisplay(candidate):
            display(candidate, start_time)

        def fnGetFitness(genes):
            return get_fitness(genes, rules, state_index_lookup)

        best = genetic.get_best(fnGetFitness, len(states), optimal_value, gene_set, fnDisplay)
        self.assertTrue(not optimal_value > best.Fitness)

        keys = sorted(states.keys())
        for index in range(len(states)):
            print(keys[index] + " is " + color_lookup[best.Genes[index]])


if __name__ == '__main__':
    unittest.main()