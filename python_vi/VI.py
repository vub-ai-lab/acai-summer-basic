import copy
import operator

def valueIteration(S, A, discount, horizon, epsilon, T, R):
    v1 = [0] * S

    ir = computeImmediateRewards(S, A, T, R)

    timestep = 0
    variation = epsilon * 2

    useEpsilon = epsilon != 0
    while timestep < horizon and (not useEpsilon or variation > epsilon):
        timestep += 1

        v0 = v1[:]

        v1 = [v * discount for v in v1]
        iir = copy.deepcopy(ir)
        q = computeQFuncton(S, A, T, v1, iir)

        a1, v1 = bellmanOperator(S, q, v1)

        if useEpsilon:
            variation = max([abs(vv0 - vv1) for vv0, vv1 in zip(v0, v1)])

    return a1, v1


def computeImmediateRewards(S, A, T, R):
    ir = [[0 for i in xrange(A)] for i in xrange(S)]

    for s in xrange(S):
        for a in xrange(A):
            for s1 in xrange(S):
                ir[s][a] += T[s][a][s1] * R[s][a][s1]

    return ir

def computeQFuncton(S, A, T, v, ir):
    for s in xrange(S):
        for a in xrange(A):
            for s1 in xrange(S):
                ir[s][a] += T[s][a][s1] * v[s1]

    return ir

def bellmanOperator(S, q, v):
    a = [0] * S
    for s in xrange(S):
        a[s], v[s] = max(enumerate(q[s]), key=operator.itemgetter(1))

    return a, v
