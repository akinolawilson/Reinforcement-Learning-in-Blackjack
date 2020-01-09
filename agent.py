import random


class AgentDecisionProcess:
    
    #  QTable will be updated during game play. Holds Q values for all visited states 
    # and asccoiated actions.
    QList = []
# state space = ['initialSize','remainingAmount','agentScore','dealerScore',
               # 'NoOfAces', 'twoAcesOrMore', 'reward','decision']
    #gamma = 0 
    def __init__(self,
                 initialDeckSize,
                 deck,
                 hitScore,
                 visibleDealerScore,
                 trueDealerScore,
                 aceCount,
                 aceCriticalHit,
                 gamma): # discount factor a 

        self.gamma = gamma
        self.sizeDeck = initialDeckSize
        self.remainingDeckSize = len(deck)
        self.score = hitScore
        self.dealerScore = visibleDealerScore
        self.trueDealerScore = trueDealerScore

        self.aceCount = aceCount # counts aces, if 1, then FREE to choose Aup or Adown
                                 # ACTIONS = {Aup,Adown} -> [A1=Aup] or [A1=Adown]                         
        self.aces = aceCriticalHit # bool, if TRUE and aceCount <=2 then out of actions
                                   # {Aup, Adown} -> [A1 = Adown, A2 = Aup] must be chosen  
                                   # If true AND aceCount >=3 then out of actions  
                                   # then {Aup, Adown} -> [A1=Adown,A2=Adown,A3=Adown]
                                   # must be chosen
################################################### 
    @staticmethod
    def actionInitiating():
        
        if random.random() <= 0.5:
            return 0 # stick
        else:
            return 1 # hitmebaby
###################################################    
    
        
###################################################        
    def eGreedyPolicyQTable(self,
                            e,
                            initialSize,
                            remainingDeckSize,
                            score,
                            dealerScore,
                            trueDealerScore,
                            aceCount,
                            aceCriticalHit):
        if random.random() < e: # e - is exploration rate; agent explores random choice
            return AgentDecisionProcess.actionInitiating()
        else: # (1-e) - is the explotation rate; agent uses current knowledge to make decision    
            return self.optimalPolicyQTable(initialSize,
                                            remainingDeckSize,
                                            score,
                                            dealerScore,
                                            trueDealerScore,
                                            aceCount,
                                            aceCriticalHit)
            
#####################################################        
            
            
#####################################################  
    @classmethod 
    def optimalPolicyQTable(cls,
                            initialSize,
                            remainingDeckSize,
                            agentScore,
                            dealerScore, 
                            trueDealerScore,
                            aceCount,
                            aceCriticalHit):
        qHit, qStick = 0,0
        # Identifying states identical to current state and collecting 
        # q-values corresponding to hitting or sticking in state. If none is 
        # found, a random action is taken.
        for i in range(len(cls.QList)):
            if (cls.QList[i][0] == initialSize and
                cls.QList[i][1] == remainingDeckSize and
                cls.QList[i][2] == agentScore and 
                cls.QList[i][3] == dealerScore and 
                cls.QList[i][4] == trueDealerScore and 
                cls.QList[i][5] == aceCount and 
                cls.QList[i][6] == aceCriticalHit and
              # cls.QList[i][7] == Q Value for state i  
                cls.QList[i][8] == 1):
                   qHit = cls.QList[i][7]
                   
            if(cls.QList[i][0] == initialSize and
               cls.QList[i][1] == remainingDeckSize and
               cls.QList[i][2] == agentScore and 
               cls.QList[i][3] == dealerScore and 
               cls.QList[i][4] == trueDealerScore and 
               cls.QList[i][5] == aceCount and 
               cls.QList[i][6] == aceCriticalHit and
               cls.QList[i][8] == 0):
                   qStick = cls.QList[i][7]
                
        if qHit > qStick:
            return 1
        elif qHit < qStick:
            return 0
        else:
            return AgentDecisionProcess.actionInitiating()
########################################################    
          
