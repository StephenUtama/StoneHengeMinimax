"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""
from typing import Any
from typing import List

# TODO: Adjust the type annotation as needed.
def interactive_strategy(game: Any) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)

def rough_outcome_strategy(game: Any) -> Any:
    """
    Return a move for game by picking a move which results in a state with
    the lowest rough_outcome() for the opponent.
    
    NOTE: game.rough_outcome() should do the following:
        - For a state that's over, it returns the score for the current
          player of that state.
        - For a state that's not over:
            - If there is a move that results in the current player winning,
              return 1.
            - If all moves result in states where the other player can
              immediately win, return -1.
            - Otherwise; return a number between -1 and 1 corresponding to how
              'likely' the current player will win from the current state.

        In essence: rough_outcome() will only look 1 or 2 states ahead to
        'guess' the outcome of the game, but no further. It's better than
        random, but worse than minimax.
    """
    current_state = game.current_state
    best_move = None
    best_outcome = -2 # Temporarily -- just so we can replace this easily later
    
    # Get the move that results in the lowest rough_outcome for the opponent
    for move in current_state.get_possible_moves():
        new_state = current_state.make_move(move)
        
        # We multiply the below by -1 since a state that's bad for the opponent
        # is good for us.
        guessed_score = new_state.rough_outcome() * -1
        if guessed_score > best_outcome:
            best_outcome = guessed_score
            best_move = move
    
    # Return the move that resulted in the best rough_outcome
    return best_move

# TODO: Implement a recursive version of the minimax strategy.
def recursive_minimax(game: Any) -> Any:
    """Return a square where it's worthwhile to play according to the minimax
    algorithm."""
    return game.minimax_recursive(game.current_state)[1]

# TODO: Implement an iterative version of the minimax strategy.
def iterative_minimax(game: Any) -> Any:
    curr_state = game.current_state
    s = Stack()
    s.add(TreeMinimax(curr_state))
    while not s.is_empty():
        curr = s.remove()
        if curr.children == []:
            if not game.is_over(curr.root):
                s.add(curr)
                for move in curr.root.get_possible_moves():
                    new_state = curr.root.make_move(move)
                    new_children = TreeMinimax(new_state, move)
                    curr.children.append(new_children)
                    s.add(new_children)
            else:
                curr.score = -1
        else:
            lst = [-x.score for x in curr.children]
            curr.score = max(lst)
            
    if curr.score == -1:
        return curr.children[0].move
    elif curr.score == 1:
        for children in curr.children:
            if children.score == -1:
                return children.move
            
                
    
    
    
class TreeMinimax:
    def __init__(self, root: object, move = None, score = 0) -> None:
        self.root = root
        self.children = []
        self.move = move
        self.score = score
        
class StackError(Exception):
    """Exception raised when trying to remove from an empty stack"""
    pass


class Stack:
    """Stores data following a first in, last out order. The last item to be added
    will also be the first one to be removed."""
    
    def __init__(self) -> None:
        """Creates an instance of a Stack object"""
        self.items = []
        
    def is_empty(self) -> bool:
        """Return whether this Stack contains no elements
        >>> s = Stack()
        >>> s.add(3)
        >>> s.is_empty()
        False
        """
        return len(self.items) == 0
    
    def add(self, item: object) -> None:
        """Adds an object item onto this Stack. The added object will 
        appear at the top of the Stack.
        >>> s = Stack()
        >>> s.add(3)
        >>> s.items
        [3]
        """
        self.items.append(item)
        
    def remove(self) -> Any:
        """Return the object at the top of this Stack if this Stack is not
        empty. Return an error if this Stack is already empty.
        >>> s = Stack()
        >>> s.add(3)
        >>> s.remove()
        3
        """
        if not self.is_empty():
            return self.items.pop()
        raise StackError("It's already an empty Stack")
    
    
    
    

if __name__ == "__main__":
    from python_ta import check_all

    check_all(config="a2_pyta.txt")
