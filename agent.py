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
                 gamma): # discount factor     
        
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
        qHitList, qStickList = [],[]
        for trajectory in range(len(cls.QList)):
            for attemptedStateAction in range(len(cls.QList[trajectory])):
                try:
                    if (cls.QList[trajectory][attemptedStateAction][0] == initialSize and
                        cls.QList[trajectory][attemptedStateAction][1] == remainingDeckSize and
                        cls.QList[trajectory][attemptedStateAction][2] == agentScore and 
                        cls.QList[trajectory][attemptedStateAction][3] == dealerScore and 
                        cls.QList[trajectory][attemptedStateAction][4] == trueDealerScore and 
                        cls.QList[trajectory][attemptedStateAction][5] == aceCount and 
                        cls.QList[trajectory][attemptedStateAction][6] == aceCriticalHit and
                ##### cls.QList[i][7] == Q Value for state i , what we are after 
                        cls.QList[trajectory][attemptedStateAction][8] == 1):
                        qHitList.append(cls.QList[trajectory][attemptedStateAction][7])  
                    if(cls.QList[trajectory][attemptedStateAction][0] == initialSize and
                       cls.QList[trajectory][attemptedStateAction][1] == remainingDeckSize and
                       cls.QList[trajectory][attemptedStateAction][2] == agentScore and 
                       cls.QList[trajectory][attemptedStateAction][3] == dealerScore and 
                       cls.QList[trajectory][attemptedStateAction][4] == trueDealerScore and 
                       cls.QList[trajectory][attemptedStateAction][5] == aceCount and 
                       cls.QList[trajectory][attemptedStateAction][6] == aceCriticalHit and
                ###### cls.QList[i][7] == Q Value for state i; what we want 
                       cls.QList[trajectory][attemptedStateAction][8] == 0):
                            qStickList.append(cls.QList[trajectory][attemptedStateAction][7]) 
                except IndexError:
                    pass
                
        try:
            qHit = max(qHitList)
            qStick = max(qStickList)        
        except ValueError:
            pass
                
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
        
        #stateActionCount = 0
        for trajectory in range(len(cls.QList)):
            for attemptedStateAction in range(len(cls.QList[trajectory])):
                trajectoryComponent = cls.QList[trajectory][attemptedStateAction] # and stateAction value  
                #stateActionCount = attemptedStateAction + 1
            
                alpha = 1 / (attemptedStateAction + 1)
#################################################################################                 
                if policySearchMethod in ["QL","TD","SARSA"]: 
            
                    oldQ = trajectoryComponent[-2]
#                    if len(oldQ) != 0: 
#                        oldQ = trajectoryComponent[-2]
                    
                    # update Q value for (nextState, policyAction) pair
                    if attemptedStateAction < (len(cls.QList[trajectory])-1): # whilst not at terminal state hence the minus 1
                        
                        if policySearchMethod == "QL":
                            hitHypothesis = cls.QList[trajectory][attemptedStateAction+1][:-1]+(1,) # alter/ keep to 'decision':1 ->  hitMeBaby
                            stickHypothesis = cls.QList[trajectory][attemptedStateAction+1][:-1]+(0,) # alter/ keep to 'decision':0 -> stick
                            maxQ = max(  hitHypothesis[:][:][-2],
                                       stickHypothesis[:][:][-2] )                   
                            sumOfFutureDiscountedRewards = gamma * maxQ # discounting future rewards

                        if policySearchMethod == "SARSA":
                            nextStateAction = cls.QList[trajectory][attemptedStateAction+1]
                            sumOfFutureDiscountedRewards = gamma * nextStateAction[-2]
                            
                        if policySearchMethod == "TD":
                            nextStateAction = cls.QList[trajectory][attemptedStateAction+1]
                            sumOfFutureDiscountedRewards = gamma * nextStateAction[-2]
                            
                    else: # at terminal state, no value for being in state 
                        sumOfFutureDiscountedRewards = 0
##################################################################################                
                if policySearchMethod == "QL":
                    update = 0
                    elements = list(trajectoryComponent)
                    elements[-2] =  (1-alpha) * oldQ + alpha*(reward + sumOfFutureDiscountedRewards)                   
                    update = tuple(elements)
                    cls.QList[trajectory][attemptedStateAction] = update
                
                if policySearchMethod == "SARSA":
                    update = 0
                    elements = list(trajectoryComponent)
                    elements[-2] =  oldQ + alpha*(reward + sumOfFutureDiscountedRewards - oldQ )                   
                    update = tuple(elements)
                    cls.QList[trajectory][attemptedStateAction] = update
                    
                if policySearchMethod == "TD":
                    update = 0
                    elements = list(trajectoryComponent)
                    elements[-2] += alpha * (reward + sumOfFutureDiscountedRewards-cls.QList[trajectory][attemptedStateAction][-2] )                   
                    update = tuple(elements)
                    cls.QList[trajectory][attemptedStateAction] = update
                    
        return cls.QList



#%%