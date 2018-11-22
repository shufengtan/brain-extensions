# Sudoku solver based on heuristics developed by
# Shufeng Tan <shufengtan@gmail.com>

class SudokuSolver(object):
    def __init__(self):
        self.all = set([str(i) for i in range(1, 10)])
        self.bt_count = 0
    def to_lol(self, _str):
        '''Convert a game in string to list of lists'''
        return [[c for c in row.strip()] for row in _str.strip().splitlines()]
    def to_str(self, game):
        return '\n'.join([''.join(row) for row in game])
    def col(self, game, ic):
        return [x for row in game for x in row[ic]]
    def blk(self, game, ix, iy):
        '''ix: 0..2, iy: 0..2'''
        return [n for row in game[ix*3:ix*3+3] for n in row[iy*3:iy*3+3]]
    def count_digits(self, game):
        d2n = {}
        for row in game:
            for d in row:
                d2n[d] = d2n.get(d, 0) + 1
        n_blanks = d2n.pop('0') if '0' in d2n else 0
        return d2n, n_blanks
    def valid(self, game):
        for ix in [0, 1, 2]:
            for iy in [0, 1, 2]:
                for n in range(1, 10):
                    if self.blk(game, ix, iy).count(str(n)) > 1:
                        return False
        for idx in range(9):
            for n in range(1, 10):
                if game[idx].count(str(n)) > 1 or self.col(game, idx).count(str(n)) > 1:
                    return False
        return True
    def each_blank(self, game):
        for i in range(9):
            for j in range(9):
                if game[i][j] == '0':
                    yield i, j
    def candidate_digits(self, game, i, j):
        return self.all - set(game[i] + self.col(game, j) + self.blk(game, i//3, j//3))
    def spawn(self, game, triplets):
        '''Make a copy of a given game, then update with triplets of (i, j, digit)'''
        game2 = [row[:] for row in game[:]]
        for i, j, d in triplets:
            print(f'...spawned game[{i}][{j}] = {d}')
            game2[i][j] = str(d)
        return game2
    def two_maps(self, game):
        '''Return two dicts: (i,j)->digit and digit->(i, j)'''
        ij2d = {}
        d2ij = {}
        n_blanks = 0
        for i in range(9):
            for j in range(9):
                if game[i][j] == '0':
                    n_blanks += 1
                else:
                    digit = game[i][j]
                    ij2d[(i, j)] = digit
                    if digit in d2ij:
                        d2ij[digit].append((i, j))
                    else:
                        d2ij[digit] = [(i, j)]
        return ij2d, d2ij, n_blanks
    def candidates_ijs(self, dijs, ij2d):
        ro_rows = set()
        ro_cols = set()
        ro_blks = set()
        for i, j in dijs:
            ro_rows.add(i)
            ro_cols.add(j)
            ro_blks.add((i//3, j//3))
        cands = []
        for i in range(9):
            if i in ro_rows:
                continue
            for j in range(9):
                if j in ro_cols or (i//3, j//3) in ro_blks or (i, j) in ij2d:
                    continue
                cands.append((i, j))
        return cands
    def squeeze(self, game):
        '''Three types of squeeze for all digits present: row, column and 3x3 squares'''
        for _iter in range(1000):
            ij2d, d2ij, n_blanks = self.two_maps(game)
            if n_blanks == 0:
                break
            progress = 0
            for digit in sorted(d2ij.keys(), key=lambda k: len(d2ij[k]), reverse=True):
                dijs = d2ij[digit]
                if len(dijs) == 9:
                    continue
                cands = self.candidates_ijs(dijs, ij2d)
                count_by_row = {}
                count_by_col = {}
                count_by_blk = {}
                for i, j in cands:
                    count_by_row[i] = count_by_row.get(i, 0) + 1
                    count_by_col[j] = count_by_col.get(j, 0) + 1
                    blk = (i//3, j//3)
                    count_by_blk[blk] = count_by_blk.get(blk, 0) + 1
                for i in count_by_row:
                    if count_by_row[i] == 1:
                        for i2, j in cands:
                            if i == i2 and game[i][j] == '0':
                                game[i][j] = digit
                                print(f'row    squeeze: game[{i}][{j}] = {digit}')
                                progress += 1
                for j in count_by_col:
                    if count_by_col[j] == 1:
                        for i, j2 in cands:
                            if j == j2 and game[i][j] == '0':
                                game[i][j] = digit
                                #print(f'{digit}: {cands}')
                                print(f'column squeeze: game[{i}][{j}] = {digit}')
                                progress += 1
                for blk in count_by_blk:
                    if count_by_blk[blk] == 1:
                        for i, j in cands:
                            if (i//3, j//3) == blk and game[i][j] == '0':
                                game[i][j] = digit
                                #print(f'{digit}: {cands}')
                                print(f'square squeeze: game[{i}][{j}] = {digit}')
                                progress += 1
            if progress == 0:
                break
    def final_check(self, game):
        '''Called when no blank'''
        str_game = self.to_str(game)
        for i in range(9):
            if len(set(game[i])) != 9:
                print(f'False solution (r{i})\n{str_game}')
                return False
            if len(set([row[i] for row in game])) != 9:
                print(f'False solution (c{i})\n{str_game}')
                return False
        for i in range(3):
            for j in range(3):
                if len(set(self.blk(game, i, j))) != 9:
                    print(f'False solution (b {i},{j}){str_game}')
                    return False
        return True
    def df_search(self, game0, next_moves=[None]):
        '''Depth-first search: evaluate candidate digits for all blanks.'''
        for next_move in next_moves:
            game = self.spawn(game0, [next_move]) if next_move else self.spawn(game0, [])
            for _iter in range(100):
                d2n, n_blanks = self.count_digits(game)
                if n_blanks == 0:
                    if self.final_check(game):
                        print(f'Solved!\n{self.to_str(game)}')
                        return True
                    else:
                        break
                print(f'{n_blanks} blanks')
                progress = 0
                branches = {}
                valid = True
                for i, j in self.each_blank(game):
                    nn = self.candidate_digits(game, i, j)
                    if len(nn) == 0:
                        print(f'Invalid at [{i}][{j}]!')
                        valid = False
                        break
                    elif len(nn) == 1:
                        game[i][j] = str(list(nn)[0])
                        progress += 1
                        print(f'game[{i}][{j}] = {game[i][j]}')
                        self.squeeze(game)
                        break
                    else:
                        branches[(i, j)] = nn
                if not valid:
                    break
                if progress > 0:
                    continue
                else:
                    # This is my heuristic
                    scores = dict([(k, sum([d2n[x] for x in branches[k]])) for k in branches])
                    ij = sorted(branches.keys(), key=scores.get)[0]
                    print(f'Possible choices for [{ij[0]}][{ij[1]}]: {branches[ij]}')
                    if self.df_search(game, [(ij[0], ij[1], d) for d in branches[ij]]):
                        return True
                    else:
                        break

if __name__ == "__main__":
    solver = SudokuSolver()
    game = solver.to_lol('''
        020905010
        049008000
        031000400
        000000507
        003002000
        496000000
        000010800
        000307000
        000000065
''')
    import time
    t0 = time.time()
    solver.squeeze(game)
    solver.df_search(game)
    print(f'Solved in {int(1000*(time.time() - t0))} miliseconds.')

