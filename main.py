from GA import run_ga

def main():
    params = {
        "m": 16,
        "n": 8,
        "mini": -10,
        "maks": 10,
        "iters": 1 * 10**5,
        "pop_size": 100,
        "pm": 0.01,
        "pc": 0.7,
        "seed_ga": 1,
        "seed_game": 2137,
        "set_seed_ga": True,
        "set_seed_game": True
    }
    filename = input("""File name to save results in 'results/' directory
(leave empty in order not to save the results)
(without extension): """)
    filename = "results/"+filename
    run_ga(params, filename)

if __name__ == "__main__":
    main()
