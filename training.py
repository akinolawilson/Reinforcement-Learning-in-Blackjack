from dealing import Dealing 
from agent import AgentDecisionProcess

def agentTraining(noOfDecks,
                  sampleSpaceSearching,
                  sampleSpaceExploitation,
                  method,
                  gamma,
                  qTable=None):
     
    deckSize = noOfDecks*52
    agentSuccessResultsSearching = [0,0,0] # win draw lose
    agentSuccessResultsExploiting = [0,0,0]
    
    for i in range(sampleSpaceSearching + sampleSpaceExploitation):
        
            gamePlay = Dealing(noOfDecks)
            gamePlay.newRound()
            gamePlay.score()
            agentDecisionProcess = AgentDecisionProcess(deckSize,
                                                        gamePlay.deck,
                                                        gamePlay.hitScore,
                                                        gamePlay.partialDealerScore,
                                                        gamePlay.aceCount,
                                                        gamePlay.aceCriticalHit,
                                                        gamma)

            exploredStatesAndAction = []
            
            if i < sampleSpaceSearching:
                
                
                while gamePlay.endOfGame() == 0: # game not finished
                                            
                    
                    e = 100 / (100 + len(exploredStatesAndAction))
                    action = agentDecisionProcess.eGreedyPolicyQTable(e, 
                                                                      deckSize,
                                                                      agentDecisionProcess.remainingDeckSize,
                                                                      agentDecisionProcess.score,
                                                                      agentDecisionProcess.dealerScore, # visible to agent
                                                                      gamePlay.dealerScore, # true cards
                                                                      agentDecisionProcess.aceCount,
                                                                      agentDecisionProcess.aces)
        
                    if action == 0: # stick
                        
                        exploredStatesAndAction.append((deckSize,
                                                        gamePlay.remainingDeckSize,
                                                        agentDecisionProcess.score,
                                                        agentDecisionProcess.dealerScore, # visible from agent
                                                        gamePlay.dealerScore, # true round score 
                                                        agentDecisionProcess.aceCount,
                                                        agentDecisionProcess.aces, # if true, we have usable ace
                                                        gamePlay.actionOutcome(action=0),
                                                        0))
                    else:
                        # dealing.actionOutcome(action=1)
                        exploredStatesAndAction.append((deckSize,
                                                        gamePlay.remainingDeckSize,
                                                        agentDecisionProcess.score,
                                                        agentDecisionProcess.dealerScore,
                                                        gamePlay.dealerScore, 
                                                        agentDecisionProcess.aceCount,
                                                        agentDecisionProcess.aces,
                                                        gamePlay.actionOutcome(action=1),
                                                        1 )) 
                                                            # action=1  this will cause dealing to 
                                                            # take a hit and recalulate score
                     
                    if gamePlay.actionOutcome(action=0) == 1:
                            agentSuccessResultsSearching[0] += 1 #win
                    elif gamePlay.actionOutcome(action=0) == 0:
                            agentSuccessResultsSearching[1] += 0 # draw
                    elif gamePlay.actionOutcome(action=0) == -1:
                            agentSuccessResultsSearching[2] -= 0 # lose
                            
                if gamePlay.endOfGame() == 1:
                
                   QList = agentDecisionProcess.QTableInColumnUpdate(method,
                                                                     exploredStatesAndAction,
                                                                     gamma)
                           
                   agentDecisionProcess = AgentDecisionProcess(deckSize,
                                                                gamePlay.deck,
                                                                gamePlay.hitScore,
                                                                gamePlay.partialDealerScore,
                                                                gamePlay.aceCount,
                                                                gamePlay.aceCriticalHit,
                                                                gamma, 
                                                                QList)

################################################################################
################################################################################
                   
            while sampleSpaceSearching <= i <(sampleSpaceSearching+sampleSpaceExploitation)-1:
                
                if gamePlay.endOfGame() == 1:
                    
                   QList = agentDecisionProcess.QTableInColumnUpdate(method,
                                                                     exploredStatesAndAction,
                                                                     gamma)
                                   
                   agentDecisionProcess = AgentDecisionProcess(deckSize,
                                                               gamePlay.deck,
                                                               gamePlay.hitScore,
                                                               gamePlay.partialDealerScore,
                                                               gamePlay.aceCount,
                                                               gamePlay.aceCriticalHit,
                                                               gamma, 
                                                               QList)
               
                   action = agentDecisionProcess.optimalPolicyQTable(deckSize,
                                                                     agentDecisionProcess.remainingDeckSize,
                                                                     agentDecisionProcess.score,
                                                                     agentDecisionProcess.dealerScore, # visible to agent
                                                                     gamePlay.dealerScore, # true cards
                                                                     agentDecisionProcess.aceCount,
                                                                     agentDecisionProcess.aces,
                                                                     QList)
                if (deckSize,
                    gamePlay.initialDeckSize,
                    agentDecisionProcess.score,
                    agentDecisionProcess.dealerScore, # visible from agent
                    gamePlay.dealerScore, # true round score 
                    agentDecisionProcess.aceCount,
                    agentDecisionProcess.aces, # if true, we have usable ace
                    gamePlay.actionOutcome(action),
                    action) not in QList and (agentDecisionProcess.score >= agentDecisionProcess.dealerScore
                    and agentDecisionProcess.score <= gamePlay.blackJack):
            
                   exploredStatesAndAction.append((deckSize,
                                                   gamePlay.initialDeckSize,
                                                   agentDecisionProcess.score,
                                                   agentDecisionProcess.dealerScore,
                                                   gamePlay.dealerScore,
                                                   agentDecisionProcess.aceCount,
                                                   agentDecisionProcess.aces,
                                                   gamePlay.actionOutcome(action),
                                                   action))
                   
                if gamePlay.actionOutcome(action=0) == 1:
                        agentSuccessResultsExploiting[0] += 1 #win
                elif gamePlay.actionOutcome(action=0) == 0:
                        agentSuccessResultsExploiting[1] += 0 # draw
                elif gamePlay.actionOutcome(action=0) == -1:
                        agentSuccessResultsExploiting[2] -= 0 # lose
                                           
                   
                   
    return agentSuccessResultsSearching, agentSuccessResultsExploiting, QList

#%%
    
s, e, q = agentTraining(2,
                  50,
                  50,
                  "QLearning",
                  0.8,
                  qTable=None)


a = agentTraining(2, 1000, "QLearning", qTable=None)
a.agentHand 
a.dealerHand
a.agentScore