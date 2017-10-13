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
        a1, a2 = A
        return (self.payoff_matrix[a1][a2])
    
    def play3(self, A): #A joint action (a1, a2, a3)
        a1, a2, a3 = A
        return (self.payoff_matrix[0][a1][a2], #player 1
                self.payoff_matrix[1][a2][a3], #player 2
                self.payoff_matrix[2][a3][a1]) #plater 3

    def play(self, A):
        if self.noPlayers == 2:
            return self.play2(A)
        elif self.noPlayers == 3:
            return self.play3(A)

class Climbing(Game):
    def __init__(self, noPlayers=2):
        self.noPlayers = noPlayers
        
        self.payoff_matrix = [[11, -30, 0],
                              [-30, 7, 0],
                              [0, 6, 5]]

    def actions(self):
        return [0, 1, 2] # Action a, b, c

    def play2(self, A): #A joint action (a1, a2)
        a1, a2 = A
        r = self.payoff_matrix[a1][a2]
        return (r,r)

    def play3(self, A): #A joint action (a1, a2, a3)
        a1, a2, a3 = A
        r12 = self.payoff_matrix[a1][a2]
        r13 = self.payoff_matrix[a1][a3]
        r23 = self.payoff_matrix[a2][a3]
        r21 = self.payoff_matrix[a2][a1]
        r31 = self.payoff_matrix[a3][a1]
        r32 = self.payoff_matrix[a3][a2]
        return (0.5*(r12 + r13), #player 1
                0.5*(r21 + r23), #player 2
                0.5*(r31 + r32)) #plater 3

    def play(self, A):
        if self.noPlayers == 2:
            return self.play2(A)
        elif self.noPlayers == 3:
            return self.play3(A)




