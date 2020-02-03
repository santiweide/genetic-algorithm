import unittest
import datetime
import genetic
# 从{0，1}中选取数字生成数组，使得生成数组中的1最多


def display(candidate, start_time):
    time_diff = datetime.datetime.now() - start_time
    # map只是一种方便地把数字转换成字符串的方法而已
    print("{0}...{1}\t{2:3.2f}\t{3}".format(
        ''.join(map(str, candidate.Genes[:15])),
        ''.join(map(str, candidate.Genes[-15:])),
        candidate.Fitness,
        str(time_diff)
    ))


def get_fitness(genes):
    return genes.count(1)


class OneMaxTests(unittest.TestCase):
    def test(self, length=100):
        gene_set = [0, 1]
        start_time = datetime.datetime.now()

        def fnDisplay(candidate):
            display(candidate, start_time)

        def fnGetFitness(genes):
            return get_fitness(genes)

        optimal_fitness = length
        best = genetic.get_best(fnGetFitness, length, optimal_fitness,
                               gene_set, fnDisplay)
        self.assertEqual(best.Fitness, optimal_fitness)

    def test_benchmark(self):
        genetic.Benchmark.run(lambda : self.test(4000))


if __name__ == '__main__':
    unittest.main()