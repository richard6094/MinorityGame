import pandas as pd
from src.minority_game import  MinorityGameWithStrategyTable
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

if __name__ == "__main__":
    # set agent num
    agent_number = 201
    # set round number from 10000 to 100000
    round_number = 10000
    depth_range = range(3,11)
    strategy_number = [3,4,8,16,32,64]
    result = pd.DataFrame(columns = ["strategy_num","d","mean","std"])
    # Run the game for different round number
    i =0
    for depth in depth_range:
        for sn in strategy_number:
            mg = MinorityGameWithStrategyTable(agent_number, round_number,depth,sn)
            mg.run_game()
            mean,stdd = mg.score_mean_std
            result.loc[i] = [sn,depth,mean,stdd]
            i+=1

    g = sns.factorplot(x="d", y="mean", hue="strategy_num", data=result,
                       palette="YlGnBu_d", size=6, aspect=1.3)
    plt.xlabel('Memory Size')
    plt.ylabel('Average numbers of winners')
    g.savefig("differerentSDmean")

    g = sns.factorplot(x="d", y="std", hue="strategy_num", data=result,
                       palette="YlGnBu_d", size=6, aspect=1.3)
    plt.xlabel('Memory Size')
    plt.ylabel('winner number stdd')
    g.savefig("differerentSDstd")
