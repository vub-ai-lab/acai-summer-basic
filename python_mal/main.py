# Extra information on possbile approaches you can implement:
# https://ai.vub.ac.be/sites/default/files/RL%20in%20NFgames.pdf


import random

from mal import *

EPISODES = 10000
EPSILON = 0.1
GAMMA = 0.9
LEARNING_RATE = 0.1
NOAGENTS = 3

def argmax(l):
    """ Return the index of the maximum element of a list
    """
    return max(enumerate(l), key=lambda x:x[1])[0]

# After implementing your learning algorithm in the vanilla environment
# try to add additional noise for the agent payoffs
# (such that the utility is a normal distribution)

def main():
    env = MatchingPennies(NOAGENTS)
    #env = Climbing(NOAGENTS)
    
    average_cumulative_reward = [0.0 for _ in range(0,NOAGENTS)]

    # Loop over episodes
    for i in range(EPISODES):
        #YOUR CODE HERE
        print(i)

if __name__ == '__main__':
    main()
