from cmath import inf
import random
import numpy as np
from game import Game
import copy

def genetic(q, μ, pm, pc, iters, length, maks, mini, m):
    '''
    q - funkcja celu
    μ - liczebnosc populacji
    pm - prawdopodobienstwo mutacji
    pc - prawdopodobienstwo krzyzowania
    iters - liczba pokoleń
    length - długość wektora (4*n)
    maks - maksymalna wartość na planszy
    mini - minimalna wartość na planszy
    m - liczba kart
    '''
    t = 0
    Po = popul_init(μ, length)
    best = -inf
    best_pat = []
    while t < iters:
        Re = select(Po, μ, q, maks, mini, m)
        Mu = cross_mut(Re, pm, pc )
        Po = Mu
        for pat in Po:
            val = q(pat)
            # print(pat, q(pat))
            if val > best:
                # print(np.reshape(pat, (4, -1)))
                # print(val)
                best = val
                best_pat = copy.deepcopy(pat)
                # print("best:")
                # print(np.reshape(best_pat, (4, -1)), '\n')
            if best >= 0:
                pass
            # else:
                # print(":C")
        t = t + 1
    # for pattern in Po:
    #     if q(pattern) > best:
    #         best = q(pattern)
    #         best_pat = pattern
    # print("ostatni best:")
    # print(np.reshape(best_pat, (4, -1)), '\n')
    return best_pat, best

def probability(P, pattern, q, maks, mini, m):
    if q(pattern) != -inf:
        try:
            return (q(pattern) -mini*m) / ((maks - mini)*m)
        except ZeroDivisionError:
            return 0
    else:
        return 0

def sum_goal(P, q):
    summ = 0
    for pattern in P:
        summ += q(pattern)
    return summ

def select(P, μ, q, maks, mini, m):
    weights = []
    sel_inds = []
    for i in P:
        weights.append(probability(P, i, q, maks, mini, m))
    if sum(weights) == 0:
        for i in range(len(weights)):
            weights[i] = 1
    for i in range(μ):
        sel_inds.append(random.choices(range(0,μ), weights=weights, k=1)[0])
    return [P[i] for i in sel_inds]

def cross_mut(R, pm, pc):
    temp = cross(R, pc)
    temp = mut(temp, pm)
    return temp

def cross(P, pc):
    ind = 0
    crossed = []
    while ind < len(P):
        if random.random() <= pc:
            try:
                point = random.randrange(len(P[ind]))
                temp = P[ind][point:]
                P[ind][point:] = P[ind+1][point:]
                P[ind+1][point:] = temp
                crossed.append(P[ind])
                crossed.append(P[ind+1])
            except IndexError:
                point = random.randrange(len(P[ind]))
                P[ind][point:] = P[0][point:]
                crossed.append(P[ind][point:])
        else:
            crossed.append(P[ind])
            try:
                crossed.append(P[ind+1])
            except IndexError:
                pass
        ind += 2
    return crossed

def mut(P, pm):
    for pattern in P:
        for unit in pattern:
            if random.random() <= pm:
                if unit == 1:
                    unit = 0
                else:
                    unit = 1
    return P

def popul_init(μ, length):
    Po = []
    for _ in range(μ):
        temp = np.random.choice([0, 1], size=(length,))
        Po.append(temp.tolist())
    return Po

if __name__ == "__main__":
    m = 16
    n = 8
    mini = -10
    maks = 10
    gejm = Game(m)
    gejm.create_random(n, mini, maks)
    print(gejm.board)

    iters = 20000
    pop_size = 100
    pm = 0.1
    pc = 0.1
    # for i in range(25):
    # print(gejm.goal_func([0, 1, 1, 0, 0, 1, 1, 0]))
    state, score = genetic(gejm.goal_func, pop_size, pm, pc, iters, n*4, maks, mini, m)
    state = np.array(state)
    state = np.reshape(state, (4, -1))
    print(state, score)
    try:
        print(gejm.goal_func(state))
    except Exception:
        pass
