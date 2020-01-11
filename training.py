from dealing import Dealing 
from agent import AgentDecisionProcess as adp


def agentTraining(noOfDecks,
                  sampleSpaceSearching,
                  sampleSpaceExploitation,
                  method,
                  gamma,
                  qTable=None):
    

    
    deckSize = noOfDecks*52
    points = [0,0] # winning score and losing Score
    #qtableHistory = []
    

    
    if qTable !=None:              #
        agent.QList.append(qTable)   # QList is class variable of adp
                                                                     
    for trajectoryNumber in range(sampleSpaceSearching + sampleSpaceExploitation):
        
        gamePlay = Dealing(noOfDecks)
        #gamePlay.newRound()            
        agent = adp(deckSize,
                    gamePlay.deck,
                    gamePlay.hitScore,
                    gamePlay.partialDealerScore,
                    gamePlay.dealerScore,
                    gamePlay.aceCount,
                    gamePlay.aceCriticalHit,
                    gamma)
            
        exploredStateAction = []
                    
        while gamePlay.ifGameEnd() == False:    
            
            if trajectoryNumber < sampleSpaceSearching:
               
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
#                if gamePlay.hitRound == False:
            stateAction = (deckSize, gamePlay.remainingDeckSize,
                           gamePlay.hitScore, agent.dealerScore,
                           gamePlay.dealerScore, agent.aceCount,
                           agent.aces, gamePlay.actionOutcome(action),
                           action)
            

            if stateAction not in adp.QList and (agent.score >= gamePlay.dealerScore
                and agent.score <= gamePlay.blackJack):
                
                exploredStateAction.append(stateAction)
            
            
            agent.QList.append(exploredStateAction)
            reward = gamePlay.actionOutcome(action)
            
            if trajectoryNumber > sampleSpaceSearching:
                
                if reward > 0: 
                    points[0] += reward
                elif reward ==0:
                    pass
                elif reward < 0:
                    points[-1] -= reward 
                
        if gamePlay.ifGameEnd() == True: # we update q table after each game played
            #if trajectoryNumber < sampleSpaceSearching:
            agent.QTableUpdate(method,
                               reward,
                               gamma)
    
    print("After playing for {} iterations of {} deck(s) using "
          " policy search method: {}".format(sampleSpaceSearching,gamePlay.deckSize,method)) 
    
    print("The agent exploits the enviromnent knowledge and plays for {} rounds ".format(sampleSpaceExploitation))
    
    print("The agent success measured by their avg winning and loosing"
          " quadratic score per game is {} and {}"
          " respectively".format((points[0]/sampleSpaceExploitation),(points[1]/sampleSpaceExploitation)))                   
        
    return agent.QList  # , objectiveScore


#%%
    
q = agentTraining(2,
                   50,
                   50,
                  "QL",
                   0.8,
                   qTable=None)

#%%

q = agentTraining(1,
                  500,
                  500,
                  "QL",
                  0.8)

#%%
b = [x for x in a if x[[:][3]]==18]