########################################################       
    @classmethod     
    def QTableUpdate(cls,
                     policySearchMethod,
                     reward,
                     gamma):

        stateScanning = [x[:][:-1] for x in cls.QList] 
        stateActionScanning = cls.QList[:]
    
        stateCount = 0
        stateActionCount = 0
    
        for i in range(len(cls.QList)):
            
            visitedState = cls.QList[i][:-1]   # evaulating all trajectory's state 
            exploredStateAction = cls.QList[i] # and stateAction value  
            
            stateCount = stateScanning.index(visitedState) + 1
            stateActionCount = stateActionScanning.index(exploredStateAction) + 1
        
            alpha = 1 / stateActionCount
            
            if policySearchMethod in ["QLearning","TD","SARSA"]: 
            
                oldQ = exploredStateAction[i][-2]
                # update Q value for (nextState, policyAction) pair
                if i < len(range(cls.QList))-1: # whilst not at terminal state hence the minus 1
                    
                    if policySearchMethod == "QLearning":
                        hitConsideration = cls.QList[i+1][:-1]+(1,) # alter/ keep to 'decision':1 ->  hitMeBaby
                        stickConsideration = cls.QList[i+1][:-1]+(0,) # alter/ keep to 'decision':0 -> stick
                                                                                           
                                                                                         ##############################################################
                                                                                         #   maxValueHit = [] 
                                                                                         #   maxValueStick = [] 
                                                                                         #   # searching QList for highest Q value for given actions and state
                        maxQ = max( cls.QList[  hitConsideration  ],                     #
                                    cls.QList[ stickConsideration ] )                    #   for i in range(len(cls.QList)):
                                                                                         #       for j in range(len(cls.QList)):
                                                                                         #           try:
                                                                                         #               if cls.QList[i][j] == hitConsideration:
                                                                                         #                   maxValueHit.append(cls.QList[j][i][-2])    
                                                                                         #           except IndexError:
                                                                                         #               pass
                                                                                         #           try:
                                                                                         #               if cls.QList[i][j] == stickConsideration:
                                                                                         #                   maxValueStick.append(cls.QList[j][i][-2])    
                                                                                         #           except IndexError:
                                                                                         #               pass
                                                                                         #   
                                                                                         #   
                                                                                         #       maxQ = max( maxValueHit, maxValueStick ) # find action which gives maximum
                                                                                         ###############################################################    
                        
                        # discounting future reward   
                        sumOfFutureDiscountedRewards = gamma * maxQ

                    if policySearchMethod == "SARSA":
                        nextStateAction = exploredStateAction[i+1]
                        sumOfFutureDiscountedRewards = gamma * nextStateAction[:][-2]
                        
                    if policySearchMethod == "TD":
                        nextStateAction = exploredStateAction[i+1]
                        sumOfFutureDiscountedRewards = gamma * nextStateAction[:][-2]
                        
                else: # at terminal state, no value for being in state 
                    sumOfFutureDiscountedRewards = 0
            
            if policySearchMethod == "QLearning":
                update = 0 
                for stateAction in exploredStateAction[i]:
                    elements = list(stateAction)
                    elements[-2] =  (1-alpha) * oldQ + alpha*(reward + sumOfFutureDiscountedRewards)                   
                    update = tuple(elements)
                cls.QList[i] = update
                
            if policySearchMethod == "SARSA":
                update = 0 
                for stateAction in exploredStateAction[i]:
                    elements = list(stateAction)
                    elements[-2] =  oldQ + alpha*(reward + sumOfFutureDiscountedRewards - oldQ )                   
                    update = tuple(elements)
                cls.QList[i] = update
                
            if policySearchMethod == "TD":
                update = 0 
                for stateAction in exploredStateAction[i]:
                    elements = list(stateAction)
                    elements[-2] += alpha * (reward + sumOfFutureDiscountedRewards-cls.QList[i][-2] )                   
                    update = tuple(elements) # Temperoal Difference target. 
                cls.QList[i] = update
                
        return cls.QList
    



#%%