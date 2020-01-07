import random


class AgentDecisionProcess:
    
    #  QTable will be updated during game play. Holds Q values for all visited states 
    # and asccoiated actions.
    
    QTable = []
    QTableCombo = dict.fromkeys(['initialSize',
                                'remainingAmount',
                                'agentScore',
                                'dealerScore',
                                'NoOfAces',
                                'twoAcesOrMore',
                                'reward',
                                'decision'])
    gamma = 0 

    def __init__(self,
                 initialDeck,
                 deck,
                 hitScore,
                 visibleDealerScore,
                 aceCount,
                 aceCriticalHit,
                 gamma): # discount factor

        self.gamma = gamma 
        self.sizeDeck = len(initialDeck)
        self.remainingDeck = len(deck)
        self.score = hitScore
        self.dealerScore = visibleDealerScore
        
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
                            remainingDeck,
                            score,
                            dealerScore,
                            aceCount,
                            aceCriticalHit):
        if random.random() < e: # e - is exploration rate; agent explores random choice
            return self.actionInitiating()
        else: # (1-e) - is the explotation rate; agent uses current knowledge to make decision    
            return self.optimalPolicyQTable(initialSize,
                                            remainingDeck,
                                            score,
                                            dealerScore,
                                            aceCount,
                                            aceCriticalHit)
#####################################################
    def         
            
#####################################################            
    def optimalPolicyQTable(self,
                            initialSize,
                            remainingDeck,
                            agentScore,
                            dealerScore,
                            aceCriticalHit):
        
        qHit = AgentDecisionProcess.QTable[(initialSize,
                                            remainingDeck,
                                            agentScore,
                                            dealerScore,
                                            aceCriticalHit,#twoAcesOrMore,
                                            1)]
    
        qStick = AgentDecisionProcess.QTable[(initialSize,
                                              remainingDeck,
                                              agentScore,
                                              dealerScore,
                                              aceCriticalHit,#Agent.twoAcesOrMore,
                                              0)]
        if qHit > qStick:
            return 0
        elif qHit < qStick:
            return 1
        else:
            return self.actionInitiating()
########################################################    
 
########################################################       
    @classmethod     
    def QTableInColumnUpdate(cls,
                             reward,
                             trajectory, # matrix [i,j]
                             noOfNextState,
                             noOfNextStateAction,
                             policySearchMethod,
                             gamma):
        
        for i in range(len(trajectory)):
            # inline update, I.e in column of qTable
            visitedState = trajectory[i][:-1]
            exploredStateAction = trajectory[i]
            
            noOfNextState[visitedState] += 1
            noOfNextStateAction[exploredStateAction] += 1
            
            # let the learning rate alpha be propotional to size of state-Action space
            # => the smaller alha, the more knowledge agent has about deck content since 
            # the closer to end of trajectory, the closer to end of game and hence
            # the less hidden information 
            
            alpha = 1/ noOfNextStateAction[exploredStateAction]
            
            if policySearchMethod == "QLearning":
                
                priorQ = AgentDecisionProcess.QTable[exploredStateAction]
                # update Q value for (nextState, policyAction) pair
                
                if i < len(trajectory)-1: # whilst not at terminal state
                    
                    inlinePosteriorStateHitAction = trajectory[i+1][:-1] + (1) # alter/ keep to 'decision':1 ->  hitMeBaby
                    inLinePosteriorStateStickAction = trajectory[i+1][:-1] + (0) # alter/ keep to 'decision':0 -> stick
                    
                    maxQ = max(AgentDecisionProcess.QTable[inlinePosteriorStateHitAction],
                               AgentDecisionProcess.QTable[inLinePosteriorStateStickAction]) # find action which gives maximum
                    
                    # discounted reward
                    maxQunderPolicy = gamma * maxQ
                    
                else: # at terminal state, no value for being in state 
                    maxQunderPolicy = 0
            
                AgentDecisionProcess.QTableDict[trajectory[i]] = (1-alpha)*priorQ + alpha*(reward + maxQunderPolicy)
            
            
            if policySearchMethod == "TemporalDifference":
                
                AgentDecisionProcess.QTable[trajectory[i]] += alpha * ( reward - AgentDecisionProcess.QTable[trajectory[i]])
    
    

#%%