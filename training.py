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
    
    gamePlay = Dealing(noOfDecks)
    gamePlay.newRound()
    gamePlay.score()

    agent = adp(deckSize,
                gamePlay.deck,
                gamePlay.hitScore,
                gamePlay.partialDealerScore,
                gamePlay.dealerScore,
                gamePlay.aceCount,
                gamePlay.aceCriticalHit,
                gamma)
    
    if qTable !=None:              #
        adp.QList.append(qTable)   # QList is class variable of adp
                                   #
 
    for i in range(sampleSpaceSearching + sampleSpaceExploitation):
        

            

            
            exploredStateAction = []
            while gamePlay.ifGameEnd() == False:    
                
                if i < sampleSpaceSearching:
                   
                   e = 100 / (100+len(exploredStateAction)) # as explore more, more likely to
                                                            # stick to optimal policy
                   action = agent.eGreedyPolicyQTable(e, 
                                                      deckSize,
                                                      gamePlay.remainingDeckSize,
                                                      gamePlay.hitScore, # true cards
                                                      agent.dealerScore, # visible to agent
                                                      gamePlay.dealerScore, # true cards
                                                      agent.aceCount,
                                                      agent.aces)
        
                else: # if in exploitation phase 
                    action = agent.optimalPolicyQTable(deckSize,
                                                       gamePlay.remainingDeckSize,
                                                       gamePlay.hitScore,
                                                       agent.dealerScore,
                                                       gamePlay.dealerScore,
                                                       agent.aceCount,
                                                       agent.aces)
                
                # expanding state space, if we have not explored this state and it is
                # indeed a wining state, we add it to our state space
                stateAction = (deckSize, gamePlay.remainingDeckSize,
                               gamePlay.hitScore, agent.dealerScore,
                               gamePlay.dealerScore, agent.aceCount,
                               agent.aces, gamePlay.actionOutcome(action),
                               action)
                
                if stateAction not in adp.QList and (agent.score >= gamePlay.dealerScore
                    and agent.score <= gamePlay.blackJack):
                        
                        exploredStateAction.append((deckSize,
                                                   agent.remainingDeckSize,
                                                   gamePlay.hitScore,
                                                   agent.dealerScore,
                                                   gamePlay.dealerScore,
                                                   agent.aceCount,
                                                   agent.aces,
                                                   gamePlay.actionOutcome(action),
                                                   action))
                   
                adp.QList.append(exploredStateAction)
            
                reward = gamePlay.actionOutcome(action)
                    
                if reward>=1:
                    successHistory[0] += 1
                elif reward==0:
                    successHistory[1] += 1
                elif reward <=-1:
                    successHistory[2] += 1
                                    
            if gamePlay.ifGameEnd() == True:
                
                if i < sampleSpaceSearching:
                    
                    adp.QTableUpdate(method,
                                     reward,
                                     gamma)
                    
        # counting wins, draws and lost games 

                
                
                
    print("After training for {} iterations of {} deck(s) using "
          " policy search method: {}".format(sampleSpaceSearching,deckSize,method)) 
    
    print("The agent plays for {} rounds ".format(sampleSpaceExploitation))
    
    print("The agents success during testing stage is win: {}, draw: {} and "
          " loss: {}".format(successHistory[0]/sampleSpaceExploitation,
                  successHistory[1]/sampleSpaceExploitation,
                  successHistory[2]/sampleSpaceExploitation))                   
        
    return adp.QList


#%%
    
q = agentTraining(2,
                  500,
                  500,
                  "QLearning",
                  0.8,
                  qTable=None)

#%%

q = agentTraining(1,
                  500,
                  500,
                  "QLearning",
                  0.8)

#%%
b = [x for x in a if x[[:][3]]==18]
