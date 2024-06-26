# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    frontier = util.Stack()
    visited = []
    
    #initial state space
    startingNode=problem.getStartState()
    
    # check if current node is solution
    if problem.isGoalState(startingNode):
        return []
    
    # push the root into the frontier and depth first search the tree
    # add nodes to visited set so we don't re-visit later
    frontier.push((startingNode, []))
    while frontier.isEmpty() == 0:
        currentNode, actions = frontier.pop()

        if currentNode not in visited:
            visited.append(currentNode)

            if problem.isGoalState(currentNode):
                return actions

        for node, action, cost in problem.getSuccessors(currentNode):
            if node not in visited:
                frontier.push((node, actions + [action]))
        
    util.raiseNotDefined()



def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # define the FIFO queue
    queue = util.Queue()
    visited = []
    
    startingNode = problem.getStartState()
    
    # if problem is a solution
    if problem.isGoalState(startingNode):
        return []
    
    # push the starting node and BFS
    # add visited nodes to the visit set as needed
    queue.push((startingNode, []))
    while not queue.isEmpty():
        currentNode, actions = queue.pop()

        if currentNode not in visited:
            visited.append(currentNode)

            if problem.isGoalState(currentNode):
                return actions

            for nextNode, action, cost in problem.getSuccessors(currentNode):
                newAction = actions + [action]
                queue.push((nextNode, newAction))

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    startingNode = problem.getStartState()
    visited = []
    
    # define PQ 
    frontier = util.PriorityQueue()
    
    # the ucs frontier should consist of the state, actions to reach state, and backwards cost.
    frontier.push((startingNode, [], 0), 0)

    # do ucs
    while frontier.isEmpty() == 0:
        currentNode, actions, prevCost = frontier.pop()

        if currentNode not in visited:
            visited.append(currentNode)

            if problem.isGoalState(currentNode):
                return actions

            for nextNode, action, cost in problem.getSuccessors(currentNode):
                priority = prevCost + cost
                newAction = actions + [action]
                frontier.push((nextNode, newAction, priority), priority)
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    startingNode = problem.getStartState()
    visited = []
    
    # A* uses PQ
    frontier = util.PriorityQueue()

    if problem.isGoalState(startingNode):
        return []

    # the A* frontier should consist of the state, actions to reach state, and  backward AND forward cost.
    frontier.push((startingNode, [], 0), 0) 

    # behold A*
    while frontier.isEmpty() == 0:
        currentNode, actions, prevCost = frontier.pop()

        if currentNode not in visited:
            visited.append(currentNode)

            if problem.isGoalState(currentNode):
                return actions

            for nextNode, action, cost in problem.getSuccessors(currentNode):
                costSoFar = prevCost + cost
                newAction = actions + [action]
                heuristicCost = costSoFar + heuristic(nextNode, problem)
                frontier.push((nextNode, newAction, costSoFar), heuristicCost)



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch