import sys

# Global Vars
nodesExpanded = 0


########################################################
#	parent: 	A Node
#	state: 		A tuple array representing 
# 				[leftBank, rightBank] [[2,3,1], [1,0,0]]
#	pathCost: 	The cost to get to this node from root
#	depth:		The depth of this node
#	action:		The action done to generate this node
########################################################
class Node:
	def __init__(self, parent, state, pathCost, depth, action):
		self.parent = parent
		self.state = state
		self.pathCost = pathCost
		self.depth = depth
		self.action = action

##################################################
#	Debugging function used to print the fringe
##################################################
def printF(f):
	a = list(f)
	while a:
		print a.pop().state
	print
	print 
	
##################################################
#	Attempts to solve the problem using BFS search
#	Returns True if solution found
#	Returns False if no solution found
##################################################
def executeBFS(root, goalState, outputFO):
	closed = []
	fringe = []
	for succ in expand(root):
		fringe.insert(0, succ)
	
	while True:
		# if fringe is empty
		if not fringe:
			return False
		curNode = fringe.pop()
		if curNode.state == goalState:
			solution(curNode, outputFO)
			return True
		if curNode.state not in closed:
			global nodesExpanded
			nodesExpanded += 1
			closed.append(curNode.state)
			for succ in expand(curNode):
				fringe.insert(0, succ)

##################################################
#	Attempts to solve the problem using DFS search
##################################################
def executeDFS(root, goalState, outputFO):
	pass


#################################################
#	Attempts to solve the problem using Iterative
# 	Deepening DFS search
#################################################
def executeIDDFS(root, goalState, outputFO):
	pass


#################################################
#	Attempts to solve the problem using A* search
#################################################
def executeASTAR(root, goalState, outputFO):
	pass


#############################################################
#	Backtracks from the GOAL node to the ROOT node pushing the 
# 	reversed solution path along onto a stack. Then, prints 
# 	the soln by poping stack
#############################################################
def solution(node, outputFO):
	solutionNodes = 0
	curNode = node
	stack = list()
	# Backtrack and push steps to stack
	while curNode:
		step = ''.join(str(e) for e in curNode.state[0]) + ',' + ''.join(str(e) for e in curNode.state[1]) 
		stack.append(step)
		curNode = curNode.parent
		solutionNodes += 1

	# Print path from root to goal
	while stack:
		outputFO.write(stack.pop() + "\n")

	# -1 because we don't count the goal node
	solutionNodes -= 1

	global nodesExpanded
	outputFO.write("nodes expanded: " + str(nodesExpanded) + "\n")
	outputFO.write("nodes in solution: " + str(solutionNodes) + "\n")


#############################################################
#	Given an action and a state the function returns
#	None if the action results in an invalid state. Otherwise
#	the new state is returned.
#############################################################
def computeNextState(action, state):
	# if the boat is on the left bank
	if state[0][2]:
		newState = [[state[0][i] - action[i] for i in range(2)], [state[1][i] + action[i] for i in range(2)]]
		newState[0].append(0)	
		newState[1].append(1)
	# if the boat is on the right bank
	else:
		newState = [[state[0][i] + action[i] for i in range(2)], [state[1][i] - action[i] for i in range(2)]]
		newState[0].append(1)	
		newState[1].append(0)

	# verify positive values
	if any(n < 0 for n in newState[0]) or any(n < 0 for n in newState[1]):
		return None

	# Verify a valid state. i.e. If there are chickens on the bank. 
	# The number of wolves must be  < the number of chickens
	if (newState[0][0] > 0 and newState[0][1] > newState[0][0]) or (newState[1][0] > 0 and newState[1][1] > newState[1][0]):
		return None
	
	# Good state. Return it
	return newState
	


#############################################################
#	Given a node, a list containing [action, result] pairs
#	is returned where result is the new state after the action
# 	is applied to the node's current state.
#############################################################
def successorFN(node):
	# [chickens, wolves]
	# 1. Put one chicken in the boat
	# 2. Put two chickens in the boat
	# 3. Put one wolf in the boat
	# 4. Put one wolf and one chicken in the boat
	# 5. Put two wolves in the boat
	actions = [[1,0],[2,0], [0,1],[1,1],[0,2]]
	state = node.state

	actionResultPairs = []
	for action in actions:
		newState = computeNextState(action, state)
		if newState:
			actionResultPairs.append([action, newState])

	return actionResultPairs


#################################################
#	Expands the given node
#################################################
def expand(node):
	successors = []
	for action, result in successorFN(node):
		# pathcost of new node may need to be (node.pathCost + StepCost(newNode))
		# where StepCost() evaluates the cost. i.e. if the cost isn't uniformly 1
		newNode = Node(node, result, node.pathCost + 1, node.depth + 1, action)
		successors.append(newNode)

	return successors

#############################################################
# The start and goal files are in the following order:
# 	Left Bank: [chickens, wolves, boat] where boat is a 1 or 0
# 			   representing is on that bank or not
# 	Right Bank:[chickens, wolves, boat] where boat is a 1 or 0 
# 			   representing is on that bank or not
#############################################################
def main():
	# Get cmmd line args
	args = sys.argv
	if len(args) is not 5:
		print("Lacking four cmmd line args: < initial state file > < goal state file > < mode > < output file >")
		return
	

	# Open files
	try:
		# Start state. e.g [[3, 3, 1], [0, 0, 0]]		
		startFO = open(args[1], "r")
		startLeftBank = startFO.readline().strip('\n')
		startRightBank = startFO.readline().strip('\n')
		startState = [[int(e) for e in startLeftBank.split(',')], [int(i) for i in startRightBank.split(',')]]
		root = Node(None, startState, 0, 0, None)
		startFO.close()
		
		# Goal state. e.g [[0, 0, 0], [3, 3, 1]]
		goalFO = open(args[2], "r")
		goalLeftBank = goalFO.readline().strip('\n')
		goalRightBank = goalFO.readline().strip('\n')
		goalState = [[int(e) for e in goalLeftBank.split(',')], [int(i) for i in goalRightBank.split(',')]]
		goalFO.close()
		
		mode = args[3]
		outputFO = open(args[4], "w")
	except e:
		print e
		print("Error on opening a file. Make sure that the file names are correct")
		return
	
	# Call respective search functions
	found = True
	if(mode == "bfs"):
		found = executeBFS(root, goalState, outputFO)
	elif(mode == "dfs"):
		found = executeDFS(root, goalState, outputFO)
	elif(mode == "iddfs"):
		found = executeIDDFS(root, goalState, outputFO)
	elif(mode == "astar"):
		found = executeASTAR(root, goalState, outputFO)
	else:
		print(mode + " is an invalid mode, try bfs, dfs, iddfs, astar")
	# if no solution found
	if not found:
		outputFO.write("nodes expanded: " + str(nodesExpanded) + "\n")
		outputFO.write("no solution found" + "\n") 

	# Close file
	outputFO.close()

if __name__ == "__main__":
	main()