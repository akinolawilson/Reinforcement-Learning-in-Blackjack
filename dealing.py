import numpy as np
import random 


class Dealing:
    
    blackJack = 21
    aceCritical = 2
    
    def __init__(self, deckSize, deck=None):
        
        self.agentHand = []
        self.dealerHand = []
        self.aceCriticalHit = False # if true we have more than two aces in round 
        self.partialDealerScore = 0
        self.dealerScore = 0
        self.agentScore = 0
        self.aceCount = 0
        self.hitScore = 0
        self.hitRound = False
        self.ending = False
        
        
        ########################################## deck info for agent 
        self.deckSize = deckSize                 #
        self.newDeck = self.createDeck(deckSize) # list of cards
        self.initialDeckSize = len(self.newDeck) #
        self.remainingDeckSize = 0               
        self.deck = self.newDeck[:]
        #######################################




        ################################################## function allows verifying 
    def ifGameEnd(self):                                 # during training if game has ended
        if self.ending == True:                          #
            self.deck = self.createDeck(self.deckSize)
            self.newRound()
            return True
        else:
            return False
        #################################################    
        
        
        
    def newRound(self): 
        ##################################### resetting attributes each around since  
        self.agentHand = []                 # they are set to zero with method call
        self.dealerHand = []                #
        self.hitScore = 0                   #
        self.aceCount = 0
        self.agentScore = 0
        self.dealerScore = 0
        self.partialDealerScore = 0
        self.hitRound = False
        self.aceCriticalHit = False         #
        self.ending = False                 #
        #####################################
        try:
            self.agentHand.append(self.deck[0]) #    
            del self.deck[0]                    # remove card top card of deck 
        except IndexError:                      # 
            self.ending = True                  # need to test each draw incase 
        else:                                   # last card. look at function ifGameEnd(self)
            pass                                # to see consequences of setting = True
            
        try:
            self.dealerHand.append(self.deck[0]) # first draw for dealer     
            del self.deck[0]
        except IndexError:
            self.ending = True
        else:
            pass
        
        try:
            self.agentHand.append(self.deck[0]) # second draw for agent
            del self.deck[0]
        except IndexError:
            self.ending = True
        else:
            pass
        
        try:
            self.dealerHand.append(self.deck[0]) # second draw for agent
            del self.deck[0]
        except IndexError:
            self.ending = True
        else:
            pass
        
        self.remainingDeckSize = len(self.deck)
###############################################################################  


      
        
###############################################################################
    def hit(self): # hit for agent     
        try:
            
            self.agentHand.append(self.deck[0])
            del self.deck[0]
            
            self.hitRound = True                     # set to true to make sure score 
            self.remainingDeckSize = len(self.deck)  # for hit round  is calculated correctly
        
        except IndexError:
            self.ending = True
        else:
            pass             
###############################################################################




