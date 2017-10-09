import numpy as np

import gym
from gym import error, spaces, utils
from gym.utils import seeding
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
    "+---------------------+",
]

DOWN, UP, RIGHT, LEFT = 0, 1, 2, 3

NUM_ROOMS = 4

class FourRooms(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self):
    self.desc = np.asarray(MAP,dtype='c')
    self.room_sizes = [[5,5], [6,5], [4,5], [5,5]]

    self.goal = [8, 8] # in absolute coordinates
    nS = np.sum(np.prod(r) for r in self.room_sizes) + 4 # no absorbing state atm
    nA = 4

    self.nR = 11 # rows
    self.nC = 11 # columns
    maxR = nR-1
    maxC = nC-1
    isd = np.zeros(nS) # initial state distribution

    P = {s : {a : [] for a in range(nA)} for s in range(nS)}
    for row in range(nR):
      for col in range(nC):
        state = self.encode(row, col)
        if row < self.room_sizes[0][0] and col < self.room_sizes[0][1]:
            isd[state] += 1
        for a in range(nA):
            # defaults
            newrow, newcol = row, col
            reward = 0
            done = False
            taxiloc = (row, col)

            if a==0 and self.desc[row+1, 2*col] == b" ":
                newrow = min(row+1, maxR)
            elif a==1 and self.desc[row-1, 2*col] == b" ":
                newrow = max(row-1, 0)
            if a==2 and self.desc[1+row,2*col+2]==b":":
                newcol = min(col+1, maxC)
            elif a==3 and self.desc[1+row,2*col]==b":":
                newcol = max(col-1, 0)
            
            if [row, col] is self.goal:
              reward = 1.0
              done = True

            newstate = self.encode(newrow, newcol)
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


def _render(self, mode='human', close=False):
  if close:
      return
  outfile = StringIO() if mode == 'ansi' else sys.stdout
  out = self.desc.copy().tolist()
  out = [[c.decode('utf-8') for c in line] for line in out]
  row, col = self.decode(self.s)
  def ul(x): return "_" if x == " " else x

  di, dj = self.goal
  out[1+di][2*dj+1] = utils.colorize(out[1+di][2*dj+1], 'magenta')
  outfile.write("\n".join(["".join(row) for row in out])+"\n")
  if self.lastaction is not None:
      outfile.write("  ({})\n".format(["South", "North", "East", "West"][self.lastaction]))
  else: outfile.write("\n")

  # No need to return anything for human
  if mode != 'human':
      return outfile
