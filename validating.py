import dealing as Dealing
import numpy as np 
import matplotlib.pyplot as plt
import time 
import random

def actionInitiating():
    
    if random.random() <= 0.5:
        return 0 # stick
    else:
        return 1 # hitmebaby
 
def optimalDecision(state, QTable, stateSpaceChosen):
    '''
    Returns optimal decision given state. Arguments are state of agent, -tuple-,
    QTable for relavent game size, and state space parameters to be inferred from.
    E.g. params to be infered from could be 
    ['initialSize','remainingAmount','agentScore'], NOTE: DONT INCLUDED REWARD and 
    DECISION, will be appended bellow.
    
    
    
    '''
    
    parameterSpace = ['initialSize','remainingAmount','agentScore','partialDealerScore','dealerScore',
                      'NoOfAces', 'twoAcesOrMore', 'reward','decision']
    
    stateSpaceChosen.append( 'reward')
    stateSpaceChosen.append('decision')  
    paramsIndices =[]
    # retrieve indices of parameters that will be used for hitting and sticking 
    for chosenParams in stateSpaceChosen:
        paramsIndices.append(parameterSpace.index(chosenParams))
      
    
    qHit, qStick = 0,0
    qHitList, qStickList = [],[]
    
    numberOfParams = len(paramsIndices)-2  # -2 because last two elements are decision and reward
    numOfParamsRange = np.arange(0,numberOfParams+1,1)
    # Reducing the QTable content to match that of the specified parameters to be used 
    # for the agent to infer from. 
    for trajectory in range(len(QTable)):
        for stateAction in range(len(QTable[trajectory])):
            
            state = list(QTable[trajectory][stateAction])
            stateReduced = [state[params] for params in paramsIndices]
            
            stateReducedTuple = tuple(stateReduced)
            QTable[trajectory][stateAction] = stateReducedTuple
    #############################################################################
    stateSpaceChosen.append( 'reward')
    stateSpaceChosen.append('decision')
    # Comparing current state to QTable and finding optimal decision 

    for trajectory in range(len(QTable)):
        for attemptedStateAction in range(len(QTable[trajectory])):
            
            try:
                for i in numOfParamsRange:
                    hitState = [state for state in QTable[trajectory][attemptedStateAction][i] == state[i]
                    and QTable[trajectory][attemptedStateAction][numberOfParams+2] == 1] #hit
                    qHitList.append( hitState[-1] )
                    
                    stickState = [state for state in QTable[trajectory][attemptedStateAction][i] == state[i]
                    and QTable[trajectory][attemptedStateAction][numberOfParams+2] == 0] # stick
                    qStickList.append( stickState[-1] )
            except IndexError:
                pass      
    try:
        qHit = max(qHitList)
    except ValueError:
        qHit= 0
    try:
        qStick = max(qStickList)        
    except ValueError: 
        qStick = 0 
    if qHit > qStick:
        return 1
    if qHit < qStick:
        return 0
   # else:
   #     return actionInitiating()
    
#%%

[item for item in a if item[0] == 1]



[hitState for hitState in QTable[trajectory][attemptedStateAction][i] == hitState[i]
 and QTable[trajectory][attemptedStateAction][numberOfParams+2] == 1]




#%%
state = (52, 40, 12, 8, 10, 0, False, 2435.19250589688, 0)
stateWithOut = (52, 12, 8)

#%%
decision = optimalDecision(stateWithOut, q, ['initialSize','agentScore','partialDealerScore'])
    
#%%    
def game(multipleOfDeck, Qtable,  secondCardVisibility=True):
    '''
    set to false for other game style
    '''
    game = Dealing
    game(multipleOfDeck)
    game.newRound()
    print("The Agent's first hand is {}".format(game.agentHand))
    print("The Dealers's first hand is {}".format(game.DealerHand))
    print(' The agent will now base its actions on the learnt optimal'
          " policy. The game will be repeat three times and the score in terms"
          " of the quadratic score and wins losses an draws  for each game will"
          " be printed.")
    runningScore, runningSucess  = [0,0,0],[0,0,0]
    
    agentState =(multipleOfDeck*52,
                Dealing.remainingDeckSize,
                Dealing.hitScore,
                Dealing.partialDealerScore,#8
                Dealing.dealerScore,
                Dealing.aceCount,#8
                Dealing.aceCriticalHit)
    
    signal = Dealing.actionOutcome(optimalDecision(agentState))
    time.sleep(0.5)
    if float(signal) > 0:
         print("First round won")
         runningScore[0] +=1
         runningSucess[0] +=1
    elif float(signal) < 0 :
         print("First round lost")
         runningScore[1] +=1
         runningSucess[1] +=1
    else:
         runningScore[3] +=1
         runningSucess[3] +=1
         
     
    for i in range(3):
        while Dealing.ifGameEnd() == False:
                if float(signal) > 0:
                     runningScore[0] +=1
                     runningSucess[0] +=1
                elif float(signal) < 0 :
                     runningScore[1] +=1
                     runningSucess[1] +=1
                else:
                     runningScore[3] +=1
                     runningSucess[3] +=1
                agentState =(multipleOfDeck*52,
                              Dealing.remainingDeckSize,
                              Dealing.hitScore,
                              Dealing.partialDealerScore,#8
                              Dealing.dealerScore,
                              Dealing.aceCount,#8
                              Dealing.aceCriticalHit)
            
                Dealing.actionOutcome(optimalDecision(agentState))   
    
                if Dealing.ifGameEnd() == True:
                    print("The wins, losses and draws are {},{} and {} "
                        "respectively".format(runningSucess[0]/sum(runningSucess)),
                                              runningSucess[1]/sum(runningSucess),
                                              runningSucess[2]/sum(runningSucess))
                    time.sleep(3)
                    break
          
    

#%%
stateSpaceChosen = ['initialSize','remainingAmount','agentScore', 'reward','decision']
parameterSpace = ['initialSize','remainingAmount','agentScore','dealerScore',
                      'NoOfAces', 'twoAcesOrMore', 'reward','decision']
paramsIndices =[]
for chosenParams in stateSpaceChosen:
    paramsIndices.append(parameterSpace.index(chosenParams))
     
#%%

