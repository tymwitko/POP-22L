import numpy as np

class Game:
    def __init__(self, m:int) -> None:
        self.m = m

    def create_random(self, n:int, min:int, max:int) -> bool:
        """
        creates board filled with random values from specified range
        """
        self.board = np.random.randint(min, high=max, size=(4, n))

    def validate_state(self, state:np.array):
        """
        returns True if state is valid
        """
        if sum(state.flatten()) > self.m:
            return False
        for row in range(1, self.board.shape[0]-1):
            for col in range(1, self.board.shape[1]-1):
                if state[row][col]:
                    if not self.check_one(state, row, col):
                        return False
        for row in range(1, self.board.shape[0]-1):
            for col in (0, self.board.shape[1]-1):
                if state[row][col]:
                    for i in (-1, 1):
                        if state[row+i][col]:
                            return False
        for row in (0, state.shape[0]-1):
            for col in range(1, self.board.shape[1]-1):
                if state[row][col]:
                    for i in (-1, 1):
                        if state[row][col+i]:
                            return False
        return True

    def check_one(self, state:np.array, row:int, col:int) -> bool:
        """
        returns True if all neighbours are empty
        """
        for i in (-1, 1):
            if state[row+i][col]:
                return False
            if state[row][col+i]:
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
