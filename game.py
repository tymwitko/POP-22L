import numpy as np

class Game:
    def __init__(self, m:int, set_seed:bool=False, seed:int=2137) -> None:
        if set_seed:
            np.random.seed(seed)
        self.m = m

    def create_random_board(self, n:int, min:int, max:int) -> bool:
        """
        creates board filled with random values from specified range
        """
        self.board = np.random.randint(min, high=max, size=(4, n))

    def save_board_to_file(self, filename:str) -> bool:
        board_str = [str(elem)+'\n' for elem in list(self.board.flatten())]
        try:
            with open(filename, 'w') as file:
                file.writelines(board_str)
        except:
            return False
        return True

    def read_board_from_file(self, flename:str) -> bool:
        try:
            with open(flename, 'r') as file:
                lines = file.readlines()
            lines = [int(line) for line in lines]
            self.board = np.reshape(lines, (4, -1))
        except:
            return False
        return True

    def validate_state(self, state:np.array) -> bool:
        """
        returns True if state is valid
        """
        if state.sum() > self.m:
            return False
        for row in range(1, state.shape[0]):
            for col in range(1, state.shape[1]):
                if state[row][col]:
                    if state[row-1][col]:
                        return False
                    if state[row][col-1]:
                        return False
        for row in range(1, state.shape[0]):
            if state[row][0] and state[row-1][0]:
                return False
        for col in range(1, state.shape[1]):
            if state[0][col] and state[0][col-1]:
                return False
        return True

    def goal_func(self, state:list) -> int:
        state = np.array(state)
        state = np.reshape(state, (4, -1))
        if self.validate_state(state):
            return np.dot(state.flatten(), self.board.flatten())
        else:
            return -np.inf

def main():
    for _ in range(100_000):
        m = 100
        n = 100
        game = Game(m)
        game.create_random(n, 0, 10)
        state = np.random.randint(0, high=2, size=(1, 4*n))
        state = list(state.flatten())
        game.goal_func(state)

if __name__ == "__main__":
    main()
