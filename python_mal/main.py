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
