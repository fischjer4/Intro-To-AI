# Uninformed and Informed Search


# Problem

In the wolves and chickens puzzle, C chickens and W wolves must cross from the right bank of a river to the left bank using a boat. The boat holds a maximum of two animals. In addition, the boat cannot cross the river by itself and must have at least one animal on board to drive it. This problem seems simple except for the following key constraint. If there are chickens present on a bank, there cannot be more wolves than chickens, otherwise the wolves will eat the chickens.

In this assignment, you will write code to solve the chickens and wolves puzzle using uninformed and informed search algorithms. The algorithms you will implement are breadth-first search, depth-first search, iterative deepening depth-first search and A-star search. Your code will print out the states along the solution path from the start state to the goal state. If no such path exists, your code must print out a no solution found message. In addition, your code must also print out the number of search nodes expanded. You will need to know this number to fill out a table comparing the different algorithms.

# File Format
The state of a game is represented by two comma-separated lines in a file. The first line stores the number of chickens, the number of wolves, and the number of boats on the left bank. The second line stores the number of chickens, the number of wolves, and the number of boats on the right bank. Since there is only one boat in the puzzle, the number of boats could be interpreted as a Boolean flag indicating the presence of the boat.

For example, the initial state

0,0,0

3,3,1

represents 3 chickens, 3 wolves and the boat being on the right bank of the river and nothing on the left bank.

Your program will take as input a starting state file and a goal state file. Your code must be able to read the start and goal state files.

Your code should take the following command line arguments: 

< initial state file > < goal state file > < mode > < output file >

The mode argument is either:

- bfs (for breadth-first search)
- dfs (for depth-first search)
- iddfs (for iterative deepening depth-first search)
- astar (for A-Star search below)

# Example Run
`python source.py testStart1.txt testGoal1.txt bfs /dev/stdout`