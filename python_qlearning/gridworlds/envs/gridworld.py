import numpy as np

import gym
from gym import error, spaces, utils
from gym.envs.toy_text import discrete

""" n x n gridworld
""" 

# windy gridworld experiment

MAP = [
    "+-------+",
    "| : : :*|",
    "| :c: :c|",
    "| : :r:c|",
    "|x:c:c:c|",
    "+-------+"]
nR, nC = 4, 4

# MAP = [
#       "+-------------------------------------+",
#       "|*: : : : : : : : :x: : : : : : : : :*|",
#       "+-------------------------------------+",]
# nR, nC = 1, 19

# MAP = [
#       "+-----------------------------+",
#       "|*: : : : : : :x: : : : : : :*|",
#       "+-----------------------------+",]
# nR, nC = 1, 15

# MAP = [
#     "+-----------------------+",
#     "|c: : : : : : : : : : : |",
#     "| : : : : : : : : : : : |",
#     "| : : : : : : : : : : : |",
#     "|x:c:c:c:c:c:c:c:c:c:c:*|",
#     "+-----------------------+",]

# MAP = [
#     "+-----------------------+",
#     "|c:c:c:c:c:c:c:c:c:c:c:c|",
#     "| : : : : : : : : : : : |",
#     "| : : : : : : : : : : : |",
#     "|x:c:c:c:c:c:c:c:c:c:c:*|",
#     "+-----------------------+",]
# nR, nC = 4, 12

# MAP = [
#     "+-------------------+",
#     "|*:*:*:*:*:*:*:*:*:*|",
#     "|*: : : : : : : : :*|",
#     "|*: : : : : : : : :*|",
#     "|*: : : : : : : : :*|",
#     "|*: : : : :x: : : :*|",
#     "|*: : : : : : : : :*|",
#     "|*: : : : : : : : :*|",
#     "|*: : : : : : : : :*|",
#     "|*: : : : : : : : :*|",
#     "|*:*:*:*:*:*:*:*:*:*|",  
#     "+-------------------+",]
# nR, nC = 10, 10

# MAP = [
#     "+-------------------+",
#     "| : : : : : : : : : |",
#     "| : : : : : : : : : |",
#     "| : : : : : : : : : |",
#     "| : : : : : : : : : |",
#     "| : : : : : : : : : |",
#     "| : : : : : : : : : |",
#     "| :x: : : : : : : : |",
#     "| : : : : : : : : : |",
#     "| : : : : : : : : : |",
#     "| : : : : : : : : :*|",  
#     "+-------------------+",]
# nR, nC = 10, 10

DOWN, UP, RIGHT, LEFT = 0, 1, 2, 3

class GridWorld(discrete.DiscreteEnv):
  metadata = {'render.modes': ['human']}

  def __init__(self):
    self.desc = np.asarray(MAP,dtype='c')
    self.nR = nR # rows
    self.nC = nC # columns
    nS = self.nR * self.nC + 1
    self.absorbing = nS-1
    nA = 4

    self.maxR = self.nR - 1
    self.maxC = self.nC - 1
    
    self.terminal_reward, self.bump_reward, self.step_reward = 10.0, -2.0, 0.0
    self.terminal_reward, self.bump_reward, self.step_reward = None, None, 0.0
    self.up_r, self.down_r, self.left_r, self.right_r = -1.0, 1.0, -1.0, 1.0 #1.0, 10.0, 100.0, 1000.0
    

    self.bump_reward, self.up_r, self.down_r, self.left_r, self.right_r = [None] * 5
    self.terminal_reward, self.step_reward, self.cliff_reward = None, -1, -100
    self.terminal_reward, self.step_reward, self.cliff_reward = 1, 0, -1

    self.terminal_reward, self.cliff_reward = [None] * 2
    self.bump_reward, self.up_r, self.down_r = [None] * 3
    self.step_reward, self.left_r, self.right_r = 0, -1.0, 1.0

    self.bump_reward, self.up_r, self.down_r, self.left_r, self.right_r = [None] * 5
    
    self.transition_noise = 0.05
    self.terminal_reward, self.cliff_reward = 100, -10
    self.step_reward, self.treasure_reward = 0, 20


    #border_penalty = -2.0
    #self.up_r, self.down_r, self.left_r, self.right_r = border_penalty, border_penalty, border_penalty, border_penalty
 
    self.terminal_states, self.cliff_states, self.treasure_states = [], [], []
    isd = np.zeros(nS) # initial state distribution
    for state in range(nS-1):
      (row, col) = self.decode(state)
      if self.desc[row+1, 2*col+1] == b'x':
          isd[state] = 1.0
      if self.desc[row+1, 2*col+1] == b'*':
        self.terminal_states += [state]
      if self.desc[row+1, 2*col+1] == b'c':
        self.cliff_states += [state]
        self.terminal_states += [state] # this isn't standard
      if self.desc[row+1, 2*col+1] == b'r':
        self.treasure_states += [state]
        #self.terminal_states += [state]
    isd /= isd.sum()

    P = {s : {a : [] for a in range(nA)} for s in range(nS)}
    for state in range(nS):
      if state == self.absorbing:
        done = True
        reward = 0.0
        newstate = self.absorbing
        for a in range(nA):
          P[state][a].append((1.0, newstate, reward, done))
      else:
        (row, col) = self.decode(state)
        for a in range(nA):
          if state in self.terminal_states:
            newrow, newcol = None, None
            newstate = self.absorbing
          else:
            newrow, newcol = self.transition(row, col, a)
            newstate = self.encode(newrow, newcol)

          #this one is better for control:
          reward, done = self.set_reward(row, col, newstate, newstate, newrow=newrow, newcol=newcol) # state or newstate matter here
          reward, done = self.set_reward(row, col, state, state, newrow=newrow, newcol=newcol)

          P[state][a].append((1-self.transition_noise, newstate, reward, done))
          if self.transition_noise and state not in self.terminal_states:
            fakerow, fakecol = self.transition(newrow, newcol, a)
            
            while (fakerow, fakecol) != (newrow, newcol):
              newrow, newcol = fakerow, fakecol
              fakerow, fakecol = self.transition(fakerow, fakecol, a)
            
            new_slip_state = self.encode(fakerow, fakecol)
            P[state][a].append((self.transition_noise, new_slip_state, reward, done))
    
    discrete.DiscreteEnv.__init__(self, nS, nA, P, isd)

  def set_reward(self, row, col, terminal_state_check, absorbing_state_check, newrow=None, newcol=None):
    reward = self.step_reward
    done = False
    if row == self.maxR and self.down_r is not None:
      reward = self.down_r
    elif row == 0 and self.up_r is not None:
      reward = self.up_r
    if col == self.maxC and self.right_r is not None:
      reward = self.right_r
    elif col == 0 and self.left_r is not None:
      reward = self.left_r
    if newrow is not None and newcol is not None:
      if (row, col) == (newrow, newcol):
        if self.bump_reward is not None:
          reward = self.bump_reward
    if terminal_state_check in self.terminal_states: # state or newstate
      if self.terminal_reward is not None:
        reward = self.terminal_reward
      done = True
    if terminal_state_check in self.cliff_states:
      if self.cliff_reward is not None:
        reward = self.cliff_reward 
    if terminal_state_check in self.treasure_states:
      if self.treasure_reward is not None:
        reward = self.treasure_reward 
    if absorbing_state_check == self.absorbing: #vs newstate
      reward = 0.0
      done = True
    return reward, done

  def transition(self, row, col, a):
    newrow, newcol = row, col # defaults
    if a == DOWN:
      newrow = min(row + 1, self.maxR)
    elif a == UP:
      newrow = max(row - 1, 0)
    if a == RIGHT:
      newcol = min(col + 1, self.maxC)
    elif a == LEFT:
      newcol = max(col - 1, 0)
    return newrow, newcol

  def encode(self, row, col):
    i = row
    i *= self.nC
    i += col
    return i

  def decode(self, i):
    out = []
    out.append(i % self.nC)
    i = i // self.nC
    out.append(i)
    #assert 0 <= i < self.nR
    return reversed(out)

  def _render(self, mode='human', close=False):
      if close:
          return
      import sys
      outfile = StringIO() if mode == 'ansi' else sys.stdout
      out = self.desc.copy().tolist()
      out = [[c.decode('utf-8') for c in line] for line in out]
      row, col = self.decode(self.s)
      #def ul(x): return "_" if x == " " else x
      #out[1+row][2*col+1] = utils.colorize(out[1+row][2*col+1], 'green', highlight=True)

      #di, dj = self.goal
      #out[1+di][2*dj+1] = utils.colorize(out[1+di][2*dj+1], 'magenta')
      outfile.write("\n".join(["".join(row) for row in out])+"\n")
      if self.lastaction is not None:
          outfile.write("  ({})\n".format(["South", "North", "East", "West"][self.lastaction]))
      else: outfile.write("\n")

      # No need to return anything for human
      if mode != 'human':
          return outfile      