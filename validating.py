import dealing as Dealing
import numpy as np 
import matplotlib.pyplot as plt
import time 

import time 

def optimalDecision(state, QTable):
    '''
    returns optimal decision 
    '''
    qHit, qStick = 0,0
    qHitList, qStickList = [],[]
    for trajectory in range(len(QTable)):
        for attemptedStateAction in range(len(QTable[trajectory])):
            try:
                if (QTable[trajectory][attemptedStateAction][0] == state[0] and
                    QTable[trajectory][attemptedStateAction][1] == state[1] and
                    QTable[trajectory][attemptedStateAction][2] == state[2] and 
                    QTable[trajectory][attemptedStateAction][3] == State[3] and 
                    QTable[trajectory][attemptedStateAction][4] == state[4] and # turn off 
                    QTable[trajectory][attemptedStateAction][5] == state[5] and 
                    QTable[trajectory][attemptedStateAction][6] == State[6] and
                    QTable[trajectory][attemptedStateAction][8] == 1):
                
                    qHitList.append(QTable[trajectory][attemptedStateAction][7]) 
                
                if (QTable[trajectory][attemptedStateAction][0] == state[0] and
                    QTable[trajectory][attemptedStateAction][1] == state[1] and
                    QTable[trajectory][attemptedStateAction][2] == state[2] and 
                    QTable[trajectory][attemptedStateAction][3] == State[3] and 
                    QTable[trajectory][attemptedStateAction][4] == state[4] and # turn off 
                    QTable[trajectory][attemptedStateAction][5] == state[5] and 
                    QTable[trajectory][attemptedStateAction][6] == State[6] and
                    QTable[trajectory][attemptedStateAction][8] == 0):
                    
                    qStickList.append(QTable[trajectory][attemptedStateAction][7]) 
            except IndexError:
                pass      
    try:
        qHit = max(qHitList)
        qStick = max(qStickList)        
    except ValueError:
        pass
    if qHit > qStick:
        return 1
    if qHit < qStick:
        return 0
    

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
game(4, q)
    