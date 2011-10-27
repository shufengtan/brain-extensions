from backtracking import backtracking
import re

Choices = [' ', 'x']
cluster_re = re.compile(filter(lambda x: x != ' ',  Choices)[0] + '+')

def count_clusters(s):
    return map(len, cluster_re.findall(''.join([Choices[s[k]] for k in sorted(s.keys())])))

def hv_counts(data):
    given = [map(int, line.split()) for line in data.splitlines() if re.search(r'\d', line)]
    dim = given[0]
    assert len(given) == sum(dim) + 1
    d_i_c =  [((0, i), c) for i, c in enumerate(given[1:1+dim[1]])]
    d_i_c += [((1, i), c) for i, c in enumerate(given[1+dim[1]:])]
    return dict(d_i_c)

def assignments(m, n):
    '''Calc how many ways of putting m items in n boxes'''
    if m == 1:
        return n
    if n <= 1:
        return n
    return sum(assignments(m - i, n - 1) for i in range(m+1))

def dof(counts, dim):
    '''Calculate degree of freedom'''
    lc = len(counts)
    return(assignments(dim - (sum(counts) + lc - 1), lc + 1))

class PC32:
    def __init__(self, data):
        given = [map(int, line.split()) for line in data.splitlines() if re.search(r'\d', line)]
        dim = given[0]
        assert len(given) == sum(dim) + 1
        d_i_c =  [((0, i), c) for i, c in enumerate(given[1:1+dim[1]])]
        d_i_c += [((1, i), c) for i, c in enumerate(given[1+dim[1]:])]
        hv_counts = dict(d_i_c)
        self.dim = dim
        self.hv_counts = hv_counts
        self.dof = dict([(d_i, dof(hv_counts[d_i], dim[d_i[0]])) for d_i in hv_counts])
        self.candidates = {}
        self.debug = False
    def box_assignable(self, cpoint, choice, sol):
        '''This method determines if a choice satisfies all constraints for the current solution.'''
        this_d_i = self.d_i
        this_counts = self.hv_counts[this_d_i]
        sol2 = dict(sol)
        sol2[cpoint] = choice
        sol_counts = count_clusters(sol2)
        this_dim = self.dim[this_d_i[0]]
        that_d = 1 - this_d_i[0]
        that_dim = self.dim[that_d]
        debug = self.debug
        if len(sol_counts) > len(this_counts):
            if debug:
                print '#', this_d_i, cpoint, choice, 'return A false', sol_counts, this_counts
            return False
        boxes_left = that_dim - cpoint - 1
        if len(sol_counts) > 0:
            if max(sol_counts) > max(this_counts):
                if debug:
                    print '#', this_d_i, cpoint, choice, 'return B false'
                return False
        else:
            boxes_needed = sum(this_counts) + len(this_counts) - 1
            if boxes_left < boxes_needed:
                if debug:
                    print '#', this_d_i, cpoint, choice, 'return C false', boxes_left, boxes_needed
                return False
        if 0 in sol2:
            sol_this_counts = zip(sol_counts, this_counts)
            if len(sol_this_counts) > 0:
                if sol_this_counts[-1][0] > sol_this_counts[-1][1]:
                    # last count in sol already > last count in constraint
                    if debug:
                        print '#', this_d_i, cpoint, choice, 'return D false'
                    return False
                elif sol_this_counts[-1][0] != sol_this_counts[-1][1] and Choices[choice] == ' ':
                    if debug:
                        print '#', this_d_i, cpoint, choice, 'return E false'
                    return False
            if len(sol_this_counts) > 1:
                for c1, c2 in sol_this_counts[:-1]:
                    if c1 != c2:
                        if debug:
                            print '#', this_d_i, cpoint, choice, 'return F false'
                        return False
            if sol_counts:
                boxes_needed = sol_this_counts[-1][1] - sol_this_counts[-1][0]
                if len(sol_counts) < len(this_counts):
                    this_counts_left = this_counts[len(sol_counts):]
                    boxes_needed += sum(this_counts_left) + len(this_counts_left) - 1
                if boxes_left < boxes_needed:
                    if debug:
                        print '#', this_d_i, cpoint, choice, 'return G false', boxes_left, boxes_needed
                    return False
        candidates = self.candidates
        if (that_d, cpoint) in candidates:
            c_list = map(lambda c: c[this_d_i[1]], candidates[(that_d, cpoint)])
            if Choices[choice] not in c_list:
                 if debug:
                     print '#', this_d_i, cpoint, choice, 'return H false', that_d
                     for c in candidates[(that_d, cpoint)]:
                         print '|%s|' % ''.join([c[i] for i in xrange(len(c))])
                 return False
        if len(sol2) == that_dim:
            res = sol_counts == this_counts
            if debug:
                print "#", this_d_i, cpoint, choice, 'return I', res
            return res
        if debug:
            print '#', this_d_i, cpoint, choice, 'fall through True', this_counts, sol_counts
        return True
    def solve(self, d_i_list):
        for d_i in d_i_list:
            print 'DoF', d_i, self.hv_counts[d_i], self.dof[d_i]
        dim = self.dim
        candidates = self.candidates
        cand_counts = [None, None]
        prev_cand_counts = [None, None]
        for itr in xrange(1000):
            print 'Iteration', itr
            for d_i in d_i_list:
                self.d_i = d_i
                this_dim = dim[d_i[0]]
                that_dim = dim[1 - d_i[0]]
                this_idx = d_i[1]
                self.candidates[d_i] = []
                for candidate in backtracking(range(this_dim), Choices, self.box_assignable):
                    if candidate not in self.candidates[d_i]:
                        self.candidates[d_i].append(candidate)
                print 'D%d %2d %d/%d' % (d_i[0], d_i[1], len(self.candidates[d_i]), self.dof[d_i])
            for d in (0, 1):
                cand_counts[d] = [len(self.candidates[(d, idx)]) for idx in xrange(dim[1-d])]
            if cand_counts[0] == prev_cand_counts[0] and cand_counts[1] == prev_cand_counts[1]:
                print 'Candidate counts remain the same. Stop.', cand_counts
                break
            for d in (0, 1):
                prev_cand_counts[d] = cand_counts[d]
            if len(set(cand_counts[0])) == 1 and cand_counts[0][0] == 1:
                print '** Found unique solution'
                break
        for y in xrange(dim[1]):
            print ''.join([candidates[(0, y)][0][x] for x in xrange(dim[0])])

if __name__ == '__main__':
    import sys
    data_file = sys.argv[1]
    #data_file = 'pc32_2.txt'
    fh = open(data_file)
    data = fh.read()
    fh.close()
    pc32 = PC32(data)
    d_i_list = pc32.hv_counts.keys()
    d_i_list.sort(key=pc32.dof.get)
    pc32.solve(d_i_list)