###############################################################################
    def score(self):
        
        #
        # agent score 
        ####################################################################
        if self.hitRound == False:
            for i in range(len(self.agentHand)):
                try:                  
                    self.agentScore += int(self.agentHand[i])
                except ValueError:                                         
                    pass
                if self.agentHand[i] in ('J', 'K', 'Q','A'):                  
                    if self.agentHand[i] == 'A':  
                        self.aceCount += 1
                        if self.aceCount == Dealing.aceCritical: # if two aces drawn in beginning
                            self.agentScore += 1
                            self.aceCriticalHit = True # second ace not usable,
                        else:                          # can only DECREASE face value
                            self.agentScore += 11                               
                    else:                         
                        self.agentScore += 10 # for J, K and Q
        
            self.hitScore = self.agentScore # save as different score for hitting possibility
        
        #
        # Dealer score  only calculate for new round          
        ########################################################################         
        if self.hitRound == False:
            for i in range(len(self.dealerHand)):
                try:
                    self.dealerScore += int(self.dealerHand[i])    
                except ValueError:                                    
                    pass                                                
                if self.dealerHand[i] in ('J','K','Q','A'):                                                     
                    if self.dealerHand[i] == 'A':
                        self.dealerScore += 11 # Dont have to worry about 
                    else:                      # dealer ace value/ number of   
                        self.dealerScore += 10 # for J, K and Q
            
            #
            #dealer's score visible to agent in game
            ###################################################################
            try:
                self.partialDealerScore += int(self.dealerHand[0])    
            except ValueError:
                pass
            if self.dealerHand[0] in ('J','K','Q','A'):
                if str(self.dealerHand[0]) == 'A':
                    self.partialDealerScore += 11
                else:
                    self.partialDealerScore += 10
        
        #
        #The hit round, no calculations for Dealer; passive. 
        ########################################################################
        
        if self.hitRound == True:
            try:                                                            
                self.hitScore = self.hitScore + int(self.agentHand[-1])         
            except ValueError:                                              
                pass                                                        
            if self.agentHand[-1] in ('J','K','Q','A'):
                if self.agentHand[-1] == 'A':                                   
                    self.aceCount += 1
                    if self.hitScore + 11 > Dealing.blackJack:
                        self.hitScore = self.hitScore + 1
                    else:
                        self.hitScore = self.hitScore + 11
                        self.aceCriticalHit = True
                else:
                    self.hitScore = self.hitScore + 10
                    
   
    def actionOutcome(self, action): 
        
        # function describes consequences of action in enviroment.
        #
        # Notice, that when action taken to stick, we automatically 
        # ask for new round
        #
        # possibly need to alter this: trying to maximise the score, which is 
        # denoted by self.objectiveScore, only have winning as objective, not 
        # by HOW much we are winning. 
        
        
        reward = 0
        if action == 0: # to stick with current cards
            if self.dealerScore < self.hitScore <= Dealing.blackJack:
                ########## self.objectiveScore =  self.hitScore**2  ##### <- SHOULD BE
                reward = 1                                            # MAXIMISING THIS
                self.newRound()
            
            elif self.dealerScore == self.hitScore:
                ########### self.objectiveScore = 0 ##########
                reward = 0
                self.newRound()
            
            elif self.hitScore < self.dealerScore:
                ########### self.objectiveScore = 0 ##########
                reward = -1
                self.newRound()
            
        if action == 1: # to take a hit from the deck
            
            self.hit()
            self.score()
            if self.agentScore > Dealing.blackJack:
                reward = -1
                self.newRound()
            
        return reward
            
              
    
    def createDeck(self, *numberOrInfinity):
        """This function creates a deck of cards that is integer multiples of a standard
        deck of 52 cards. 
        
        Example: enter 1 returns a deck of 52 cards.
                 enter 2 returns a deck of 104 cards.
                    
        For infinite size deck enter arguement 'infinite',  WITH '' bounding the arguement
        
        The deck returned will be a list -> ['A', '3',....,'4']
        
        """
    
        card_faces = ['2', '3', '4', '5', '6', '7',
                      '8', '9', '10', 'J', 'Q', 'K', 'A']
        deck = []
        for size in numberOrInfinity:
            if size == 'infinite': 
                numberOfEachCard = np.inf*np.ones((1,13))
                ##
                # issue with creating infinite list, overflow errors. Will bound full 
                # deck length  to 13 * 1e5 
                ##
                for face in card_faces:
                    for no in range(int(1e5)):
                        
                        deck.append(face)
                        if len(deck) > 13 * 1e5: # stopping criterion for length of infinite deck
                            break
                
                freshDeck = random.sample(deck, len(deck))
                break
        
            try: 
                size = int(size)
            except ValueError: 
                pass
            
            if size > 0:
                numberOfEachCard = size * 4 * np.ones((1,13))
                for face in card_faces:
                    for no in range(int(numberOfEachCard[0,0])):
                        deck.append(face)
                
                freshDeck = random.sample(deck, len(deck))
                
                                                                                                                      
            if size == 0:
                print("Size of deck must be greater than 0.")
                while size == 0: 
            
                    size = int(input('Please enter an integer greater'
                                          ' than 0 for the deck size: '))
                    
                    numberOfEachCard = size * 4 * np.ones((1,13))
                    for face in card_faces:
                        for no in range(int(numberOfEachCard[0,0])):
                            deck.append(face)                                                                       
                    
                    freshDeck = random.sample(deck, len(deck)) # used to shuffle deck        
                                                               
        return freshDeck                                                                                              
    
 #%%