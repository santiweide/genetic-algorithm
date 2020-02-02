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


# 产生新的数据
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


# 从基因池里面选择Fitness更高的child作为newchild
def _get_improvement(new_child, generate_parent):
    best_parent = generate_parent()
    yield best_parent
    while True:
        child = new_child(best_parent)
        # p > c 说明子代没有更fit的
        if best_parent.Fitness > child.Fitness:
            continue
        # c == p(即p <= c && c <= p)
        # 说明 有了一个和best parent权值相同的child，
        # 我们选择更新parent但是不返回这个值
        if not child.Fitness > best_parent.Fitness:
            best_parent = child
            continue
        yield child
        best_parent = child


# _get_improvement抽象了选择更fit自代的过程，
# 这样get_best就只需要对得到的优秀自带进行显示和判断是否达到返回条件
def get_best(get_fitness, target_len, optimal_fitness, gene_set, display):
    random.seed()

    def fnMutate(parent):
        return _mutate(parent, gene_set, get_fitness)

    def fnGenerateParent():
        return _generate_parent(target_len, gene_set, get_fitness)

    for improvement in _get_improvement(fnMutate, fnGenerateParent):
        display(improvement)
        if not optimal_fitness > improvement.Fitness:
            return improvement
