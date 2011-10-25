from backtracking import backtracking
import re

Choices = [' ', 'x']

def hv_counts(data):
    given = [map(int, line.split()) for line in data.splitlines() if re.search(r'\d', line)]
    dim = given[0]
    assert len(given) == sum(dim) + 1
    h_counts = given[1:1+dim[1]]
    v_counts = given[1+dim[1]:]
    return h_counts, v_counts

def search():
    that_idx = None     # index for THAT dimension
    this_counts = None  # counts for THIS dimension
    this_dim = None     # len of THIS dimension
    this_sol = None # choices in THIS dimension, len == 0 or this_dim
    def counts_assignable(cpoint, choice, sol):
        if len(this_sol) > cpoint and Choices[choice] not in set([c[that_idx] for c in this_sol[cpoint]]):
            return False
        if cpoint in sol:
            return sol[cpoint] == choice
        else:
            sol2 = dict(sol)
            sol2[cpoint] = choice
            sol_counts = map(len, re.findall(r'x+', ''.join([Choices[sol2[k]] for k in sorted(sol2.keys())])))
            if len(sol_counts) > len(this_counts):
                return False
            if len(sol_counts) > 0 and max(sol_counts) > max(this_counts):
                return False
            if len(sol2) == this_dim:
                return sol_counts == this_counts
            if 0 in sol2:
                sol_this_counts = zip(sol_counts[:-1], this_counts)
                if len(sol_this_counts) >= 1:
                    #print '##', sol_this_counts
                    for c1, c2 in sol_this_counts:
                        #print '# that idx %d: %d, %d' % (that_idx, c1, c2)
                        if c1 != c2:
                            return False
            else:
                print "??", sol2
            return True
    h_sol = []
    v_sol = []
    for itr in xrange(10):
        print 'iteration', itr
        v_sol = []
        for v_idx in range(V_dim):
            # this is horizonal
            that_idx = v_idx
            this_counts = H_counts[v_idx]
            this_dim = H_dim
            this_sol = h_sol
            ss = []
            for hc in backtracking(range(H_dim), Choices, counts_assignable):
                print 'V %d |%s|' % (v_idx, ''.join([hc[x] for x in range(H_dim)]))
                ss.append(hc)
            v_sol.append(ss)
        print 'v_sol', map(len, v_sol)
        for vs in v_sol:
            if len(vs) > 1:
                break
        else:
            print "Found unique solution:"
            for vs in v_sol:
                print ''.join([vs[0][x] for x in range(H_dim)])
            return
        h_sol = []
        for h_idx in range(H_dim):
            # this is vertical
            that_idx = h_idx
            this_counts = V_counts[h_idx]
            this_dim = V_dim
            this_sol = v_sol
            ss = []
            for vc in backtracking(range(V_dim), Choices, counts_assignable):
                print 'H %d |%s|' % (h_idx, ''.join([vc[y] for y in range(V_dim)]))
                ss.append(vc)
            h_sol.append(ss)

if __name__ == '__main__':
    import sys
    data_file = sys.argv[1]
    fh = open(data_file)
    data = fh.read()
    fh.close()
    H_counts, V_counts = hv_counts(data)
    H_dim = len(V_counts)
    V_dim = len(H_counts)
    print 'H dim', H_dim, 'V dim', V_dim
    print 'H counts:', H_counts
    print 'V counts:', V_counts
    search()
