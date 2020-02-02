import random
import time
import statistics
import sys


class Chromosome:
    Genes = None
    Fitness = None

    def __init__(self, genes, fitness):
        self.Genes = genes
        self.Fitness = fitness


class Benchmark:
    @staticmethod
    def run(function):
        timings = []
        stdout = sys.stdout
        for i in range(100):
            sys.stdout = None
            start_time = time.time()
            function()
            seconds = time.time() - start_time
            sys.stdout = stdout
            timings.append(seconds)
            mean = statistics.mean(timings)
            if i < 10 or i % 10 == 9:
                print("{0} {1:3.2f} {2:3.2f}".format(
                    1+i, mean,
                    statistics.stdev(timings, mean)
                    if i > 1 else 0))


def _generate_parent(length, gene_set,get_fitness):
    genes = []
    while len(genes) < length:
        # 一位一位随机也可以，但是长一点比较可以体现不重复随机的优势？其实用带重复随机的也可以。
        sample_size = min(length - len(genes), len(gene_set))
        genes.extend(random.sample(gene_set, sample_size))
    fitness = get_fitness(genes)
    return Chromosome(genes, fitness)


def _mutate(parent, gene_set, get_fitness):
    child_genes = parent.Genes[:]
    index = random.randrange(0, len(parent.Genes))
    new_gene, alternate = random.sample(gene_set, 2)
    if new_gene == child_genes[index]:
        child_genes[index] = alternate
    else:
        child_genes[index] = new_gene
    fitness = get_fitness(child_genes)
    return Chromosome(child_genes, fitness)


def get_best(get_fitness, target_len, optimal_fitness, gene_set, display):
    random.seed()
    best_parent = _generate_parent(target_len, gene_set, get_fitness)
    display(best_parent)
    if best_parent.Fitness >= optimal_fitness:
        return best_parent
    while True:
        child = _mutate(best_parent, gene_set, get_fitness)
        if best_parent.Fitness >= child.Fitness:
            continue
        display(child)
        if child.Fitness >= optimal_fitness:
            return child
        best_parent = child
