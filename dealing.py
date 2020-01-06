import numpy as np
import random 


class Dealing:
    
    def __init__(self, deckSize, deck, agentScore):
        
        self.blackJack = 21
#        self.newRound = False
#        self.hit = False
        self.agentHand = []
        self.dealerHand = []
        self.agentTotalInRoundScore = 0
        self.agentScore = 0
     #   self.dealerScore = 0
        
        self.newDeck = self.createDeck(deckSize)
        self.initialDeck = self.newDeck
        self.deck = self.newDeck[:]
        
        self.agentAceInHand = 0; # Agent possibly has ace in hand 
        self.dealerPartialHand = 0; # partial information during round
        
       # if self.newRound == True:
       #     self.drawNewRound(yes=True)
       # if self.hit == True:
       #     self.drawInRoundHit(yes=True)
        

    def drawNewRound(self, yes=False):
        if yes == True:
            self.agentHand.append(self.deck[0]) # first draw for agent     
            del self.deck[0] # remove card top card of deck 
            self.dealerHand.append(self.deck[0]) # first draw for dealer
            del self.deck[0]
            self.agentHand.append(self.deck[0]) # second draw for agent
            del self.deck[0]
            self.dealerHand.append(self.deck[0]) # second draw for dealer. the unknown card, 
            del self.deck[0]                     # hidden information to the dealer
             
   
    
    def drawInRoundHit(self, yes=False):
        if yes == True:    
            self.agentHand.append(self.deck[0]) # hit for agent     
            del self.deck[0] # remove card top card of deck 
    
    
    

    def agentPersonalScoreComputation(self):
        
        noOfAces, acePossible, aceUsed = 0, False, False # aceUsed implies this has happened => 11 goes to 1 
                                                         # acePossible implies CAN use ace and => 11 goes to 1
        ####################################################################
        if len(self.agentHand) == 2: # we know its a new round. rather than hit. #
            for i in range(len(self.agentHand)):                                       #
                                                                           #                    
                try:                                                       #  
                    self.score += int(self.agentHand[i])    # 2 to 10 cards          # New round, since number of 
                except ValueError:                                         # cards is more than 1, i,e
                    pass                                                   # 2 cards dealt = New Round
                                                                           #  
                else:                                                      #   
                    if str(self.agentHand[i]) == 'A': # A face cards            #         
                        noOfAces += 1
                        acePossible = True
                        aceUsed = False                                           #
                        self.agentScore += 11                                        #
                    else:                                                  #
                        self.agentScore += 10 # for J, K and Q
                finally:
                    self.agentTotalInRoundScore = self.agentScore
    
               #     return scoreHitRound, noOfAcesHitRound
        
        #####################################################################
        else:
                                                                       #
            try:                                                            # Hit round since no.
                self.agentTotalInRoundScore = self.agentTotalInRoundScore + int(self.agentHand[-1])                  #  of cards not 2 but must be 
            except ValueError:                                              # greater than. Hence a hit round
                pass                                                        #
            else:                                                           #
                if str(self.agentHand[-1]) == 'A':                                   #
                    noOfAces = noOfAces + 1 
                    acePossible = True
                    while self.agentTotalInRoundScore + 11 > self.blackJack:
                        self.agentTotalInRoundScore = self.agentTotalInRoundScore + 1
                        aceUsed = True
                        
                    else:
                        self.agentTotalInRoundScore = self.agentTotalInRoundScore + 11
                        
                else:
                    self.agentTotalInRoundScore = self.agentTotalInRoundScore + 10
                    
            finally:
                return noOfAces, acePossible, aceUsed
            
            
        
            
            
    def hitOrStickAction(self, dealing, action, score):
        
        reward, agentScore, dealerScore = 0, dealing.agentScore, dealing.dealerScore
        
        if action == 0: # to stick with current cards
            if  dealerScore < agentScore <= self.blackJack:
                self.agentTotalScore += agentScore**2
                reward = 1
            
            elif dealerScore == agentScore:
            
                reward = 0
                
            else:
                reward = -1
        
        if action == 1: # to take a hit from the deck
            
            dealing.drawInRoundHit(yes=True)
            agentScore = dealing.agentScore
            
            if action == 0: # to stick 
                
                if  dealerScore < agentScore <= self.blackJack:
                    self.agentTotalScore += agentScore**2
                    reward = 1
            
                elif dealerScore == agentScore:        
                    reward = 0
                
                else:
                    reward = -1
                    
            if action == 1: # to take a hit from the deck
    
                dealing.drawInRoundHit(yes=True)
                agentScore = dealing.agentScore
            
                if action == 0: # to stick 
                
                    if  dealerScore < agentScore <= self.blackJack:
                        self.agentTotalScore += agentScore**2
                        reward = 1
                
                    elif dealerScore == agentScore:        
                        reward = 0
                    
                    else:
                        reward = -1
                        
                if action == 1: # to take a hit from the deck, ALLOWING THREE HITS
    
                    dealing.drawInRoundHit(yes=True)
                    agentScore = dealing.agentScore
            
                    if action == 0: # to stick 
                    
                        if  dealerScore < agentScore <= self.blackJack:
                            self.agentTotalScore += agentScore**2
                            reward = 1
                    
                        elif dealerScore == agentScore:        
                            reward = 0
                        
                        else:
                            reward = -1
                            
        
            agentTotalScore = self.agentTotalScore                    
                            
        return agentTotalScore, reward       

    
    def createDeck(self, *kwargs):
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
        for size in kwargs:
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