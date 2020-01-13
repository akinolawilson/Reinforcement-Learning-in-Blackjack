from dealing import Dealing
import numpy as np 
import time 
import random
from ast import literal_eval as make_tuple

def actionInitiating():
    
    if random.random() <= 0.5:
        return 0 # stick
    else:
        return 1 # hit

def QTableReduction(QTable, stateSpaceChosen):
    """
    Function takes in qtable and reduces the state space to the specified list of 
    state parameters that should be used for the agent to play from. 
    
    E.g. params to be infered from could be 
    ['initialSize','remainingAmount','agentScore'], 
    NOTE: DONT INCLUDED REWARD and DECISION, will be appended bellow.
    
    Function returns the indices corresponding to the specified state space 
    and the reduced QTable
    """
    parameterSpace = ['initialSize','remainingAmount','agentScore',
                      'partialDealerScore','dealerScore', 'NoOfAces',
                      'twoAcesOrMore', 'reward','decision']
    
    stateSpaceChosen.append( 'reward')
    stateSpaceChosen.append('decision')  
    paramsIndices =[]
    # retrieve indices of parameters that will be used for hitting and sticking 
    for chosenParams in stateSpaceChosen:
        paramsIndices.append(parameterSpace.index(chosenParams))
    # Reducing the QTable content to match that of the specified parameters to be used 
    # for the agent to infer from. 
    for trajectory in range(len(QTable)):
        for stateAction in range(len(QTable[trajectory])):
            
            state = list(QTable[trajectory][stateAction])
            stateReduced = [state[params] for params in paramsIndices]
            
            stateReducedTuple = tuple(stateReduced)
            QTable[trajectory][stateAction] = stateReducedTuple
   
    return QTable, paramsIndices

def optimalDecision(state, QTableReduced,numberOfParams):
    '''
    Returns optimal decision given state. Arguments are state of agent, -tuple-,
    the reduced QTable and the NUMBER of state space parameters, NOT indices.

    '''
    qHit, qStick = 0,0
    qHitList, qStickList = [],[]

    for trajectory in range(len(QTableReduced)):
        for attemptedStateAction in range(len(QTableReduced[trajectory])):
            try:
                if tuple(QTableReduced[trajectory][attemptedStateAction][:numberOfParams+1]) +(1,) ==  tuple(state) +(1,):
                    # Hit hypothesis
                    qHitList.append(QTableReduced[trajectory][attemptedStateAction][-2])   
                if tuple(QTableReduced[trajectory][attemptedStateAction][:numberOfParams+1]) +(0,) == tuple(state) +(0,):
                    # stick Hypothesis
                    qStickList.append(QTableReduced[trajectory][attemptedStateAction][-2])
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
    else:
        return actionInitiating()

def game(multipleOfDeck, stateSpaceChosen, policy, numberOfRepitionsOfGame):
    """
    The possible multiple of decks are [1-10]. The game will automatically load 
    in the corresponding QTable for the game size, state sapce parameters chosen
    and the policy. Please ensure that the relevant QTable files are in the correct
    working directory.
    
    The agent will then play against a passive dealer given the state space and 
    the quantitative results of the game play will be printed in the console.
    
    Please vary the sleep period for larger repetitions( 10>>), 
    marked  in script with ## above and
    below each line of code. 
    """
    for policy in ["TD", "QL", "SARSA"]:
        with open('qTable'+str(policy)+str(multipleOfDeck)+'.csv', "r") as table:
            trajectory = table.readlines()
            file = [x.strip("\n") for x in trajectory]
            QTable = []
            for i in range(len(file)):
               QTable.append(make_tuple(file[i])) 
    

    if policy == "TD":
        name = 'temporal difference'
        
    if policy =="QL":
        name = 'Q-Learning'
        
    if policy== "SARSA":
        name = 'state-action-reward-state-action'

    QTableReduced, paramsIndices = QTableReduction(QTable, stateSpaceChosen)
    
    game = Dealing(multipleOfDeck)
    game.newRound()
    
    print("The Agent's first hand is {}".format(game.agentHand))
    print("The Dealers's first hand is {}".format(game.dealerHand))
    print(' The agent will now base its actions on the learnt optimal'
          " policy under the {} control search method .".format(name))
    print("Given the state parameters provided : {}".format(str(stateSpaceChosen)))
    print("The game will be repeated {} times".format(numberOfRepitionsOfGame))
    print(" Finally, the average quadratic score of the agent per game and "
          " win, loss an draw precentages will be printed.")
    print("The result of each in game interation will be printed in the console")
    
    time.sleep(2) # added so that the text above can be read
    runningScore = 0
    runningSucess= [0,0,0]

    for i in range(numberOfRepitionsOfGame):  
        while game.ifGameEnd()==False:        
            def initialSize():
                return game.initialDeckSize                
            def remainingAmount():
                return game.remainingDeckSize                
            def agentScore():
                return game.hitScore                
            def partialDealerScore():
                return game.partialDealerScore                
            def dealerScore():
                return game.dealerScore
            def NoOfAces():
                return game.aceCount
            def twoAcesOrMore():
                return game.aceCriticalHit
            
            stateSpaceDictionary = {0:initialSize,
                                    1:remainingAmount,
                                    2:agentScore,
                                    3:partialDealerScore,
                                    4:dealerScore,
                                    5:NoOfAces,
                                    6:twoAcesOrMore}
            
            def StateParamsSelector(paramsIndices):
                state = []
                for p in paramsIndices[:-2]:
                    state.append(stateSpaceDictionary[p])
                state = tuple(state)
                return state
            
            agentState = StateParamsSelector(paramsIndices)
            action = optimalDecision( agentState, QTableReduced, len(paramsIndices))
            r = game.actionOutcome(action)
            time.sleep(0.5)
            
            if float(r) > 0:
                 print("Agent won round")
                 runningScore +=1 * game.hitScore**2
                 runningSucess[0] +=1
            elif float(r) < 0 :
                 print("Agent lost round")
                 runningSucess[1] +=1
            else:
                print("Agent drew round")
                runningSucess[2] +=1        
            
            if game.ifGameEnd()==True:
                break 
                
    print("The win, loss and draw  are {}%,{}% and {}% "
        "respectively".format(np.round(runningSucess[0]/sum(runningSucess) *100, 1),
                              np.round(runningSucess[1]/sum(runningSucess) *100, 1),
                              np.round(runningSucess[2]/sum(runningSucess) *100, 1)))
    
    print("The average quadratic score per game is: {} ".format(runningScore/numberOfRepitionsOfGame))
    