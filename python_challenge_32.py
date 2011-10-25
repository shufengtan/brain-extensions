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
    this_choices = None # choices in THIS dimension, len == 0 or this_dim
    def counts_assignable(cpoint, choice, sol):
        #print 'choice point', cpoint, 'choice', choice, 'sol len', len(sol)
        if len(this_choices) > cpoint and Choices[choice] not in set([c[that_idx] for c in this_choices[cpoint]]):
            return False
        if cpoint in sol:
            return sol[cpoint] == choice
        else:
            sol2 = dict(sol)
            sol2[cpoint] = choice
            if len(sol2) == this_dim:
                sol_counts = map(len, re.findall(r'x+', ''.join([Choices[sol2[k]] for k in sorted(sol2.keys())])))
                if sol_counts != this_counts:
                    return False
            sol[cpoint] = choice
            return True
    h_sol = []
    for itr in xrange(10):
        print 'iteration', itr
        v_sol = []
        for v_idx in range(V_dim):
            # this is horizonal
            that_idx = v_idx
            this_counts = H_counts[v_idx]
            this_dim = H_dim
            this_choices = h_sol
            v_sol.append([hc for hc in backtracking(range(H_dim), Choices, counts_assignable)])
            for vc in v_sol[-1]:
                print 'V', v_idx, vc
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
            this_choices = v_sol
            h_sol.append([vc for vc in backtracking(range(V_dim), Choices, counts_assignable)])
            for hc in h_sol[-1]:
                print 'H', h_idx, hc

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
