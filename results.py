from matplotlib import pyplot as plt

def main():
    experiment_type = 'pm'
    experiment_number = 22
    n = 5
    scores = []
    x = []
    nums = list(range(1, 21))
    nums.insert(0, 21)
    for number in nums:#range(1, experiment_number + 1):
        # x.append(number)
        if number == 21: x.append(0.01)
        else: x.append((number)/20)
        with open('results/{}{}_result.txt'.format(experiment_type, number + n * 1000), 'r') as file:
            score = file.readlines()[4].replace('# Score: ', '').replace('\n', '')
            scores.append(float(score))
    plt.plot(x, scores)
    plt.xlabel('Mutation probability')
    plt.ylabel('Score')
    plt.show()

if __name__ == "__main__":
    main()
