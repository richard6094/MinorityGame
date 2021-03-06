#!/usr/bin/env python3
# coding: utf-8

import itertools
import random

import numpy as np


# convert a list of number into string
# for example [1,1,1] -> "111"
def list_to_str(num_list):
    return "".join(str(e) for e in num_list)


# Select best item in list. Randomly choose one when there are several best items
def max_randomly(item_list, key_function):
    if len(item_list) == 1:
        return item_list[0]
    else:
        item_list.sort(key=key_function, reverse=True)
        item_iterator = 0
        index = len(item_list) - 1
        max_value = key_function(item_list[0])
        for item in item_list:
            if key_function(item) < max_value:
                index = item_iterator
            item_iterator += 1
        return item_list[random.randint(0, index - 1)]


class StrategyTable(object):
    def __init__(self, depth=3):
        """
        :param depth: agent memory
        :return: None
        """

        string_list = [list_to_str(i) for i in itertools.product([0, 1], repeat=depth)]
        self.__strategy_table = {x: random.randint(0, 1) for x in string_list}
        self.__weight = 0

    @property
    def weight(self):
        return self.__weight

    @property
    def strategy_table(self):
        return self.__strategy_table

    # predict with a string format history input
    def predict(self, history):
        """
        :param history: past m winning groups
        :return: next decision
        """
        return self.__strategy_table[history]

    def update_weight(self, is_win):
        """
        :param is_win: boolean, Did the strategy win
        :return: adjust the weight
        """
        if is_win:
            self.__weight += 1
        else:
            self.__weight -= 1


class Agent(object):
    """
    base class for AgentWithStrategyTable
    Also, used in random simulation
    """
    def predict(self):
        return random.randint(0, 1)


class AgentWithStrategyTable(Agent):
    """
    composed with StrategyTable class
    inherited with Agent class
    """

    def __init__(self, depth=3, strategy_num=2):
        # last memory
        self.__history = None
        self.__depth = depth
        # init strategy_pool
        self.__strategy_pool = []
        self.__win_times = 0
        self.__last_choice = 0
        for x in range(strategy_num):
            self.__strategy_pool.append(StrategyTable(depth))

    @property
    def strategy_pool(self):
        return self.__strategy_pool
    @property
    def win_times(self):
        return self.__win_times

    # predict with memory, a list
    def predict(self, history):
        """
        :param history: last m winning group code, list of int
        :return:   next decision from a table which has the highest weight
        """
        history = list_to_str(history)
        if len(history) == self.__depth:
            self.__history = history
            strategy_choice = max_randomly(self.__strategy_pool, lambda x: x.weight)
            self.__last_choice = strategy_choice.predict(self.__history)
            return self.__last_choice
        else:
            raise Exception("Wrongly input agent memory")

    # result is winner room number
    # update weights of tables
    def get_winner(self, result):
        """
        :param result: the winning group of this round
        """
        for table in self.__strategy_pool:
            is_win = result == table.predict(self.__history)
            table.update_weight(is_win)
        if result == self.__last_choice:
            self.__win_times+=1


class MinorityGame(object):
    """
    a base class for minority Game
    """
    def __init__(self, agent_num, run_num):
        # agent number
        self.agent_num = agent_num
        # number of rounds
        self.run_num = run_num
        #defined the collection of agent objects
        self.agent_pool = []
        #Winning records
        self.win_history = np.zeros(run_num)

    @property
    def score_mean_std(self):
        """
        :return: the winner number mean and stdd
        """
        return self.win_history.mean(), self.win_history.std()


class MinorityGameWithRandomChoice(MinorityGame):
    """
    a Class for random choice Minority Game
    """
    def __init__(self, agent_num, run_num):
        super(MinorityGameWithRandomChoice,self).__init__(agent_num, run_num)
        for i in range(self.agent_num):
            self.agent_pool.append(Agent())

    def run_game(self):
        means = []
        stdds = []
        #run_num is the number of rounds
        for i in range(self.run_num):
            #the number of people deciding to go
            num_of_one = 0
            for agent in self.agent_pool:
                num_of_one+=agent.predict()
            #total game result
            game_result = 1 if num_of_one<self.agent_num/2 else 0
            #agents who making winning strategy
            winner_num = num_of_one if game_result == 1 else self.agent_num - num_of_one
            self.win_history[i] = winner_num
            if (i+1)%10000 == 0:
                print("%dth round"%i)
        return means,stdds

class MinorityGameWithStrategyTable(MinorityGame):
    """
    class used for run the minority game with StrategyTable
    """
    def __init__(self, agent_num, run_num, depth, *strategy_num):
        super(MinorityGameWithStrategyTable,self).__init__(agent_num, run_num)
        self.all_history = list()
        self.depth = depth
        self.strategy_num = strategy_num

        for x in range(depth):
            self.all_history.append(random.randint(0, 1))
        self.init_agents()

    def init_agents(self):
        """
        generate S tables for each agent
        if strategy_num has multiple variable, then the agent population will have
        different  strategy number for each agent
        """
        for i in range(self.agent_num):
            if i < self.agent_num // len(self.strategy_num):
                self.agent_pool.append(AgentWithStrategyTable(self.depth, self.strategy_num[0]))
            else:
                self.agent_pool.append(AgentWithStrategyTable(self.depth, self.strategy_num[1]))

    def run_game(self):
        """
        run the minority game n times
        """
        means = []
        stdds = []
        #run_num rounds
        for i in range(self.run_num):
            num_of_ones = 0
            record_number = 0
            for agent in self.agent_pool:
                predict_temp  = agent.predict(self.all_history[-self.depth:])
                num_of_ones += predict_temp
            game_result = 1 if num_of_ones < self.agent_num / 2 else 0
            for agent in self.agent_pool:
                agent.get_winner(game_result)  #update each agent's strategies
            winner_num = num_of_ones if game_result == 1 else self.agent_num - num_of_ones
            self.win_history[i] = winner_num
            self.all_history.append(game_result)
            if (i+1)%10000 == 0:
                means.append(self.win_history[:i].mean())
                stdds.append(self.win_history[:i].std())
                record_number+=1
                print("%dth round"%i)
        return means,stdds


    def winner_for_diff_group(self):
        mid = len(self.agent_pool)/len(self.strategy_num)
        first_part = 0
        second_part = 0
        index = 0
        for agent in self.agent_pool:
            if index<mid:
                first_part+=agent.win_times
            else:
                second_part+=agent.win_times
            index +=1

        return first_part,second_part
if __name__ == "__main__":
    m = MinorityGameWithStrategyTable(201, 500, 3, 3,5)
    m.run_game()
    print(m.winner_for_diff_group())
