import datetime
import genetic
import unittest
import random

# 从字符集合中选取合适字符使得最终字符串与给定字符串相同


def display(candidate, start_time):
    time_diff = datetime.datetime.now() - start_time
    print("{0}\t{1}\t{2}".format(
        ''.join(candidate.Genes),
        candidate.Fitness,
        str(time_diff)))


def get_fitness(genes, target):
    return sum(1 for expected, actual in zip(target, genes)
               if expected == actual)


class GuessPasswordTests(unittest.TestCase):
    gene_set = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!.,"

    def test_random(self):
        length = 150
        target = ''.join(random.choice(self.gene_set) for _ in range(length))
        self.guess_password(target)

    def test_benchmark(self):
        genetic.Benchmark.run(self.test_random)

    def guess_password(self, target):
        start_time = datetime.datetime.now()

        def fnGetFitness(genes):
            return get_fitness(genes, target)

        def fnDisplay(candidate):
            display(candidate, start_time)

        optimal_fitness = len(target)
        best = genetic.get_best(fnGetFitness, len(target), optimal_fitness, self.gene_set, fnDisplay)
        self.assertEqual(''.join(best.Genes), target)


if __name__ == '__main__':
    unittest.main()
