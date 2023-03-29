"""MultiStrategy Search in TicTacToe

Warm up thought questions 
(not graded, just to get you going)... consider referring to the slides.

a. read the documentation for count_outcomes(). What should the 
   return value be for the input state 122122011? 
 
b. what should count_outcomes() return for an input state of
   102122001?



Graded questions (answer these):

1. Given an initially empty 3x3 board, how many end games result in
   a win for X?

   131184 end games result in a win for x

2. How early can X force a win assuming O plays randomly?

    X can force a win after it has made 3 moves (so 5 moves total)

3. How early can X force a win assuming O plays the best strategy?

    X can force a win after it has made 2 moves (so 3 moves total)

"""

import sys

class TicTacToe():
    Column = 0
    Row = 1
    Diagonal = 2
    StaleMate = 3
    Chrs = {0: ' ', 1: 'X', -1: 'O'}

from collections import namedtuple

#
# NOTE:  ** Be Careful Constructing These ! **
#
#       The 'nextplayer' field must be set appropriately for the board state
#       and no verification is performed to ensure that it is valid.
#       'nextplayer' should be 1 (if the nextplayer is X) and -1 otherwise
#       Although 'nextplayer' *could* be calculated from the board contents,
#       it is explicitly maintained in the state for efficiency.
#
#       Recall that this creates the class TTTNode which behaves like
#       a tuple (the instance variable references are immutable), but
#       unlike a tuple, you can access the instance variables ("slots")
#       with names instead of indicies. Here, each instance will have
#       the three instance variable names: 'nextplayer', 'board' and 'parent'
TTTNode = namedtuple('TTTNode', ['nextplayer', 'board', 'parent'])

