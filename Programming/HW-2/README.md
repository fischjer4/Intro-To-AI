# MiniMax Algorithm Used In Simplified Othello


# Requirments

You will calculate the next move for the computer player using the Minimax algorithm. Since we will be using ASCII art to display the board, we will use the symbols X (for the dark player who goes first) and O (for the light player who goes second). We will operate under the assumption that the player going first is the maximizing player and the player going second is the minimizing player.

The command line allows you to select whether a player is a human player or a computer player. We will only be grading your assignment with the human player moving first and the Minimax player moving second. Note that the 4x4 game of Othello is asymmetric; the player moving second has a serious advantage over the player moving first. In this assignment, the computer player, when going second, should always either win or tie.

The specific things you need to implement for this assignment are:
- __Utility Function__: The 4x4 version of Othello is small enough that we can generate the entire game tree while doing the Minimax search. As a result, you do not need to create an evaluation function for non-terminal nodes. You will, however, need to create a utility function that determines the "goodness" of a terminal state. You will need to create this utility function on your own. When creating the utility function, remember that the player that moves first is assumed to be the maximizing player.
- __Successor Function__: You will also need to create a successor function. This function takes the current state of the game and generates all the successors that can be reached within one move of the current state.

- __Minimax Function__: You will need to implement the Minimax-Decision, Max-Value and Min-Value functions. 

In addition to the functionality described above, you may need to implement some other code to do things like bookkeeping.

# Example Run
`make && clear && ./othello human minimax`