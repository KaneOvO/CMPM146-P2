
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 1000
explore_faction = 2.

def UCT(node,identityJudge):
    if identityJudge:
        UCTvalue =  node.wins / node.visits + explore_faction * (sqrt(log(node.parent.visits) / node.visits))
        return UCTvalue
    else:
        UCTvalue =  (1 - node.wins / node.visits) + explore_faction * (sqrt(log(node.parent.visits) / node.visits))
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
    #pass
    # Hint: return leaf_node

    currentNode = node#visit might be added in traverse node?? acording to section
    bestUCT = -999999
    bestNode = None
    bestAction = None
    newState = state
    identityJudge = identity == board.current_player(state)

    #while the current node still has actions that have not been performed, jump out of the loop
    while len(currentNode.untried_actions) == 0:
        #checks if nodes are 0
        if len(currentNode.child_nodes)==0: 
        #Iterate over all child nodes
            return currentNode, board.next_state(state, current_node)
        for child in currentNode.child_nodes.keys():
            childUCT = UCT(currentNode.child_nodes[child], identityJudge)

        #print(childUTC)

        #Update the current best node and uct
            if childUCT > bestUCT:
                bestUCT = childUCT
                bestAction = child
                bestNode = currentNode.child_nodes[child]

        # Set the current best node as the starting point for the next round of the loop
        currentNode = bestNode
        newState = board.next_state(state, bestAction)


    return currentNode, newState 



        

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
    if len(node.untried_actions) > 0:
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

        return newNode, nextState
    
    return node, state


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
    
    
    return state



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
        backpropagate(node.parent, won)

def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    #given state of the way it look at every posible action 
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root

        node = root_node



        # Do MCTS - This is all you!
        leafNode, newState = traverse_nodes(node, board, sampled_game, identity_of_bot)

        newLeaf, newState = expand_leaf(leafNode, board, newState)

        newState = rollout(board, newState)

        winValue = board.points_values(newState)

        backpropagate(newLeaf, winValue[identity_of_bot])
        
        #It's not done yet.
        #https://www.youtube.com/watch?v=UXW2yZndl7U 
        #The current implementation is based on this video
            
    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.

    action = None
    bestRate = -999999
    for child in node.child_nodes.keys():
        currRate = node.child_nodes[child].wins / node.child_nodes[child].visits
        
        if currRate > bestRate:
            
            bestRate = currRate
            action = child
    
    
    return action