class MultiStrategySearch():
    def __init__(self, boardsize=3):
        self.n = boardsize
        self.n2 = boardsize**2
        
    def is_win(self, tttnode):
        """ _Part 1: Implement This Method_
        
        Use your code from TicTacToe to determine if the
        TTTNode instance represents a board in an end-game configuration. 
        Note that "tttnode" is an argument to the method here, it is 
        not an instance variable...

        For a board of size n, a win requires one player to have n tokens
        in a line (vertical, horizontal or diagonal). 

        Arguments:
         tttnode - an instance of TTTNode representing a particular node
                     in the search tree (this give you player information
                     along with the state in the search graph, which can 
                     help you improve the speed of this method). You can 
                     assume that any tttnode passed into this method
                     with encapsulate a board with self.n2 elements

        Returns:
         (TicTacToe.Column, c, player): if player wins in column c
         (TicTacToe.Row, r, player): if player wins in row r
         (TicTacToe.Diagonal, 0, player): if player wins via
           a diagonal in the upper-left corner
         (TicTacToe.Diagonal, 1, player): if player wins via a
           diagonal in the upper-right corner
         (TicTacToe.StaleMate, 0, 0): if the game is a stalemate
         False: if the outcome can't be determined yet
        """

        # only check for last player's win
        lastPlayer = tttnode.nextplayer*-1

        # since it starts i nthe upper left three times, make one call here and save as boolean 
        upperLeft = (lastPlayer == tttnode.board[0])

        #check if there is a win in the columns
        # use result of upperleft to assign which column to start on, if lastPlayer isn't in
        # upper left, no point checking it
        if upperLeft:
            i = 0
        else:
            i = 1

        while i < self.n:
            if lastPlayer == tttnode.board[i]:
                # set j to be i + n as that is the position directly right
                j = i + self.n
                cont = True

                while cont and j < self.n2:
                    #check if there is a match
                    if tttnode.board[j] == lastPlayer:
                        j = j + self.n
                    else:
                        cont = False

                #if cont is still true, then the loop exited after n matches victor declared
                if cont:
                    return (TicTacToe.Column, i, lastPlayer)
            i = i + 1

        #check if there is a win in the rows
        # use result of upperleft to assign which row to start on, if lastPlayer isn't in
        # upper left, no point checking it
        if upperLeft:
            i = 0
        else:
            i = self.n

        while i < self.n2:
            if lastPlayer == tttnode.board[i]:
                # set j to be i + n as that is the position directly below
                j = i + 1
                cont = True

                while cont and j < i + self.n:
                    #check if there is a match
                    if tttnode.board[j] == lastPlayer:
                        j = j + 1
                    else:
                        cont = False

                #if cont is still true, then the loop exited after n matches victor declared
                if cont:
                    return (TicTacToe.Row, (i//self.n), lastPlayer)
            i = i + self.n

        # check if there is a left diagonal win
        # use result of upperleft
        if upperLeft:
            # set j to be n + 1 as that is the position directly below and one square right
            j = self.n + 1
            cont = True
        
            while cont and j < self.n2:
                #check if there is a match
                if tttnode.board[j] == lastPlayer:
                    j = j + self.n + 1
                else:
                    cont = False

            #if cont is still true, then the loop exited after n matches victor declared
            if cont:
                return (TicTacToe.Diagonal, 0, lastPlayer)

        # check if there is a right diagonal win
        i = self.n - 1

        if lastPlayer == tttnode.board[i]:
        
            # set j to be i + n - 1 as that is the position directly below and one square left
            j = i + self.n - 1
            cont = True

            while cont and j < self.n2 - 1:
                #check if there is a match
                if tttnode.board[j] == lastPlayer:
                    j = j + self.n - 1
                else:
                    cont = False

            #if cont is still true, then the loop exited after n matches victor declared
            if cont:
                return (TicTacToe.Diagonal, 1, lastPlayer)

        #check if there is a stalemate, means no 0's in board
        if 0 in tttnode.board:
            #play continues
            return False
        else:
            return (TicTacToe.StaleMate, 0, 0)
  
                
    def show(self, state, stream=sys.stdout):
        """Prints a representation of the board on the specified stream."""
        
        for i in range(self.n):
            fmtstr = []
            for j in range(self.n-1):
                fmtstr.append( " %s |"%TicTacToe.Chrs[state.board[i*self.n+j]])
            fmtstr.append(" %s "%TicTacToe.Chrs[state.board[(i+1)*self.n-1]])
            line = "".join(fmtstr)
            print(line, file=stream)
            if i < self.n-1:
                print('-'*len(line), file=stream)


    def successors(self, tttnode):
        """Yield the successor nodes of the given parent node.
        
        Note that this successor function takes a TTTNode instance
        and yields TTTNode instances. These nodes don't track path/edge
        costs since we don't care about that in our search. But, they do
        maintain a reference to their parent so we can navigate the search
        tree.
        """
        for i in range(self.n**2):
            if tttnode.board[i] == 0:
                lstate = list(tttnode.board)  # create a list to manipulate
                lstate[i] = tttnode.nextplayer # fill an empty space
                
                # before we yield the successor, turn that child state back
                # into a tuple so no one can accidentally modify it...
                yield TTTNode(tttnode.nextplayer * -1,
                               tuple(lstate), tttnode)


        # recursive helper method for count outcomes
    def getOutcomeCount(self, tttnode):
        # base case: one element in tttList
        gameResult = self.is_win(tttnode)
        if(gameResult):
            # third element contains victor
            if gameResult[2] == 1:
                # X won
                return (0, 1, 0)
            elif gameResult[2] == -1:
                # O won
                return (0, 0, 1)
            else:
                # stalemate
                return (1, 0, 0)

        # recursive case: tttnode not a end state
        # want to return a tuple of victories use addtuples and 
        res = (0, 0, 0)
        for element in self.successors(tttnode):
            # sum current result count + result of all successors
            res = addtuples(res, self.getOutcomeCount(element))

        return res

                            
    def count_outcomes(self, tttnode, verbose=False):
        """ _ Part 4: Implement this method _ 

        Counts the distinct outcomes of tictactoe games.

        Hints: (1) it may be easiest to create a recursive helper method
        to do the heavy lifting. (2) you can turn a list into a tuple by
        calling tuple() with the list as an argument.

        args:
            tttnode - a TTTNode instance representing the 'initial state'
            verbose - True for debugging output

        returns:
            a tuple of (# of ties, # of X wins, # of O wins) for all possible
            games generated by starting at the initial state and playing until
            completion.
        """

        result = self.getOutcomeCount(tttnode)
        return result

        pass

    # recursive helper method for evaluate_strategies
    def generateStrategies(self, tttnode):
        # base case: terminal, so all results will be the same
        gameResult = self.is_win(tttnode)
        if(gameResult):
            moves = 10
            forceState = (0,0,0,0,0,0,0,0,0)
            # third element contains victor
            if gameResult[2] == 1:
                # X won
                result = (0, 1, 0)
                moves = 9
                forceState = tttnode.board
            elif gameResult[2] == -1:
                # O won
                result = (0, 0, 1)
            else:
                # stalemate
                result = (1, 0, 0)

            return({"BB" : result, "RB" : result, "BR" : result, "RR" : result}, moves, forceState)


        # recursive case : non terminal tttnode
        children = []

        for element in self.successors(tttnode):
            (childs, temp_xForce, temp_xForceState) = self.generateStrategies(element)
            #children.append((childs)
            children.append((childs, temp_xForce, temp_xForceState))
        
        result = {}

        # X's move
        if tttnode.nextplayer == 1:
            # assign these result value to the first one : need to compare to something
            resultBB = children[0][0]["BB"]
            resultBR = children[0][0]["BR"]

            # these can be zero they're just added
            resultRB = (0, 0, 0)
            resultRR = (0, 0, 0)

            for currentNode in children:
                resultBB = bestchoice(resultBB, currentNode[0]["BB"], 1)

                # BB X Force
                if(resultBB == currentNode[0]["BB"]):
                    xForce = currentNode[1]
                    xForceState = currentNode[2]

                resultBR = bestchoice(resultBR, currentNode[0]["BR"], 1)

                # BR X Force
                #f(resultBR == currentNode[0]["BR"]):
                #    xForce = currentNode[1]
                #    xForceState = currentNode[2]


                resultRB = addtuples(resultRB, currentNode[0]["RB"])
                resultRR = addtuples(resultRR, currentNode[0]["RR"])

            result["BB"] = resultBB
            result["BR"] = resultBR
            result["RB"] = resultRB
            result["RR"] = resultRR


            


            
            
            return (result, xForce, xForceState)
        # O's move
        else:
            # assign these result value to the first one : need to compare to something
            resultBB = children[0][0]["BB"]
            resultRB = children[0][0]["RB"]

            xForce = children[0][1]
            xForceState = children[0][2]

            # these can be zero they're just added
            resultBR = (0, 0, 0)
            resultRR = (0, 0, 0)

            for currentNode in children:
                resultBB = bestchoice(resultBB, currentNode[0]["BB"], -1)

                # BB X Force
                if(resultBB == currentNode[0]["BB"]):
                    xForce = currentNode[1]
                    xForceState = currentNode[2]


                resultRB = bestchoice(resultRB, currentNode[0]["RB"], -1)
                resultBR = addtuples(resultBR, currentNode[0]["BR"])

                # BR X Force
                if(currentNode[0]["BR"][0] == 0 and currentNode[0]["BR"][2] == 0):
                    xForce = currentNode[1]
                    xForceState = currentNode[2]
                elif currentNode[1] < xForce:
                    xForce = currentNode[1]
                    xForceState = currentNode[2]



                resultRR = addtuples(resultRR, currentNode[0]["RR"])

            result["BB"] = resultBB
            result["BR"] = resultBR
            result["RB"] = resultRB
            result["RR"] = resultRR


            #BR X Force

            c = 0
            for i in range(len(tttnode.board)):
                if tttnode.board[i] != 0:
                    c = c + 1

            #print("c:%d, xforce : %d" % (c, xForce))
            #if resultBB == (0, 1, 0) and c < xForce:

            
            if resultBR[0] == 0 and resultBR[2] == 0 and c < xForce:
                h = [0,0,0,0,0,0,0,0,0]
                xForce = c
                for i in range(len(tttnode.board)):
                    h[i] = tttnode.board[i]
                xForceState = h


            return (result, xForce, xForceState)



    def evaluate_strategies(self, tttnode, verbose=False):
        """ _ Part 5: Implement this method _ 
        
        return a dictionary representing the strategic outcome table for
        a given input state (tttnode). If verbose is False, no
        output should be generated on stdout or stderr.
        
        the dictionary should have keys 'BB', 'RB', 'BR', and 'RR'
        representing the best ('B') and random ('R') strategies
        for player 1 (X) and player 2 (O) respectively. So 'RB'
        corresponds to X playing randomly and O playing its best.
        Values of this table should be a tuple of (ties, X-wins, O-wins).

        Hint: this method may be easiest to implement recursively.
        """
        (result, xForce, xForceState) = self.generateStrategies(tttnode)

        # used for xForce values
        #d = str(xForceState)
        #print("x forced a victory after %d moves, with state %s" % (xForce, d) )

        return (result)


                    
def addtuples(t1, t2):
    """ _ Part 2: Implement this function _

    Given two tuples (of the same length) as input, 
    return a tuple that represents the element-wise sum
    of the inputs.  That is

    (out_0, ..., out_n) = (t1_0 + t2_0, ..., t1_n + t2_n)
    """
    res = list(t1)
    for i in range(len(t1)):
        res[i] = t1[i] + t2[i]

    return tuple(res)
    
    pass

def bestchoice(t1, t2, whom):
    """ _ Part 3: Implement this function _

    Given two tuples representing:
    (ties, p1-wins, p2-wins)
    
    return the 'best' choice for the player
    'whom'.

    The best choice decision is the one where
    the opponent is least likely to win. If the 
    likelihood (% wins) is insufficient to determine
    a 'best' choice, break ties by selecting the tuple
    in which the 'whom' has *won* the most games; if
    this is still insufficient, break ties further by
    selecting the tuple with the most stalemates.
    """
    # tuples are [TIES, P1, P2]
    # whom is -1 (P2); 1 (P1)

    # x's best choice
    if whom == 1:
        #check O wins
        # if O wins fewer times in t1, return t1
        if t1[2] < t2[2]:
            return t1
        # if O wins fewer times in t2, return t2
        elif t1[2] > t2[2]:
            return t2
        else:
            # tie, examine x wins
            # if X wins more times in t1, return t1
            if t1[1] > t2[1]:
                return t1
            # if X wins more times in t2, return t2
            elif t1[1] < t2[1]:
                return t2
            # tie, choose tuple with most stalemates
            else:
                if t1[0] > t2[0]:
                    return t1
                else:
                    return t2
    

    # O's best choice
    if whom == -1:
        #check X wins
        # if X wins fewer times in t1, return t1
        if t1[1] < t2[1]:
            return t1
        # if X wins fewer times in t2, return t2
        elif t1[1] > t2[1]:
            return t2
        else:
            # tie, examine O wins
            # if O wins more times in t1, return t1
            if t1[2] > t2[2]:
                return t1
            # if O wins more times in t2, return t2
            elif t1[2] < t2[2]:
                return t2
            # tie, choose tuple with most stalemates
            else:
                if t1[0] > t2[0]:
                    return t1
                else:
                    return t2
    pass
        
        
if __name__ == "__main__":
    import argparse
    import random
    parser = argparse.ArgumentParser()
    parser.add_argument("--state")
    parser.add_argument("--verbose", action='store_true')
    parser.add_argument("do_what", choices=['count', 'evaluate'])
    args = parser.parse_args()

    if args.state:
        assert len(args.state) == 9, "Expected string with 9 elements"
        
        state = [int(z) for z in args.state]
        state = [-1 if s == 2 else s for s in state]
        stateset = set(state)
        assert not stateset.issuperset(set([0,1,2])), \
            "Expected string with elements 0,1,2"
        state = tuple(state)
        assert sum(state) == 0 or sum(state) == 1, \
            "Doesn't look like moves are alternating!"
        
        if sum(state) == 1:
            nextturn = -1
        elif sum(state) == 0:
            nextturn = 1
        else:
            print("state is invalid...")
            sys.exit(1)

        if args.verbose:
            print("".join(TicTacToe.Chrs[i] for i in state[:3]))
            print("".join(TicTacToe.Chrs[i] for i in state[3:6]))
            print("".join(TicTacToe.Chrs[i] for i in state[6:]))

        t3s = TTTNode(nextturn, state, None)


        mss = MultiStrategySearch()
        mss.show(t3s)
        if args.do_what == 'evaluate':
            pm = mss.evaluate_strategies(t3s)
            for key in sorted(pm):
                print("%s:%s"%(str(key), str(pm[key])))
            
        elif args.do_what == 'count':
            wins = mss.count_outcomes(t3s, args.verbose)
            print("Wins:", wins)
                
