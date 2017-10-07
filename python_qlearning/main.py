import random

from ice import *

EPISODES = 100000
EPSILON = 0.1
GAMMA = 0.9
LEARNING_RATE = 0.1

def argmax(l):
    """ Return the index of the maximum element of a list
    """
    return max(enumerate(l), key=lambda x:x[1])[0]

def main():
    env = Ice()
    average_cumulative_reward = 0.0

    # Q-table, 4x4 states, 4 actions per state
    qtable = [[0., 0., 0., 0.] for state in range(4*4)]

    # Loop over episodes
    for i in range(EPISODES):
        state = env.reset()
        terminate = False
        cumulative_reward = 0.0

        # Loop over time-steps
        while not terminate:
            # Compute what the greedy action for the current state is
            qvalues = qtable[state]
            greedy_action = argmax(qvalues)

            # Sometimes, the agent takes a random action, to explore the environment
            if random.random() < EPSILON:
                action = random.randrange(4)
            else:
                action = greedy_action

            # Perform the action
            next_state, reward, terminate = env.step(action)

            # Update the Q-Table
            td_error = reward + GAMMA * max(qtable[next_state]) - qtable[state][action]
            qtable[state][action] += LEARNING_RATE * td_error

            # Update statistics
            cumulative_reward += reward
            state = next_state

        # Per-episode statistics
        average_cumulative_reward *= 0.95
        average_cumulative_reward += 0.05 * cumulative_reward

        print(i, cumulative_reward, sep=',')

    # Print the value table
    for y in range(4):
        for x in range(4):
            print('%03.3f ' % max(qtable[y*4 + x]), end='')

        print()

if __name__ == '__main__':
    main()
