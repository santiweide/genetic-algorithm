# 解决生成exactly the same string、 生成拥有尽可能多的1的序列、生成一个递增序列的时候，
# 我们的基因空间**就是**解空间的直接来源，但是实际上很多问题并没有这么方便
# 比如八皇后中，我们的解空间实际上是一个个8*8的棋盘以及上面的皇后位置。我们希望他们可以被抽象为数字
# 比如考虑棋盘有皇后是1，没皇后是0，那么一横行就是一个01序列，一行八个数字，就是一行一个8位二进制整数
# 一共8行，就是拼成一个64位整数。这样一个棋盘状态就可以用一个64位整数来记载。
# 这就像基因型和表现型：基因型是64位整数，表现型是数组内64位整数翻译成的棋盘布局。
# 我们总是用框架枚举基因型，吧基因型放到框架里运算出满足optimal_fitness的基因型，
# 在输出的时候才把基因型转化为表现型。
# 不过我们在这里没有选择这样表示，毕竟是python也没啥速度和内存要求，
# 就用一个16个数字的数组记录8个皇后的位置了。genes[2*k]，gene[2*k+1]表示皇后k的坐标。k=0,1,2,...
import unittest
import datetime
import genetic


# 我们约定gene是一个长度为2*n序列，表示n皇后问题
# 第2*k+1和第2*k+2个分别表示一个皇后所在的行号和列号
# 其中k=0,1,2,...
class Board:
    def __init__(self, genes, size):
        # 初始化所有board都是没有皇后的
        board = [['.'] * size for _ in range(size)]
        for index in range(0, len(genes), 2):
            row = genes[index]
            column = genes[index + 1]
            board[column][row] = 'Q'
        self._board = board

    def print(self):
        # 0,0 print in bottom left corner
        for i in reversed(range(0, len(self._board))):
            print(' '.join(self._board[i]))

    def get(self, row, column):
        return self._board[column][row]


class Fitness:
    Total = None

    def __init__(self, total):
        self.Total = total

    def __gt__(self, other):
        return self.Total < other.Total

    def __str__(self):
        return "{0}".format(self.Total)


def get_fitness(genes, size):
    board = Board(genes, size)
    rows_with_queens = set()
    cols_with_queens = set()
    north_east_diagonal_with_queens = set()
    south_east_diagonal_with_queens = set()
    for row in range(size):
        for col in range(size):
            if board.get(row, col) == 'Q':
                rows_with_queens.add(row)
                cols_with_queens.add(col)
                north_east_diagonal_with_queens.add(row + col)
                south_east_diagonal_with_queens.add(size - 1 - row + col)

    total = size - len(rows_with_queens) \
            + size - len(cols_with_queens) \
            + size - len(north_east_diagonal_with_queens) \
            + size - len(south_east_diagonal_with_queens)

    return Fitness(total)


def display(candidate, start_time, size):
    time_diff = datetime.datetime.now() - start_time
    board = Board(candidate.Genes, size)
    board.print()
    print("{0}\t- {1}\t{2}".format(
        ' '.join(map(str, candidate.Genes)),
        candidate.Fitness,
        str(time_diff)
    ))


class EightQueensTests(unittest.TestCase):
    def test(self, size=8):
        gene_set = [i for i in range(size)]
        start_time = datetime.datetime.now()

        def fnDisplay(candidate):
            display(candidate, start_time, size)

        def fnGetFitness(genes):
            return get_fitness(genes, size)

        optimal_fitness = Fitness(0)
        best = genetic.get_best(fnGetFitness, 2 * size,
                                optimal_fitness, gene_set, fnDisplay)
        self.assertTrue(not optimal_fitness > best.Fitness)

    def test_benchmark(self):
        genetic.Benchmark.run(lambda: self.test(20))
