
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 1000
explore_faction = 2.

def UCT(node):
    UCTvalue =  node.wins/node.visits + explore_faction * (sqrt(log(node.parent.visits) / node.visits))
    return UCTvalue

def traverse_nodes(node, board, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """
    #paaa
    # Hint: return leaf_node

    currentNode = node
    bestUCT = -999999
    bestNode = None
    #If the current node still has actions that have not been performed, jump out of the loop
    while len(currentNode.untried_actions) == 0:
        #Iterate over all child nodes
        for childNode in currentNode.child_nodes.values():
            #If the child node is not visited, meaning that the divisor is 0,uct is infinite, return it directly
            if(childNode.visits == 0):
                return childNode
            
            #Calculate uct
            childUCT = UCT(childNode)
            
            #Update the current best node and uct
            if childUCT > bestUCT:
                bestUCT = childUCT
                bestNode = childNode
        ## Set the current best node as the starting point for the next round of the loop
        currentNode = bestNode

    return currentNode      
    

        

def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.

    """
    #pass
    # Hint: return new_node

    #Expand only if child nodes have been visited
    if node.visits != 0:
        #The action taken from the parent node that transitions the state to this node.
        parentAction = node.untried_actions.pop()
        #New state after action
        nextState = board.next_state(state, parentAction)
        #List of actions for a new node
        actionList = board.legal_actions(nextState)

        #Creating a new node
        newNode = MCTSNode(node, parentAction, actionList)
        #set as a child node
        node.child_nodes[parentAction] = newNode

        return newNode
    
    return node
    

def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    #pass

    #If the current state of the game is not over
    while board.is_ended(state) == False:
        #Perform a random act
        randomAction = choice(board.legal_actions(state))
        #Update state
        state = board.next_state(state, randomAction)
    
    #
    return board.points_values(state)



def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    #pass

    #Update the number of visits and wins for the current node
    node.visits += 1
    node.wins += won

    #Recursively update the parent node if it exists
    if node.parent:
        backpropagate(node.parent, node.parent.wins)

def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        # Do MCTS - This is all you!
        leaf_node = traverse_nodes(node, board, sampled_game, identity_of_bot)

        #It's not done yet.
        #https://www.youtube.com/watch?v=UXW2yZndl7U 
        #The current implementation is based on this video
            
    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    
    
    return None
