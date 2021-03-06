from dealing import Dealing 
from agent import AgentDecisionProcess as adp
import numpy as np

# state space = ['initialSize','remainingAmount','agentScore','partialDealerScore','dealerScore',
               # 'NoOfAces', 'twoAcesOrMore', 'reward','decision']

def agentTraining(noOfDecks,
                  sampleSpaceSearching,
                  sampleSpaceExploitation,
                  method,
                  gamma,
                  qTable=None):
    """
    Function for training an agent on a simplified version of blackjack with a 
    passive dealer.
    
    -noOfDecks is the number decks the agents trains with
    -sampleSpaceSearching specifies the 
    -sampleSpaceExploitation specifies the
    -method can be one of QL, TD, SARSA
    -gamma is the discount factor
    -qTable has None set as default, if using a q table that has already been 
     generated import the csv file and name it as "qTable[]" where the decksize
     replaces [].
     
     Example: QTable,pe, pO,pointOptimal,pointEgreedy= agentTraining(1,
                                                        50,
                                                        50,
                                                        "TD",
                                                        1,
                                                        None)
     returns the QTable, 
    """
    deckSize = noOfDecks*52
    optimalScore = 0 # winning score and losing Score
    egreedyScore = 0
    pO = [0,0,0]
    pe = [0,0,0]

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
    
    # for iterating 
    if qTable !=None:
        if type(qTable) == int:
             agent.QList = []
        else:                                          
            for trajectory in range(len(qTable)):
                agent.QList.append(qTable[trajectory])
                # for qtable, expect form: [[(trajector1)], [(initialSize,remainingAmount,agentScore,dealerScore',
                # NoOfAces,twoAcesOrMore,reward,decision),...]]
     
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
            reward = gamePlay.actionOutcome(action)
            # if gamePlay.actionOutcome(action) method executed, newround or hit method is 
            # also exectued. this inturn updates gameplay details. Hence assigned 
            # variables prior to method excecution
            stateAction = (deckSize, numRemaining,
                           agentScore,agentVisScore,
                           actualDealerScore, numOfaces,
                           criticalAce, reward,
                           action)

            if stateAction not in agent.QList and (agentScore >= actualDealerScore
                and agentScore <= gamePlay.blackJack):
                # if not a repeated state-action anywhere in my searchedSpace, save it
                exploredStateAction.append(stateAction)
                
            if gamePlay.ifGameEnd() == True:
                agent.QList.append(exploredStateAction)
                agent.QTableUpdate(method,
                                   reward,
                                   gamma)
                break

            if trajectoryNumber > sampleSpaceSearching: # optimal policy 
                if reward > 0: 
                    optimalScore += gamePlay.hitScore**2
                    pO[0] +=1 # winning points
                if reward ==0:
                    pO[1] +=1    
                if reward < 0:
                    pO[2] += 1
            
            else: # eGreedy policy 
                if reward > 0: 
                    egreedyScore += gamePlay.hitScore**2
                    pe[0] +=1 # winning points
                if reward ==0:
                    pe[1] +=1
                if reward < 0:
                    pe[2] +=1
                    
    print("Deck size = {} deck(s) using policy"
          " search method: {}".format(gamePlay.deckSize,
                                              method)) 
    
    print("The agent exploration period = {} rounds.Followed by {}"
          " rounds of exploitation".format(sampleSpaceSearching,sampleSpaceExploitation))

    print("The Agent average quadratic score per game exploration phase = {}"
          " The exploitation quadratic score per game =  {}"
          " In terms of winning and loosing against the house,"
          " the Agent wins {}% draws {}% and loses {}% on the training (explore) stage, followed by "
          " wins {}% draws {}% and loses {}% on the"
          " testing (exploitation) stage ".format((egreedyScore/sampleSpaceSearching),
                                                   (optimalScore/sampleSpaceExploitation),
                                                   np.round(pe[0]/sum(pe)*100,1 ),
                                                   np.round(pe[1]/sum(pe)*100,1 ),
                                                   np.round(pe[2]/sum(pe)*100,1 ),
                                                   np.round(pO[0]/sum(pO)*100,1 ),
                                                   np.round(pO[1]/sum(pO)*100,1 ),
                                                   np.round(pO[2]/sum(pO)*100,1 )))                   

    return agent.QList, pe, pO, egreedyScore, optimalScore