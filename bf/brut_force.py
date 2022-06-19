from sympy.utilities.iterables import multiset_permutations
from game import Game
import numpy as np
import timeit
import datetime

def main():
    m = 16
    n = 7
    mini = -10
    maks = 10
    game = Game(m, set_seed=True, seed=2137)
    game.create_random_board(n, mini, maks)
    print(game.board)
    best_val = -np.inf
    best_state = None
    start = timeit.default_timer()
    for i in range(m+1):
        A = np.zeros((4, n), dtype=np.int8)
        A = A.flatten()
        A[0:i] = 1
        print('-----')
        for p in multiset_permutations(A):
            A = np.reshape(p, (4, -1))
            if game.validate_state(A):
                val = game.goal_func(list(A))
                if val > best_val:
                    best_val = val
                    best_state = A
        print(A)
        print(best_state, best_val)
        stop = timeit.default_timer()
        exec_time = str(datetime.timedelta(seconds=stop-start))
        print('Execution time:', exec_time)
    print('--------------------')
    print(best_state, best_val)
    stop = timeit.default_timer()
    exec_time = str(datetime.timedelta(seconds=stop-start))
    print('Execution time:', exec_time)
        
if __name__ == "__main__":
    main()
