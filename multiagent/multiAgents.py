# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util
import math

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #if we win return bigger number for reward
        if successorGameState.isWin():
            return 5000

        score = successorGameState.getScore()
        foodList = newFood.asList()

        for food in foodList:
            nearestFood = min([manhattanDistance(food, newPos)])
            if manhattanDistance(food,newPos) != 0:
                score+=(1.0/manhattanDistance(food,newPos))
            

        for ghost in newGhostStates:
        
            # if we lost (pacman in ghost and ghost isn't 'scared'), return the opposite of win number, we've failed :(
            if ghost.scaredTimer == 0 and manhattanDistance(ghost.getPosition(), newPos) <= 1:
                return -5000
        
        
        return successorGameState.getScore() * 10.0 + (1.0 / nearestFood)

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        actions = gameState.getLegalActions(0)
        
        # Return the max of the current actions and then the best values available in the miniMax helper function I made
        # ps, i made helper functions for the next 2 questions as well
        
        return max(actions, key = lambda x: self.miniMax(gameState.generateSuccessor(0,x),1))
        
        util.raiseNotDefined()
        
    def miniMax(self, gameState, turn):
        numAgents = gameState.getNumAgents()
        agentIndex = turn % numAgents
        actions = gameState.getLegalActions(agentIndex)
        
        depth = turn/ numAgents
        
        # if depth is current depth or win/lose depth, start eval
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        # value list
        values = []
        for action in actions:
            values.append(self.miniMax(gameState.generateSuccessor(agentIndex, action), turn+1))
        
        # if the index is > 0 return the min values we have, else return the max
        if agentIndex > 0:
            return min(values)
        else:
            return max(values)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        a = -5000
        b = 5000
        values = []
        myActions = gameState.getLegalActions(0)
        

        for i in myActions:
            v = self.abSearch(gameState.generateSuccessor(0, i), 1, a, b)
            a = max(a, v)
            values.append(v)
        
        for x in range(len(values)):
            if a == values[x]:
                return myActions[x]
        
        util.raiseNotDefined()
    
    def abSearch(self, gameState, turn, a, b):
        numAgents = gameState.getNumAgents()
        agentIndex = turn % numAgents
        actions = gameState.getLegalActions(agentIndex)
        depth = turn / numAgents
        math.floor(depth)

        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        if agentIndex == 0:
            val = -5000
        else:
            val = 5000
        
        # straight from proj3 pdf basically
        for x in actions:
            s = gameState.generateSuccessor(agentIndex, x)
            if (agentIndex > 0):
                val = min(val, self.abSearch(s, turn+1, a, b))
                if val < a:
                    return val
                b = min(b, val)

            else:
                val = max(val, self.abSearch(s,turn+1,a,b))
                if val > b:
                    return val
                a = max(a, val)
        return val

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        #same as minimax
        actions = gameState.getLegalActions(0)
        return max(actions, key = lambda x: self.eMax(gameState.generateSuccessor(0,x ), 1))
        
        util.raiseNotDefined()
    
    def eMax(self, gameState, t):
        numAgents = gameState.getNumAgents()

        agentIndex = t % numAgents
        depth = t / numAgents
        math.floor(depth)

        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
    
        # List of legal actions for agent
        myActions = gameState.getLegalActions(agentIndex)

        # Heck ya, it works!
        values = []
        for action in myActions:
            values.append(self.eMax(gameState.generateSuccessor(agentIndex, action), t+1))

        if agentIndex > 0:
            return sum(values) * 1.0 / len(values) # same as minimax but witha avg!
        return max(values)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    if currentGameState.isWin():
        #print ("WIN")
        return 1000000
    if currentGameState.isLose():
        #print("LOSE")
        return -100000

    myFood = currentGameState.getFood().asList()
    pos = currentGameState.getPacmanPosition() 
    ghostStates = currentGameState.getGhostStates()

    nearestFood = min(manhattanDistance(pos, food) for food in myFood)

    for g in ghostStates:
        kill = sum([(manhattanDistance(pos, g.getPosition()) < 3)])
        scare = sum([(g.scaredTimer == 0)])

    return (currentGameState.getScore() * 10.0) + (1.0 / nearestFood) + (1.0 * kill) + (1.0 / (scare + 0.01))
    
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
