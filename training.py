from dealing import Dealing 
from agent import AgentDecisionProcess as adp


def agentTraining(noOfDecks,
                  sampleSpaceSearching,
                  sampleSpaceExploitation,
                  method,
                  gamma,
                  qTable=None):
    

    
    deckSize = noOfDecks*52
    pointOptimal =[0,0] # winning score and losing Score
    pointEgreedy = [0,0]
    # searchSpace = []
    gamePlay = Dealing(noOfDecks)
    gamePlay.newRound()
    
    agent = adp(deckSize,
                gamePlay.deck,
                gamePlay.hitScore,
                gamePlay.partialDealerScore,
                gamePlay.dealerScore,
                gamePlay.aceCount,
                gamePlay.aceCriticalHit,
                gamma)
    
    if qTable !=None:              #
        agent.QList.append(qTable)   # QList is class variable of adp
                                                                     
    for trajectoryNumber in range(sampleSpaceSearching + sampleSpaceExploitation):
               
        exploredStateAction = []
                    
        while gamePlay.ifGameEnd() == False:    
            
            if trajectoryNumber < sampleSpaceSearching: # condition for still exploring 
        
               e = 100 / (100+len(exploredStateAction)) # as explore more, more likely to
                                                        # stick to optimal policy
               action = agent.eGreedyPolicyQTable(e, 
                                                  deckSize,
                                                  gamePlay.remainingDeckSize,
                                                  gamePlay.hitScore, # true cards
                                                  gamePlay.partialDealerScore, # visible to agent
                                                  gamePlay.dealerScore, # true cards
                                                  gamePlay.aceCount,#8
                                                  gamePlay.aceCriticalHit)#8
    
            else: # if in exploitation phase 
                action = agent.optimalPolicyQTable(deckSize,
                                                   gamePlay.remainingDeckSize,
                                                   gamePlay.hitScore,
                                                   gamePlay.partialDealerScore,#8
                                                   gamePlay.dealerScore,
                                                   gamePlay.aceCount,#8
                                                   gamePlay.aceCriticalHit)#8

            numRemaining = gamePlay.remainingDeckSize
            agentScore = gamePlay.hitScore
            agentVisScore = gamePlay.partialDealerScore
            actualDealerScore = gamePlay.dealerScore
            numOfaces = gamePlay.aceCount
            criticalAce = gamePlay.aceCriticalHit # boolean 
            ###################################################################
            reward = gamePlay.actionOutcome(action)
            # if gamePlay.actionOutcome(action) method executed, newround or hit method is 
            # also exectued. this inturn updates gameplay details. Hence assigned 
            # variables prior to method excecution
            ###################################################################
            stateAction = (deckSize, numRemaining,
                           agentScore,agentVisScore,
                           actualDealerScore, numOfaces,
                           criticalAce, reward,
                           action)

            if stateAction not in agent.QList[:] and (agentScore >= actualDealerScore
                and agentScore <= gamePlay.blackJack):
                # if not a repeated state-action anywhere in my searchedSpace, save it
                exploredStateAction.append(stateAction)
            
            agent.QList.append(exploredStateAction)
            agent.QTableUpdate(method,
                               reward,
                               gamma)
        
            if trajectoryNumber > sampleSpaceSearching: # optimal policy 
                
                if reward > 0: 
                    pointOptimal[0] += reward
                elif reward ==0:
                    pass
                elif reward < 0:
                    pointOptimal[1] += reward
            
            
            else: # eGreedy policy 
                if reward > 0: 
                    pointEgreedy[0] += reward
                elif reward ==0:
                    pass
                elif reward < 0:
                    pointEgreedy[1] += reward
                               
        if gamePlay.ifGameEnd() == True: # we update q table after each game played
            trajectoryNumber+= 1

    print("After playing for {} iterations of {} deck(s) using "
          " policy search method: {}".format(sampleSpaceSearching,
                                              gamePlay.deckSize,
                                              method)) 
    
    print("The agent explores the enviromnent for {} rounds, using the eGreedy policy"
          " and random decisions. It then play for {} rounds using the found optimal policy"
          " ".format(sampleSpaceSearching,sampleSpaceExploitation))
    
    print("The agent success measured by it's average quadratic score per game in the "
          " training stage (eGreedy Policy application) is {} and for the optimal"
          " policy application stage is {}"
          " respectively".format((pointEgreedy[0]/sampleSpaceSearching),
                                 (pointOptimal[0]/sampleSpaceExploitation)))                   
        
    return agent.QList, pointEgreedy, pointOptimal


#%%
    
q, egreedyScore, optimalScore = agentTraining(1,
                                              5000,
                                              5000,
                                              "TD",
                                              1,
                                              qTable=None)

#%%
winningScore =[]
for tra in range(len(q)):
    for traComponent in range(len(q[tra])):
        winningScore.append(q[tra][traComponent][-2])
