"""
The StoneHenge game and state classes.
"""

from game_state import GameState
from game import Game
from typing import Any
from copy import deepcopy
import random

SIZE_1 = \
"""\
      @   @
     /   /
@ - A - B
     \ / \\
  @ - C   @
       \\
        @"""

SIZE_2 = \
"""\
        @   @
       /   /
  @ - A - B   @
     / \\ / \\ /
@ - C - D - E
     \\ / \\ / \\
  @ - F - G   @
       \\   \\
        @   @"""

SIZE_3 = \
"""\
          @   @
         /   /
    @ - A - B   @
       / \\ / \\ /
  @ - C - D - E   @
     / \\ / \\ / \\ /
@ - F - G - H - I
     \\ / \\ / \\ / \\
  @ - J - K - L   @
       \\   \\   \\
        @   @   @"""

SIZE_4 = \
"""\
            @   @
           /   /
      @ - A - B   @
         / \\ / \\ /
    @ - C - D - E   @
       / \\ / \\ / \\ /
  @ - F - G - H - I   @
     / \\ / \\ / \\ / \\ /
@ - J - K - L - M - N
     \\ / \\ / \\ / \\ / \\
  @ - O - P - Q - R   @
       \\   \\   \\   \\
        @   @   @   @"""


SIZE_5 = \
"""\
              @   @
             /   /
        @ - A - B   @
           / \\ / \\ /
      @ - C - D - E   @
         / \\ / \\ / \\ /
    @ - F - G - H - I   @
       / \\ / \\ / \\ / \\ /
  @ - J - K - L - M - N   @
     / \\ / \\ / \\ / \\ / \\ /
@ - O - P - Q - R - S - T
     \\ / \\ / \\ / \\ / \\ / \\
  @ - U - V - W - X - Y   @
       \\   \\   \\   \\   \\
        @   @   @   @   @"""

GAME_TEMPLATES = {1: SIZE_1, 2: SIZE_2, 3: SIZE_3, 4: SIZE_4, 5: SIZE_5}
num_of_leylines = {1: 6, 2: 9, 3: 12, 4: 15, 5: 18}
class StoneHenge(Game):
    """
    Abstract class for a game to be played with two players.
    """

    def __init__(self, p1_starts):
        """
        Initialize this Game, using p1_starts to find who the first player is.

        :param p1_starts: A boolean representing whether Player 1 is the first
                          to make a move.
        :type p1_starts: bool
        """
        self.length = int(input("Enter a side length(1 to 5): "))
        visual = GAME_TEMPLATES[self.length].split('\n')
        self.current_state = StoneHengeState(p1_starts, visual, self.length)

    def get_instructions(self):
        """
        Return the instructions for this Game.

        :return: The instructions for this Game.
        :rtype: str
        """
        instructions = "Players take turns claiming cells." + \
            " When a player captures at least half of the cells in a ley-line" + \
            " then the player captures that layline. The first player to capture" + \
            " half of the ley-lines is the winner."
        return instructions

    def is_over(self, state):
        """
        Return whether or not this game is over.

        :return: True if the game is over, False otherwise.
        :rtype: bool
        """
        p1_sum = 0
        p2_sum = 0
        stripped = [x.strip() for x in state.visual]
        for row in stripped[2:-2]:
            if row != stripped[self.length * 2]:
                p1_sum += row[0].count('1')
                p1_sum += row[-1].count('1')
                p2_sum += row[0].count('2')
                p2_sum += row[-1].count('2')
        p1_sum += stripped[self.length*2][0].count('1')
        p2_sum += stripped[self.length*2][0].count('2')
        p1_sum += stripped[0].count('1')
        p1_sum += stripped[-1].count('1')
        p2_sum += stripped[0].count('2')
        p2_sum += stripped[-1].count('2')

        return p1_sum >= num_of_leylines[self.length] / 2 or \
               p2_sum >= num_of_leylines[self.length] / 2
    
    def get_winner(self, state):
        """
        Return whether or not this game is over.

        :return: True if the game is over, False otherwise.
        :rtype: bool
        """
        p1_sum = 0
        p2_sum = 0
        stripped = [x.strip() for x in state.visual]
        for row in stripped[2:-2]:
            if row != stripped[self.length * 2]:
                p1_sum += row[0].count('1')
                p1_sum += row[-1].count('1')
                p2_sum += row[0].count('2')
                p2_sum += row[-1].count('2')
        p1_sum += stripped[self.length*2][0].count('1')
        p2_sum += stripped[self.length*2][0].count('2')
        p1_sum += stripped[0].count('1')
        p1_sum += stripped[-1].count('1')
        p2_sum += stripped[0].count('2')
        p2_sum += stripped[-1].count('2')

        if p1_sum >= num_of_leylines[self.length] / 2:
            return "p1"
        if p2_sum >= num_of_leylines[self.length] / 2:
            return "p2"
        return False
    
    def is_winner(self, player):
        """
        Return whether player has won the game.

        Precondition: player is 'p1' or 'p2'.

        :param player: The player to check.
        :type player: str
        :return: Whether player has won or not.
        :rtype: bool
        """
        return (self.current_state.get_current_player_name() != player
                and self.is_over(self.current_state))
            
    
    def str_to_move(self, string):
        """
        Return the move that string represents. If string is not a move,
        return an invalid move.

        :param string:
        :type string:
        :return:
        :rtype:
        """
        if not string.strip().isalpha():
            return -1
        return string.strip()


    def minimax_recursive(self, state):
        self.current_state = state
        if state.get_current_player_name() == "p1": 
            best = -1
            bestMove = None
        else:
            best = 1
            bestMove = None
        if self.is_over(state) :
            if self.is_winner('p2'):
                
                return -1, None
            elif self.is_winner('p1'):
    
                return 1, None
            else:
    
                return 0, None
    
        for move in state.get_possible_moves():
    
            new_state = state.make_move(move)
    
            val, _ = self.minimax_recursive(new_state)
    
            if state.get_current_player_name() == "p1":
                if val >= best:
                    best, bestMove = val, move
                    return best, bestMove
            else:
                if val <= best:
                    best, bestMove = val, move
        return best, bestMove


