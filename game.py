from os import stat
import numpy as np

class Game:
    def __init__(self, m:int) -> None:
        self.m = m

    def create_random(self, n:int, min:int, max:int) -> bool:
        self.board = np.random.randint(min, high=max, size=(4, n))

    def validate_state(self, state:np.array):
        for row in range(1, self.board.shape[0]-1):
            for col in range(1, self.board.shape[1]-1):
                if state[row][col]:
                    if not self.check_one(state, row, col):
                        return False
        for col in range(1, self.board.shape[0]-1):
            for row in (0, state.shape[0]-1):
                if state[row][col]:
                    for i in (-1, 1):
                        if state[row+i][col]:
                            return False
        for col in range(1, self.board.shape[1]-1):
            for row in (0, state.shape[1]-1):
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

def main():
    game = Game(19)
    game.create_random(4, 0, 10)
    print(game.board)
    print(game.board.size)
    print(game.board.shape)
    state = [[0, 1, 0, 0], [1, 0, 0, 1], [0, 1, 0, 0], [1, 0, 0, 1]]
    state = np.array(state)
    print(state)
    print(game.validate_state(state))

if __name__ == "__main__":
    main()
