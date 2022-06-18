from GA import run_ga
import multiprocessing as mp
import random

def main():
    # e+5 iters liczy sie ok 14 minut (troche ponad) (populacja 100; n 4)
    proc = 11 # liczba rdzeni do uzycia
    iters = 2 # ile razy ma sie policzyc (na kazdym procesorze, czyli bedzie iters * proc wynikow)
    bias = 5000 # od jakiego numeru ma zaczac nazywac pliki
    params = {
        "m": 20,
        "n": 5,
        "mini": -10,
        "maks": 10,
        "iters": 1 * 10**5,
        "pop_size": 100,
        "pm": 0.01,
        "pc": 0.7,
        "seed_ga": 32493,
        "seed_game": 2137,
        "set_seed_ga": True,
        "set_seed_game": True
    }
    params_list = []
    filename_list = []
    output_list = []
    show_board_list = []
    for i in range(1, 22):
        output_list.append(True) # if i % proc == 0 else False)
        show_board_list.append(True if i==0 else False)
        params['pm'] = i*0.05 # random.randint(1, 100_000)
        if i == 21: params['pm'] = 0.01
        params_list.append(params.copy())
        filename_list.append("results/pm{}".format(i + bias))
    with mp.Pool(proc) as pool:
        pool.starmap(run_ga, zip(params_list, filename_list, output_list, show_board_list))

if __name__ == "__main__":
    main()
