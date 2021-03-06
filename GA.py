from cmath import inf
import random
import numpy as np
from game import Game
import copy
import yaml
import timeit
import datetime

def genetic(q, params, output:bool=True):#μ, pm, pc, iters, length, maks, mini, m):
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
    μ = params["pop_size"]
    pm = params["pm"]
    pc = params["pc"]
    iters = params["iters"]
    length = params["n"] * 4
    maks = params["maks"]
    mini = params["mini"]
    m = params["m"]
    Po = popul_init(μ, length)
    best = -inf
    best_pat = []
    for t in range(iters):
        if output:
            if t % (iters/100) == 0: # for speed print only whole % numbers
                print(' ', str(round(t*100/iters)) + '%   ', end='\r')
        Re = select(Po, μ, q, maks, mini, m)
        Mu = cross_mut(Re, pm, pc, m)
        Po = Mu
        for pat in Po:
            val = q(pat)
            if val > best:
                best = val
                best_pat = copy.deepcopy(pat)
            if best >= 0:
                pass
    if output:
        print('          ', end='\r')
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

def cross_mut(R, pm, pc, m):
    temp = cross(R, pc)
    temp = mut(temp, pm, m)
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
                crossed.append(P[ind])
        else:
            crossed.append(P[ind])
            try:
                crossed.append(P[ind+1])
            except IndexError:
                pass
        ind += 2
    return crossed

def mut(P, pm, m):
    for pattern in P:
        # for unit in pattern:
        #     if random.random() <= pm:
        #         if unit == 1:
        #             unit = 0
        #         else:
        #             unit = 1
        if random.random() <= pm:
            rand_ind = int(random.random() * len(pattern))
            if pattern[rand_ind] == 0:
                pattern[rand_ind] = 1
            else:
                pattern[rand_ind] = 0
            while sum(pattern) > m:
                indices = []
                for ind, i in enumerate(pattern):
                    if i == 1:
                        indices.append(ind)
                rand_ind = int(random.random() * len(indices))
                pattern[indices[rand_ind]] = 0

    return P

def popul_init(μ, length):
    Po = []
    for _ in range(μ):
        temp = np.zeros(length) #np.random.choice([0, 1], size=(length,))
        Po.append(temp.tolist())
    # Po[0] = np.zeros(length)
    return Po
    
def save_params(params:dict, filename:str) -> None:
    with open(filename+"_params.yaml", 'w') as file:
        yaml.safe_dump(params, file, default_flow_style=False)

def read_params(filename:str) -> dict:
    with open(filename+"_params.yaml", 'r') as file:
        params = yaml.safe_load(file)
    return params

def save_result(state:np.array, score:float, exec_time:str, filename:str) -> None:
    try:
        np.savetxt(filename+"_result.txt", state, delimiter=',', fmt='%d', footer="Score: "+str(score) + '\n' + 'Execution time: ' + exec_time)
    except:
        print("SAVING RESULT TO FILE FAILED!")

def run_ga(params:dict, filename:str="", output:bool=True, show_board:bool=True) -> None:
    if params["set_seed_ga"]:
        random.seed(params["seed_ga"])
        np.random.seed(params["seed_ga"])
    # create game
    gejm = Game(params["m"], set_seed=params["set_seed_game"], seed=params["seed_game"])
    gejm.create_random_board(params["n"], params["mini"], params["maks"])
    if show_board:
        print(gejm.board)
    # run GA
    start = timeit.default_timer()
    state, score = genetic(gejm.goal_func, params, output)
    stop = timeit.default_timer()
    exec_time = str(datetime.timedelta(seconds=stop-start))
    state = np.array(state)
    state = np.reshape(state, (4, -1))
    print(state, score)
    # save results to files
    if filename != "" and filename[-1] != '/':
        save_params(params, filename)
        save_result(state, score, exec_time, filename)
        gejm.save_board_to_file(filename+"_board.txt")

def recreate(params_filename:str) -> None:
    params = read_params(params_filename)
    run_ga(params)