class StoneHengeState(GameState):
    """
    The state of a game at a certain point in time.
    """

    def __init__(self, is_p1_turn: bool, visual: list, length: int) -> None:
        """
        Initialize this game state and set the current player based on
        is_p1_turn.
        """
        super().__init__(is_p1_turn)
        self.visual = visual
        
        if is_p1_turn:
            self.player = '1'
        else:
            self.player = '2'
            
        self.size = length
        
    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.
        """
        real_visual = '\n'.join(self.visual)
        return real_visual
        
    def is_over(self):
        """
        Return whether or not this game is over.

        :return: True if the game is over, False otherwise.
        :rtype: bool
        """
        p1_sum = 0
        p2_sum = 0
        stripped = [x.strip() for x in self.visual]
        for row in stripped[2:-2]:
            if row != stripped[self.size * 2]:
                p1_sum += row[0].count('1')
                p1_sum += row[-1].count('1')
                p2_sum += row[0].count('2')
                p2_sum += row[-1].count('2')
        p1_sum += stripped[self.size*2][0].count('1')
        p2_sum += stripped[self.size*2][0].count('2')
        p1_sum += stripped[0].count('1')
        p1_sum += stripped[-1].count('1')
        p2_sum += stripped[0].count('2')
        p2_sum += stripped[-1].count('2')

        return p1_sum >= num_of_leylines[self.size] / 2 or \
               p2_sum >= num_of_leylines[self.size] / 2
    
    def get_enemy(self):
        if self.p1_turn:
            return "p2"
        return "p1"    
    
    def get_possible_moves(self) -> list:
        """
        Return all possible moves that can be applied to this state.
        """
        moves = []
        if not self.is_over():
            for row in self.visual:
                for i in range(len(row)):
                    if row[i].isalpha():
                        moves.append(row[i])
        return moves

    def make_move(self, move: Any) -> "StoneHengeState":
        """
        Return the GameState that results from applying move to this GameState.
        """
        # lst is already in [] form with split('\n')
        lst = deepcopy(self.visual)
        for i in range(len(lst)):
            lst[i] = list(lst[i])
        for row in lst:
            for j in range(len(row)):
                if row[j] == move:
                    row[j] = self.player
        #make it so that its a nested list with the alphabets and digits to calculate @
        lst1 = []
        for row in lst[2:-2]:
            inner_list = []
            if '-' in row:
                for word in row[row.index('-'):-1]:
                    if word.isdigit() or word.isalpha():
                        inner_list.append(word)
                if row == lst[self.size * 2]:
                    inner_list.append(row[-1])
                if inner_list != []:
                    lst1.append(inner_list)
                
        #Row
        index_ = 2
        i = 0
        while i < len(lst1):
            p1 = lst1[i].count('1')
            p2 = lst1[i].count('2')
            if p1 >= len(lst1[i]) / 2 and \
                lst[index_][lst[index_].index('-') - 2] == '@':
                lst[index_][lst[index_].index('-') - 2] = '1'
            elif p2 >= len(lst1[i]) / 2 and \
                 lst[index_][lst[index_].index('-') - 2] == '@':
                lst[index_][lst[index_].index('-') - 2] = '2'
            else:
                pass
            i += 1
            index_ += 2
            
        #diagonal
        #this makes it so that each row has equal length filled with ''
        lst_dia = lst1[:]
        for row in lst_dia:
            size = len(row)
            while size < self.size + 1:
                row.append('')
                size += 1
        #this filter out so that it is in columns instead of rows and no ''
        column = []
        k = 0
        while k < self.size + 1:
            new_list = []
            for j in range(len(lst_dia) - 1):
                if lst_dia[j][k] != '':
                    new_list.append(lst_dia[j][k])
            if k>=1:
                new_list.append(lst_dia[-1][k-1])
            column.append(new_list)
            k += 1
        #now calculating and changing the @
        l = 0
        index2 = 2
        while l < len(column):
            p1_d = column[l].count('1')
            p2_d = column[l].count('2')
            if l == 0 and '@' in lst[0]:
                if p1_d >= len(column[l]) / 2 and \
                   lst[0].index('@') != len(lst[0]) - 1:
                    lst[0][lst[0].index('@')] = '1'
                elif p2_d >= len(column[l]) / 2 and \
                   lst[0].index('@') != len(lst[0]) - 1:
                    lst[0][lst[0].index('@')] = '2'
                    
            elif l == 1 and '@' in lst[0]:
                if p1_d >= len(column[l]) / 2 and \
                   lst[0][-1] == '@':
                    lst[0][-1] = '1'
                elif p2_d >= len(column[l]) / 2 and \
                   lst[0][-1] == '@':
                    lst[0][-1] = '2'
                    
            elif l > 1:
                if p1_d >= len(column[l]) / 2 and \
                   lst[index2][-1] == '@':
                    lst[index2][-1] = '1'
                elif p2_d >= len(column[l]) / 2 and \
                   lst[index2][-1] == '@':
                    lst[index2][-1] = '2'
                index2 += 2
                
            l += 1
            
        #diagonal \
        dia = []
        i = 0
        while i < self.size:
            new_list = []
            j = 0
            for row in lst1[i:self.size]:
                new_list.append(row[j])
                j += 1
            new_list.append(lst1[-1][j-1])
            dia.append(new_list)
            i += 1
            
        #last BEINT
        m = 1
        new = []
        for row in lst1[:-1]:
            new.append(row[m])
            m += 1
        dia.append(new)
        #calculating
        i = -1
        for row in dia[:-1]:
            p1_dd = row.count('1')
            p2_dd = row.count('2')
            if p1_dd >= len(row) / 2 and lst[-1][i] == '@':
                lst[-1][i] = '1'
            elif p2_dd >= len(row) / 2 and lst[-1][i] == '@':
                lst[-1][i] = '2'
            i -= 4
            
        p1_ddd = dia[-1].count('1')
        p2_ddd = dia[-1].count('2')
        if p1_ddd >= (len(dia[-1]) / 2) and lst[-3][-1] == '@':
            lst[-3][-1] = '1'
        elif p2_ddd >= (len(dia[-1]) / 2) and lst[-3][-1] == '@':
            lst[-3][-1] = '2'   

                
        for k in range(len(lst)):
            lst[k] = ''.join(lst[k])
            
        return StoneHengeState(not self.p1_turn, lst, self.size)
    
    def __repr__(self) -> str:
        """
        Return a representation of this state (which can be used for
        equality testing).
        """
        return "P1's Turn: {}".format(self.p1_turn)
                                                  
        