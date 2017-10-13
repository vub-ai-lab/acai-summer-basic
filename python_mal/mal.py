#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Game():
    
    def actions(self):
        pass
    
    def play(self, A):
        pass
    
    
class MatchingPennies(Game):
    
    def __init__(self, noPlayers=2):
        self.noPlayers = noPlayers
        
        if self.noPlayers == 2:
            self.payoff_matrix = [[(1, -1), (-1, 1)],
                                  [(-1, 1), (1, -1)]]

        elif self.noPlayers == 3:
            self.payoff_matrix = [[[1,0], #player 1, action 0, player 2
                                   [0,1]], #player 1, action 1, player 2
                                   [[1,0], #player 2, action 0, player 3
                                    [0,1]], #player 2, action 1, player 3
                                   [[0,1], #player 3, action 0, player 1
                                    [1,0]]] #player 3, action 1, player 1

    def actions(self):
        return [0, 1] # Heads and Tails

    def play2(self, A): #A joint action (a1, a2)
        rewards = []
        a1, a2 = A
        return (self.payoff_matrix[a1][a2])
    
    def play3(self, A): #A joint action (a1, a2, a3)
        rewards = []
        a1, a2, a3 = A
        return (self.payoff_matrix[0][a1][a2], #player 1
                self.payoff_matrix[1][a2][a3], #player 2
                self.payoff_matrix[2][a3][a1]) #plater 3

    def play(self, A):
        if self.noPlayers == 2:
            return self.play2(A)
        elif self.noPlayers == 3:
            return self.play3(A)



