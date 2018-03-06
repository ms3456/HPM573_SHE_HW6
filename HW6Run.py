import HW6 as lol

#Q1
headProb = 0.5
timeSteps = 20
realizationNumber = 1000
ALPHA = 0.05

print ('The probability of getting a head is 0.5, and 20 flips/experiment, and 1000 experiments.')

myCohort = lol.Realization(id = 2, game_times = realizationNumber, head_prob = headProb)
realizationOutcomes = myCohort.simulate(timeSteps)

#estimate the prob of losing money in this game
probLoss = myCohort.get_loss_num()
print ('Problem 1')
print ('Average expected reward (dollors):', myCohort.get_ave_exp_value())
print ('The 95% t-based CI for the expected reward (dollars) is', realizationOutcomes.get_CI_exp_value(ALPHA))
print ('The probability of losing money in this game is:', realizationOutcomes.get_mean_loss_result())
#print ('The maximum reward is:', max(myCohort._expValue), "dollars, and the minimum reward is:", min(myCohort._expValue), 'dollars.')
print ('The 95% t-based CI for the probability of loss is', realizationOutcomes.get_CI_loss_result(ALPHA))



print ('Problem 2')
print('CI interpretation: if we repeat the game many times, 95% of the CIs generated from theses games (which was estimated as above) will cover the true mean of reward.')



#simulations for the owner
HEAD_PROB = 0.5    # annual probability of mortality
GAME_TIMES = 20        # simulation length
OWNER_POP_SIZE = 1000    # size of the real tries that a gambler would play
NUM_SIM_COHORTS = 1000   # number of simulated realizations used for making projections
ALPHA = 0.05

multiCohort = lol.MultiRealization(
    ids=range(NUM_SIM_COHORTS),   # [0, 1, 2 ..., NUM_SIM_COHORTS-1]
    realization_sizes=[OWNER_POP_SIZE] * NUM_SIM_COHORTS,  # [REAL_POP_SIZE, REAL_POP_SIZE, ..., REAL_POP_SIZE]
    head_probs=[HEAD_PROB]*NUM_SIM_COHORTS  # [p, p, ....]
)

multiCohort.simulate(GAME_TIMES)

myCohort = lol.Realization(id = 2, game_times = realizationNumber, head_prob = headProb)
realizationOutcomes = myCohort.simulate(timeSteps)


print ('Problem 3')
# print the expected reward
print('Average expected reward (dollars) for the owner is:', realizationOutcomes.get_ave_exp_value())
print('95% CI of average reward for the owner (dollars)', realizationOutcomes.get_CI_exp_value(ALPHA))



#simulations for the gambler
HEAD_PROB = 0.5    # annual probability of mortality
GAME_TIMES = 20        # simulation length
REAL_POP_SIZE = 10    # size of the real tries that a gambler would play
NUM_SIM_COHORTS = 100   # number of simulated realizations used for making projections
ALPHA = 0.05            # significance level

# calculating prediction interval for mean survival time
# create multiple cohorts
multiCohort = lol.MultiRealization(
    ids=range(NUM_SIM_COHORTS),   # [0, 1, 2 ..., NUM_SIM_COHORTS-1]
    realization_sizes=[REAL_POP_SIZE] * NUM_SIM_COHORTS,  # [REAL_POP_SIZE, REAL_POP_SIZE, ..., REAL_POP_SIZE]
    head_probs=[HEAD_PROB]*NUM_SIM_COHORTS  # [p, p, ....]
)
# simulate all cohorts
multiCohort.simulate(GAME_TIMES)


# print projected mean survival time (years)
print('Projected mean reward (dollars) for the gambler is:',
      multiCohort.get_overall_mean_expValue())
# print projection interval
print('95% projection interval of average reward (dollars) for the gambler is:',
      multiCohort.get_PI_mean_expValue(ALPHA))