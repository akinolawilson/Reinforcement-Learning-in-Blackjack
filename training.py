from dealing import Dealing 
from agent import AgentDecisionProcess as adp


def agentTraining(noOfDecks,
                  sampleSpaceSearching,
                  sampleSpaceExploitation,
                  method,
                  gamma,
                  qTable=None):
    
    deckSize = noOfDecks*52
    successHistory = [0,0,0]
    
    for i in range(sampleSpaceSearching + sampleSpaceExploitation):
        
            gamePlay = Dealing(noOfDecks)
            gamePlay.newRound()
            gamePlay.score()
            agent = adp(deckSize,
                        gamePlay.deck,
                        gamePlay.hitScore,
                        gamePlay.partialDealerScore,
                        gamePlay.aceCount,
                        gamePlay.aceCriticalHit,
                        gamma)
            
            if qTable !=None:
                adp.QList.append(qTable)    

            exploredStateAction = []

            while gamePlay.ifGameEnd() == False:    
               if i < sampleSpaceSearching:                                
                    
                    e = 100 / (100 + len(exploredStateAction))
                    
                    action = agent.eGreedyPolicyQTable(e, 
                                                      deckSize,
                                                      agent.remainingDeckSize,
                                                      agent.score,
                                                      agent.dealerScore, # visible to agent
                                                      gamePlay.dealerScore, # true cards
                                                      agent.aceCount,
                                                      agent.aces)
        
               else: # if in exploitation phase 
                    action = agent.optimalPolicyQTable(deckSize,
                                                     agent.remainingDeckSize,
                                                     agent.score,
                                                     agent.dealerScore,
                                                     gamePlay.dealerScore,
                                                     agent.aceCount,
                                                     agent.aces)
                
                # expanding state space
               if (deckSize,
                   gamePlay.remainingDeckSize,
                   agent.score,
                   agent.dealerScore,
                   gamePlay.dealerScore,
                   agent.aceCount,
                   agent.aces,
                   gamePlay.actionOutcome(action),
                   action) not in adp.QList and (agent.score >= gamePlay.dealerScore
                    and agent.score <= gamePlay.blackJack):
                   
                   exploredStateAction.append((deckSize,
                                               gamePlay.remainingDeckSize,
                                               agent.score,
                                               agent.dealerScore,
                                               gamePlay.dealerScore,
                                               agent.aceCount,
                                               agent.aces,
                                               gamePlay.actionOutcome(action),
                                               action))
                   
                   adp.QList.append(exploredStateAction)
            
            reward = gamePlay.actionOutcome(action)
            
            if gamePlay.ifGameEnd() == True:
                if i < sampleSpaceSearching:
                    
                    adp.QTableUpdate(method,
                                     reward,
                                     gamma)
                    
                else:
                    if reward==1:
                        successHistory[0] += 1
                    elif reward==0:
                        successHistory[1] += 1
                    else:
                        successHistory[2] += 1
    print("After training for {} iterations of {} deck(s) using "
          " policy search method: {}".format(sampleSpaceSearching,deckSize,method)) 
    print("The agent plays for {} rounds ".format(sampleSpaceExploitation))
    print("The agents success during testing stage is win: {}, draw: {} and "
          " loss: {}".format(successHistory[0]/sampleSpaceExploitation,
                  successHistory[1]/sampleSpaceExploitation,
                  successHistory[2]/sampleSpaceExploitation))                   
        
    return adp.QList


#%%
    
q = agentTraining(1,
                  500,
                  500,
                  "QLearning",
                  0.8,
                  qTable=None)


a = agentTraining(2, 1000, "QLearning", qTable=None)
a.agentHand 
a.dealerHand
a.agentScore

