from dealing import Dealing
from agent import agentDecisionProcess



class BlackJackGamePlayTraining:

  #  visitedState = trajectory[i][:-1]
  #  exploredStateAction = trajectory[i]
    
    def __init__(self,
                 deckSize,
                 policySearchMethod,
                 trainIteration,
                 testIteration,
                 gamma):
        
        self.deckSize = len(deckSize)
        self.policySearchMethod = policySearchMethod # string: 'QLearning' or 'TemporalDifference'
        self.trainIteration = trainIteration
        self.testIteration = testIteration 
        self.gamma = gamma
 
    
    def gamePlayInitialising(self,
                             trainIteration, # random plays to generate policy; exploration
                             testIteration,  # iteration upon random plays with found policy; exploitation
                             policySearchMethod,
                             initialDeckSize):
            
        
        for i in (trainIteration + testIteration):
            
            # Games initiated are = trainIteration + testIteration
            
            dealing = Dealing(initialDeckSize) # initialising deck
            dealing.newRound() # initialising hands
            
            while i < trainIteration: # passing through trainIteration games
                
                trajectory = [] # empty place holder for history of game
                
                while dealing.endOfGame() == 0: # whilst the game (because of decksize) is not finished
 
                    trajectory = []
                    dealing.score() # calculating score
                    
                    player = agentDecisionProcess(dealing.initalDeckSize,
                                                   dealing.remainingDeckSize,
                                                   dealing.hitScore,
                                                   dealing.partialDealerScore,
                                                   dealing.aceCount,
                                                   dealing.aceCritical,  # If aceCritical True, then have two aces in hand
                                                   gamma=0.8)
                    
                    if player.actionInitiating() == 0: # stick
                        
                        reward = dealing.actionOutcome(action = 0)
                        
                        trajectory.append( player.sizeDeck,
                                           player.remainingDeck,
                                           player.score,
                                           dealing.dealerScore,
                                           player.aceCount,
                                           player.aces,
                                           reward,
                                           (0)) # stick
                        
                        player.QList.append(trajectory)
                        
                    else: # hit
                        
                        reward = dealing.actionOutcome(action = 1)
                        
                        trajectory.append(player.sizeDeck,
                                           player.remainingDeck,
                                           player.score,
                                           dealing.dealerScore,
                                           player.aceCount,
                                           player.aces,
                                           reward,
                                           (1)) # hit
                        
                        player.QList.append(trajectory)
                 
                    
                if  dealing.endOfGame() == 1: # after finished game, update qTable 
                    

                    QTable = player.QTableInColumnUpdate(self.policySearchMethod,
                                                         self.gamma)
                   
                    return QTable
                
        return trajectory        




    @classmethod                 
    def updateTrajectory(cls):
        pass 