import unittest
import datetime
import genetic


# 利用遗传算法的思想生成一个递增数列，数列里面的数字来自[range(100)]
def display(candidate, start_time):
    time_diff = datetime.datetime.now() - start_time
    print("{0}\t=> {1}\t{2}".format(
        ', '.join(map(str, candidate.Genes)),
        candidate.Fitness,
        str(time_diff)
    ))


class Fitness:
    numbers_in_sequence_count = None
    total_gap = None

    def __init__(self, number_in_sequesce_count, total_gap):
        self.numbers_in_sequence_count = number_in_sequesce_count
        self.total_gap = total_gap

    # 为get_best写一个cmp函数">"来约束fitness权重
    # 单纯统计一个序列的“上升对”对数会陷入stall；于是我们约定：
    # 如果两个序列的上升对数相同，则优先按照gap小的改变fitness
    # 此处gap指的是一个序列中非上升对的数对差多少才能上升。
    # 比如 9 30 1 20 60 这个序列, num_in_seq = 3, gap = 29
    # 9 30 15 20 60, num_in_seq = 3, gap = 15
    # 9 16 1 20 60, num_in_seq = 3, gap = 15
    def __gt__(self, other):
        if self.numbers_in_sequence_count != other.numbers_in_sequence_count:
            return self.numbers_in_sequence_count > other.numbers_in_sequence_count
        return self.total_gap < other.total_gap

    def __str__(self):
        return "{0} Sequential, {1} Total Gap".format(
            self.numbers_in_sequence_count,
            self.total_gap
        )


# 因为重写的是gt，所以要把get_best里面的比较都改成大于号，
# 不然这个重写就白写了
def get_fitness(genes):
    fitness = 1
    gap = 0
    for i in range(1, len(genes)):
        if genes[i] > genes[i - 1]:
            fitness += 1
        else:
            gap += genes[i - 1] - genes[i]
    return Fitness(fitness, gap)


class SortedNumberTests(unittest.TestCase):
    def test_sort_10_numbers(self):
        self.sort_numbers(10)

    def test_benchmark(self):
        genetic.Benchmark.run(lambda: self.sort_numbers(40))

    def sort_numbers(self, total_numbers):
        gene_set = [i for i in range(100)]
        start_time = datetime.datetime.now()

        def fnDisplay(candidate):
            display(candidate, start_time)

        def fnGetFitness(genes):
            return get_fitness(genes)

        optimal_fitness = Fitness(total_numbers, 0)
        best = genetic.get_best(fnGetFitness, total_numbers,
                                optimal_fitness, gene_set, fnDisplay)
        self.assertTrue(not optimal_fitness > best.Fitness)


if __name__ == '__main__':
    unittest.main()