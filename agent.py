import random


class AgentDecisionProcess:
    
    #  QTable will be updated during game play. Holds Q values for all visited states 
    # and asccoiated actions.
    
    QList = []
#   QTableKeys = dict.fromkeys(['initialSize',
#                                'remainingAmount',
#                                'agentScore',
#                                'dealerScore',
#                                'NoOfAces',
#                                'twoAcesOrMore',
#                                'reward',
#                                'decision'])
    gamma = 0 

    def __init__(self,
                 initialDeckSize,
                 deck,
                 hitScore,
                 visibleDealerScore,
                 aceCount,
                 aceCriticalHit,
                 gamma,
                 QList = None ): # discount factor

        self.gamma = gamma 
        self.sizeDeck = initialDeckSize
        self.remainingDeckSize = len(deck)
        self.score = hitScore
        self.dealerScore = visibleDealerScore
        
        self.QList = QList
        #self.newEpisode = newEpisode # for clearing QTable for new Trajectory
        
        self.aceCount = aceCount # counts aces, if 1, then FREE to choose Aup or Adown
                                 # ACTIONS = {Aup,Adown} -> [A1=Aup] or [A1=Adown]
                                 
        self.aces = aceCriticalHit # bool, if TRUE and aceCount <=2 then out of actions
                                   # {Aup, Adown} -> [A1 = Adown, A2 = Aup] must be chosen  
                                   # If true AND aceCount >=3 then out of actions  
                                   # then {Aup, Adown} -> [A1=Adown,A2=Adown,A3=Adown]
                                   # must be chosen


###################################################                    
    def actionInitiating(self):
        
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
            return self.actionInitiating()
        
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
    def optimalPolicyQTable(self,
                            initialSize,
                            remainingDeckSize,
                            agentScore,
                            dealerScore, 
                            trueDealerScore,
                            aceCount,
                            aceCriticalHit,
                            QList):
        
        try:
             QList = self.QList
        except None:
            pass
        

            
        
        for i in range(len(QList)):
            
            if (QList[i][0] == initialSize and
                QList[i][1] == remainingDeckSize and
                QList[i][2] == agentScore and 
                QList[i][3] == dealerScore and 
                QList[i][4] == trueDealerScore and 
                QList[i][5] == aceCount and 
                QList[i][6] == aceCriticalHit and
               QList[i][8] == 1):
                   qHit = QList[i][7]
                   
        for j in range(len(QList)):
            
            if (QList[j][0] == initialSize and
               QList[j][1] == remainingDeckSize and
               QList[j][2] == agentScore and 
               QList[j][3] == dealerScore and 
               QList[j][4] == trueDealerScore and 
               QList[j][5] == aceCount and 
               QList[j][6] == aceCriticalHit and
               QList[j][8] == 0):
                
                   qStick = QList[j][7]
                
        if qHit > qStick:
            return 1
        elif qHit < qStick:
            return 0
        else:
            return self.actionInitiating()
########################################################    
#    @classmethod
#    def makeQTable(cls, Q):
#        QTable = list(zip(cls.QTableKeys, cls.QList))
#        return QTable
########################################################        

    
########################################################       
    @classmethod     
    def QTableInColumnUpdate(cls,
                             self,
                             policySearchMethod,
                             QList,
                             gamma):
        
        #trajectory = cls.makeQTable()
        
        # boot strap
        try:
            self.QList = QList
            stateScanning = [x[:][:-1] for x in self.QList] 
            stateActionScanning = QList[:]
        except NameError:
            pass
        else:
            stateScanning = [x[:][:-1] for x in QList] 
            stateActionScanning = QList[:]
            

        stateCount = 0 
        stateActionCount = 0 
        
        for i in range(len(QList)):
            # inline update, I.e in column of qTable
            visitedState = QList[i][:-1] # state without action, LAST element is action taken, state s_i
            exploredStateAction = QList[i] # state WITH previous action, 
            
            stateCount = stateScanning.index(visitedState) + 1 # incrementing state  and stateAction count
            stateActionCount = stateActionScanning.index(exploredStateAction) + 1
            
            # let the learning rate alpha be propotional to size of state-Action space
            # => the smaller alha, the more knowledge agent has about deck content since 
            # the closer to end of trajectory, the closer to end of game and hence
            # the less hidden information 
            
            alpha = 1 / stateActionCount
            
            if policySearchMethod == "QLearning" or policySearchMethod == "TD":
                
                priorQ = exploredStateAction[i][-2]
                
                # update Q value for (nextState, policyAction) pair
                
                if i < len(range(QList))-1: # whilst not at terminal state
                    
                    if policySearchMethod == "QLearning":
                            
                        trajectoryHitConsideration = QList[i+1][:-1] + (1,) # alter/ keep to 'decision':1 ->  hitMeBaby
                        trajectoryStickConsideration = QList[i+1][:-1] + (0,) # alter/ keep to 'decision':0 -> stick
                        
                        maxQ = max( QList[  trajectoryHitConsideration  ],
                                    QList[ trajectoryStickConsideration ] ) # find action which gives maximum
                        
                        # discounted reward
                        bestNextQ = gamma * maxQ
                    
                    
                    
                    if policySearchMethod == "TD":
                        
                        nextStateAction = exploredStateAction[i+1]
                        bestNextQ = gamma * nextStateAction[:][-2]
                        
                    
                else: # at terminal state, no value for being in state 
                    bestNextQ = 0
            
            
            if policySearchMethod == "QLearning":
                
                QList[exploredStateAction[i]] = (1-alpha)*priorQ + alpha*( exploredStateAction[-2] + bestNextQ)
            
            
            if policySearchMethod == "TD":
                
                QList[exploredStateAction[i]] += alpha * ( exploredStateAction[i][-2] - QList[exploredStateAction[i]] )
    
        return QList
    

#%%