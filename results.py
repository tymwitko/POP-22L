from matplotlib import pyplot as plt

def main():
    experiment_type = 'range'
    experiment_number = 20
    n = 5
    scores = []
    x = []
    # nums = list(range(1, 21))
    # nums.insert(0, 21)
    # print(nums)
    for number in range(1, experiment_number + 1):
        x.append(number)
        # if number == 21: x.append(0.01)
        # else: x.append((number-1)/20)
        with open('results/{}{}_result.txt'.format(experiment_type, number + n * 1000), 'r') as file:
            score = file.readlines()[4].replace('# Score: ', '').replace('\n', '')
            scores.append(float(score))
    plt.plot(x, scores)
    plt.xlabel('Range of board values [-x; x]')
    plt.ylabel('Score')
    plt.show()

if __name__ == "__main__":
    main()
