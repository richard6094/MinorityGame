# !/usr/bin/env python3
# coding: utf-8

from src.minority_game import  MinorityGameWithRandomChoice
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
if __name__ == "__main__":
    # set agent num
    agent_number = 201
    # set round number from 10000 to 100000
    round_number = range(10000,110000,10000)

    means = []
    stdds = []
    round_number = 100000

    # Run the game for different round number
    mg = MinorityGameWithRandomChoice(agent_number, round_number)
    means,stdds = mg.run_game()

    # print result
    print(means)
    print(stdds)
    # plot mean
    fig = plt.figure(figsize=(8, 4))
    plt.plot(round_number,means)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)
    fig.suptitle('Mean Value')
    plt.xlabel('Iteration number')
    plt.ylabel('Average numbers of winners')
    fig.savefig('ex3-1-mean.jpg')

    # plot SD
    fig2 = plt.figure(figsize=(8, 4))
    plt.plot(round_number,stdds)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)
    fig2.suptitle('Standard Deviation')
    plt.xlabel('Iteration number')
    plt.ylabel('Average numbers of winners')
    fig2.savefig('ex3-1-std.jpg')
