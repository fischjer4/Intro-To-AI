import sys



##################################################
#	Attempts to solve the problem using BFS search
##################################################
def executeBFS(startFO, goalFO, outputFO):
	pass


##################################################
#	Attempts to solve the problem using DFS search
##################################################
def executeDFS(startFO, goalFO, outputFO):
	pass


#################################################
#	Attempts to solve the problem using Iterative
# 	Deepening DFS search
#################################################
def executeIDDFS(startFO, goalFO, outputFO):
	pass


#################################################
#	Attempts to solve the problem using A* search
#################################################
def executeASTAR(startFO, goalFO, outputFO):
	pass


def main():
	# Get cmmd line args
	args = sys.argv
	if len(args) is not 5:
		print("Lacking four cmmd line args: < initial state file > < goal state file > < mode > < output file >")
		return

	# Open files
	try:
		startFO = open(args[1], "r")
		goalFO = open(args[2], "r")
		mode = args[3]
		outputFO = open(args[4], "w")
	except:
		print("Error on opening a file. Make sure that the file names are correct")
		return
	
	# Call respective search functions
	if(mode == "bfs"):
		executeBFS(startFO, goalFO, outputFO)
	elif(mode == "dfs"):
		executeDFS(startFO, goalFO, outputFO)
	elif(mode == "iddfs"):
		executeIDDFS(startFO, goalFO, outputFO)
	elif(mode == "astar"):
		executeASTAR(startFO, goalFO, outputFO)
	else:
		print(mode + " is an invalid mode, try bfs, dfs, iddfs, astar")

	# Close files
	startFO.close()
	goalFO.close()
	outputFO.close()

if __name__ == "__main__":
	main()