import numpy as np
import sys
from six import StringIO

import gym
from gym import spaces, utils
from gym.envs.toy_text import discrete

""" Four rooms. The goal is either in the 3rd room, or in a hallway adjacent to it
"""

MAP = [
    "+---------------------+",
    "| : : : : | | : : : : |",
    "| : : : : |-| : : : : |",
    "| : : : : : : : : : : |",
    "| : : : : |-| : : : : |",
    "| : : : : | | : : : : |",
    "|-| |-----| | : : : : |",
    "| : : : : | |---| |---|",
    "| : : : : | | : : : : |",
    "| : : : : |-| : : : : |",
    "| : : : : : : : : : : |",
    "| : : : : |-| : : : : |",    
    "+---------------------+",]

DOWN, UP, RIGHT, LEFT = 0, 1, 2, 3

NUM_ROOMS = 4

class FourRooms(discrete.DiscreteEnv):
  metadata = {'render.modes': ['human']}

  def __init__(self):
    self.desc = np.asarray(MAP,dtype='c')
    self.locs = [(2,5), (6,8), (9,5), (5,1)]
    self.start_room = 0

    self.nR = 11 # rows
    self.nC = 11 # columns
    self.goal = [6, 8] # in absolute coordinates
    nS = self.nR * self.nC #np.sum(np.prod(r) for r in self.room_sizes) + 4 # no absorbing state atm
    nA = 4

    maxR = self.nR-1
    maxC = self.nC-1
    isd = np.zeros(nS) # initial state distribution

    P = {s : {a : [] for a in range(nA)} for s in range(nS)}
    for row in range(self.nR):
      for col in range(self.nC):
        state = self.encode(row, col)
        if self.get_room(row, col) == self.start_room:
            isd[state] += 1
        for a in range(nA):
            # defaults
            newrow, newcol = row, col
            reward = 0.0
            done = False
            loc = (row, col)

            if a==DOWN and self.desc[row+2,2*col+1]==b" ":
              newrow = min(row+1, maxR)
            elif a==UP and self.desc[row,2*col+1]==b" ":
              newrow = max(row-1, 0)
            if a==RIGHT and self.desc[1+row,2*col+2]==b":":
              newcol = min(col+1, maxC)
            elif a==LEFT and self.desc[1+row,2*col]==b":":
              newcol = max(col-1, 0)
            
            if [row, col] == self.goal:
              reward = 1.0
              done = True

            newstate = self.encode(newrow, newcol)
            #print(newrow, newcol)
            P[state][a].append((1.0, newstate, reward, done))

    isd /= isd.sum()

    discrete.DiscreteEnv.__init__(self, nS, nA, P, isd)


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
    assert 0 <= i < self.nR
    return reversed(out)

  def get_room(self, row, col):
    if col < 5: # include hallway regions otherwise 5 here
      room = 0 if row < 5 else 3
    else:
      room = 1 if row < 6 else 2

    if (row, col) in self.locs:
      room = 4 # code for hallway location
    
    return room

  def _render(self, mode='human', close=False):
    if close:
        return
    outfile = StringIO() if mode == 'ansi' else sys.stdout
    out = self.desc.copy().tolist()
    out = [[c.decode('utf-8') for c in line] for line in out]
    row, col = self.decode(self.s)
    #def ul(x): return "_" if x == " " else x
    out[1+row][2*col+1] = utils.colorize(out[1+row][2*col+1], 'green', highlight=True)

    di, dj = self.goal
    out[1+di][2*dj+1] = utils.colorize(out[1+di][2*dj+1], 'magenta')
    outfile.write("\n".join(["".join(row) for row in out])+"\n")
    if self.lastaction is not None:
        outfile.write("  ({})\n".format(["South", "North", "East", "West"][self.lastaction]))
    else: outfile.write("\n")

    # No need to return anything for human
    if mode != 'human':
        return outfile
