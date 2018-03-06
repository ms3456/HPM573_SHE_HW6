import numpy as np
from enum import Enum
import scr.StatisticalClasses as Stat


class Flip(Enum):
    """flip results of a coin"""
    TAIL = 0
    HEAD = 1

class Game(object):
    def __init__(self, id, head_prob):
        self._id = id # a seed for the random number generator
        self._rnd = np.random
        self._rnd.seed(self._id)
        self._headProb = head_prob
        self._flipResult = Flip.TAIL
        self._trials = [] # a list to store the flip results in each game
        self._reward = -250 # reward after each game (including 20 flips in our case)


    def simulate(self, n_time_steps):
        t = 0
        while t < n_time_steps:
            if self._rnd.sample() < self._headProb:
                self._flipResult = Flip.HEAD
                self._trials.append(self._flipResult)

            else:
                self._flipResult = Flip.TAIL
                self._trials.append(self._flipResult)

            t += 1


    def get_reward(self, n_time_steps):
        i = 2

        while i <n_time_steps:
            if self._trials[i] == Flip.HEAD and self._trials[i-1] == Flip.TAIL and self._trials[i-2] == Flip.TAIL:
                self._reward += 100
            i += 1
        return self._reward


class Realization:
    def __init__(self, id, game_times, head_prob):
        self._games = [] # a list of game
        self._expValue = [] # a list of reward in each game
        self._gameTimes = game_times
        n = 1
        self._lossresult = []

        #creating games in one realization
        while n <= game_times:
            game = Game(id * game_times + n, head_prob)
            self._games.append(game)
            n += 1

    #simulations to get reward for each game
    def simulate (self, n_time_steps):
        for game in self._games:
            game.simulate(n_time_steps)
            value = game.get_reward(n_time_steps)
            if not (value is None):
                self._expValue.append(value)
            if value < 0:
                self._lossresult.append (1)
            elif value >= 0:
                self._lossresult.append (0)

        return RealizationOutcomes(self)

    def get_loss_result(self):
        return self._lossresult
    def get_exp_value(self):
        return self._expValue

    def get_ave_exp_value(self):
        return sum(self._expValue)/len(self._expValue)

    def get_loss_num(self):
        loss = 0
        for i in self._expValue:
            if i < 0:
                loss += 1
        return loss/1000




class RealizationOutcomes:
    def __init__(self, simulated_realization):
        """ extracts outcomes of a simulated realization
        :param simulated_realization: a realization after being simulated"""

        self._simulatedRealization = simulated_realization

        # summary statistics on expected reward
        self._sumStat_gameExpValue = \
            Stat.SummaryStat('Expected Value', self._simulatedRealization.get_exp_value())

        # summary statistics on loss
        self._sumStat_lossResult = \
            Stat.SummaryStat('Loss Results', self._simulatedRealization.get_loss_result())

    def get_ave_exp_value(self):
        """ returns the average expected value of games in this realization """
        return self._sumStat_gameExpValue.get_mean()

    def get_CI_exp_value(self, alpha):
        """
        :param alpha: confidence level
        :return: t-based confidence interval
        """
        return self._sumStat_gameExpValue.get_t_CI(alpha)

    def get_mean_loss_result(self):
        return self._sumStat_lossResult.get_mean()

    def get_CI_loss_result(self, alpha):
        """
        :param alpha: confidence level
        :return: t-based confidence interval
        """
        return self._sumStat_lossResult.get_t_CI(alpha)

class MultiRealization:
    """ simulates multiple realizations with different parameters """

    def __init__(self, ids, realization_sizes, head_probs):
        """
        :param ids: a list of ids for realizations to simulate
        :param realization_sizes: a list of game times that one gambler can play
        :param head_prob: a list of the probabilities of flipping the head
        """
        self._ids = ids
        self._realizationSizes = realization_sizes
        self._headProbs = head_probs

        self._expValues = []      # two dimensional list of expected reward from each simulated realization
        self._meanExpValue = []   # list of mean expected reward for each simulated realization
        self._sumStat_meanExpValue = None

    def simulate(self, n_time_steps):
        """ simulates all cohorts """

        for i in range(len(self._ids)):
            # create a realization
            realization = Realization(self._ids[i], self._realizationSizes[i], self._headProbs[i])
            # simulate the realization
            output = realization.simulate(n_time_steps)
            # store all expected reward from this realization
            self._expValues.append(realization.get_exp_value())
            # store average reward for this realization
            self._meanExpValue.append(output.get_ave_exp_value())

        # after simulating all cohorts
        # summary statistics of mean survival time
        self._sumStat_meanExpValue = Stat.SummaryStat('Mean expected value (dollars) is', self._meanExpValue)

    def get_cohort_mean_survival(self, cohort_index):
        """ returns the mean survival time of an specified cohort
        :param cohort_index: integer over [0, 1, ...] corresponding to the 1st, 2ndm ... simulated cohort
        """
        return self._meanExpValue[cohort_index]

    def get_cohort_CI_mean_survival(self, cohort_index, alpha):
        """ :returns: the confidence interval of the mean survival time for a specified cohort
        :param cohort_index: integer over [0, 1, ...] corresponding to the 1st, 2ndm ... simulated cohort
        :param alpha: significance level
        """
        st = Stat.SummaryStat('', self._expValue[cohort_index])
        return st.get_t_CI(alpha)

    def get_all_mean_expValue(self):
        " :returns a list of mean reward for all simulated realization"
        return self._meanExpValue

    def get_overall_mean_expValue(self):
        """ :returns the overall mean reward (the mean of the mean reward of all realizations)"""
        return self._sumStat_meanExpValue.get_mean()

    def get_cohort_PI_expValue(self, cohort_index, alpha):
        """ :returns: the prediction interval of the reward for a specified realization
        :param cohort_index: integer over [0, 1, ...] corresponding to the 1st, 2ndm ... simulated cohort
        :param alpha: significance level
        """
        st = Stat.SummaryStat('', self._expValue[cohort_index])
        return st.get_PI(alpha)

    def get_PI_mean_expValue(self, alpha):
        """ :returns: the prediction interval of the mean reward"""
        return self._sumStat_meanExpValue.get_PI(alpha)

