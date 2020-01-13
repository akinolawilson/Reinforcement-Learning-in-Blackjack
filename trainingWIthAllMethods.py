import training as t
import numpy as np 

# Running this script will produce the Q Table for the the control methods: Q-Learning
# Temperoal Difference and State-action-reward-state-action method. These tables 
# will be produced for deck size of 1 to 10 decks. The saved csv files are then 
# used in the validating.py script. 


policySearchMethods = ['QL','TD', 'SARSA']
gameSizes = [1,2,3,4,5,6,7,8,9,10]
exploreVsExploit =[1000,5000] # iterations of phases

results = []

for gameSize in gameSizes:
    for methods in policySearchMethods:
        
        QTable,  pe, pO, pointOptimal, pointEgreedy = t.agentTraining(gameSize,
                                                                      exploreVsExploit[0],
                                                                      exploreVsExploit[1],
                                                                      methods,
                                                                      1,
                                                                      0)
        numberOfinteractions = 0 
        # calculating number of interactions
        for traj in range(len(QTable)):
            for SA in range(len(QTable[traj])):
                numberOfinteractions += 1
                
        results.append(methods)
        results.append(gameSize)                                                                        
        results.append(numberOfinteractions)
        results.append(pe)
        results.append(pO)
        results.append(pointOptimal)
        results.append(pointEgreedy)
                                            
        np.savetxt('qTable'+str(methods)+str(gameSize)+'.csv',
                                                       QTable,
                                                       newline='\n',
                                                       delimiter="\t",
                                                       fmt='%s')
        
        
        
#%%
 