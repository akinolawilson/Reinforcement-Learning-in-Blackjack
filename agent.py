import random


#%%
class AgentDecisionProcess:
    
    QTable = dict.fromkeys(['initialSize',
                           'remainingAmount',
                           'agentScore',
                           'dealerScore',
                           'NoOfAces',
                           'twoAcesOrMore',
                           'decision'])

    def __init__(self,
                 initialDeck,
                 deck,
                 hitScore,
                 visibleDealerScore,
                 aceCount,
                 aceCriticalHit):
        
        
        self.sizeDeck = len(initialDeck)
        self.remainingDeck = len(deck)
        self.score = hitScore
        self.dealerScore = visibleDealerScore
        
        self.aceCount = aceCount # counts aces, if 1, then FREE to choose Aup or Adown
                                 # ACTIONS = {Aup,Adown} -> [A1=Aup] or [A1=Adown]
                                 
        self.aces = aceCriticalHit # bool, if TRUE and aceCount <=2 then out of actions
                                   # {Aup, Adown} -> [A1 = Adown, A2 = Aup] must be chosen  
                                   # If true AND aceCount >=3 then out of actions  
                                   # then {Aup, Adown} -> [A1=Adown,A2=Adown,A3=Adown]
                                   # must be chosen
        

        
        
    def actionInitiating(self):
        if random.random() <= 0.5:
            return 0 # stick
        else:
            return 1 # hitmebaby
    
    

    def eGreedyPolicyQTable(self,
                            e,
                            QTable,
                            score,
                            dealerScore,
                            aceCount,
                            aceCriticalHit):
        if random.random() < e: # e - is exploration rate; agent explores random choice
            return self.actionInitiating()
        else: # (1-e) - is the explotation rate; agent uses current knowledge to make decision    
            return self.optimalPolicyQTable(QTable,
                                            score,
                                            dealerScore,
                                            aceCount,
                                            aceCriticalHit)
    
    
    def optimalPolicyQTable(self,
                            QTable,
                            agentScore,
                            dealerScore,
                            aceCriticalHit):
        qHit = AgentDecisionProcess.QTable[(agentScore,
                                           dealerScore,
                                           aceCriticalHit,#twoAcesOrMore,
                                           1)]
        qStick = AgentDecisionProcess.QTable[(agentScore,
                                              dealerScore,
                                              aceCriticalHit,#Agent.twoAcesOrMore,
                                              0)]
        if qHit > qStick:
            return 0
        elif qHit < qStick:
            return 1
        else:
            return self.actionInitiating()
    
        
        
    def QTableInColumnUpdate(self,
                             reward,
                             trajectory, # matrix [i,j]
                             QTable,
                             noOfState,
                             noOfStateAction,
                             method,
                             gamma = 0.8):
        for i in range(len(trajectory)):
            
            state = trajectory[i][:-1]
            stateAction = trajectory[i]
            
            noOfState[state] += 1
            noOfStateAction[stateAction] += 1
            
            
            
        QTable = dict.fromkeys(['initialSize',
                           'remainingAmount',
                           'agentScore',
                           'dealerScore',
                           'NoOfAces',
                           'twoAcesOrMore',
                           'decision'])
        
        
                
        
        pass
            
      
        
    
    
    
    
    def qLearning(self):
        pass

    def sarsaLearning(self):
        pass
    
    def TDLearning(self):
        pass
    
    
    #%%