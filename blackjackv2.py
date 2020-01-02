import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random

"""
Todo: 
    Add error messages to basics functions. (?)
    Work on q learning stuff.
    Create a table that shows derived probabilities of hitting or sticking with
    a given hand value.
    
    Eventually: optimise basic functions
"""
#%%
#Basic functions for running a game of blackjack

def checkEqual1(iterator):
    """
    Function checks if elements of list are the same, used for building hand for 
    situation where a hand of ['A','A'] is dealt.
    """
    iterator = iter(iterator)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(first == rest for rest in iterator)

def hand_basket(dealtHand):
    """ Function creates  holder for all possible hands. Using dictionary as 
        place holder for cards. Keys are card faces and key values are number of 
        cards in hand 
    
    """
  
    if checkEqual1(dealtHand) == True:
        key = str(dealtHand[0])
        handBasket = dict({key: 2})
        pass
    
        #handBasket = handBasket.update(x)
    if checkEqual1(dealtHand) == False:
        key1 = str(dealtHand[0])
        key2 = str(dealtHand[1])
        handBasket = dict({key1:1,key2:1})
        #handBasket = handBasket.update(x)
        pass
    if len(dealtHand) == 1 : 
        key = str(dealtHand[0])
        handBasket.update(key = handBasket[key] + 1)
        pass 


#    


    return handBasket

     
#%%
def create_deck(*kwargs):
    """This function creates a deck of cards that is integer multiples of a standard
    deck of 52 cards. 
    
    Example: enter 1 returns a deck of 52 cards.
             enter 2 returns a deck of 104 cards.
                
    For infinite size deck enter arguement 'infinite',  WITH '' bounding the arguement
    
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
            
            finishedDeck = random.sample(deck, len(deck))
        
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
            
            finishedDeck = random.sample(deck, len(deck))
            
                                                                                                                  
        if size == 0:
            print("Size of deck must be greater than 0.")
            while size == 0: 
        
                size = int(input('Please enter an integer greater'
                                      ' than 0 for the deck size: '))
                
                numberOfEachCard = size * 4 * np.ones((1,13))
                for face in card_faces:
                    for no in range(int(numberOfEachCard[0,0])):
                        deck.append(face)                                                                       
                
                finishedDeck = random.sample(deck, len(deck)) # used to shuffle deck                                                                       
                                                                                       

    return finishedDeck  


#%%
def gameDealing(deck, *options):
    
    """A function to deal cards. 1 draw for agent (face up), 1 draw for dealer (face up)
    1 draw for agent (face up) and 1 draw for dealer (face down). """
    

    if (deck.sum(axis=1) == 0).all() == True: #check for enough cards in deck to draw from
        print("No cards in deck.")
        ########update this for finite case
        
        
        continueGame = input(str('Play another game? Enter yes or no : ')) 
        if continueGame == 'yes': # new episode starts!!! But we define the episodes 
                                  # with the deck size, so this might be irrelavent
            
            newDeck = create_deck(*kwargs) # need to replace *kwargs with deck size
                                           # from previous game, still trying to get 
                                           # handle on variable.
                                           
                                           
        if continueGame == 'no': # Epsiode ends; will have to add input reply 'no'
                                 # to terminate game since Reinforcement Learning Blackjack
                                 # document defines the episodes to be determined by 
                                 # the deck size. 
            pass
                               
    if options == 'newRound': # need to add options= 'newRound' at start of game 
    # One round 
        firstDrawAgent = list(deck[0]) 
        del deck[0]
        secondDrawDealer = list(deck[0])
        del deck[0]
        thirdDrawAgent = firstDrawAgent.append(deck[0])
        del deck[0]
        fourthDrawDealer = secondDrawDealer.append(deck[0]) # the unknown card, hidden information
        del deck[0]
        pass
# Allow agent to hit at least 5 times during round 
#
#       
    if options == 'hitMe1':
        # feeling lucky and taking another draw from the deck
        agentFirstDrawInRound = list(deck[0])
        del deck[0]
        thirdDrawAgent = thirdDrawAgent.append(agentFirstDrawInRound)
        pass 
    
    if options == 'hitMe2':
        # feeling even more lucky and taking another draw from the deck
        agentSecondDrawInRound = list(deck[0])
        del deck[0]
        thirdDrawAgent = thirdDrawAgent.append(agentSecondDrawInRound)
        pass
    
    if options == 'hitMe3':
        # Another one?; taking another draw from the deck
        agentThirdDrawInRound = list(deck[0])
        del deck[0]
        thirdDrawAgent = thirdDrawAgent.append(agentThirdDrawInRound)
        pass
    
    if options == 'hitMe4':
        # Really, again?
        agentForthDrawInRound = list(deck[0])
        del deck[0]
        thirdDrawAgent = thirdDrawAgent.append(agentForthDrawInRound)
        pass 
    
    if options == 'hitMe5':
        # No this has got to be the last one
        agentFithDrawInRound = list(deck[0])
        del deck[0]
        thirdDrawAgent = thirdDrawAgent.append(agentFithDrawInRound) 
        pass
    
    if options == 'stick':
        # add info of dealers hand to agents knowledge since second card 
        # will now be revealed.
        firstDrawAgent = list(deck[0]) 
        del deck[0]
        secondDrawDealer = list(deck[0])
        del deck[0]
        thirdDrawAgent = firstDrawAgent.append(deck[0])
        del deck[0]
        fourthDrawDealer = secondDrawDealer.append(deck[0]) # the unknown card, hidden information
        del deck[0]
        pass

    
    dealerHand = hand_basket(fourthDrawDealer)
    agentHand =  hand_basket(thirdDrawAgent)
    
    visibleCardFromAgentPerspective = { str(list(dealerHand.keys())[0]) : dealerHand[dealerHand.keys()[0]] } 
    
    
    gameHistoryAgentPerspective = {'2':0, '3':0, '4':0, '5':0,
                                   '6':0, '7':0, '8':0, '9':0,
                                   '10':0, 'J':0, 'Q':0, 'K':0,
                                   'A':0 }
    
    gameHistory = {'2':0, '3':0, '4':0, '5':0,
                   '6':0, '7':0, '8':0, '9':0,
                   '10':0, 'J':0, 'Q':0, 'K':0,
                   'A':0 }    

    gameHistory.update(dealerHand)
    gameHistory.update(agentHand)
    # dictionary below is for in round information as agent hits
    gameHistoryAgentPerspective.update(visibleCardFromAgentPerspective)
    gameHistoryAgentPerspective.update(agentHand)
    
    deckLength = len(deck)
        
        
        
        
    return agentHand, dealerHand, deck, gameHistory, gameHistoryAgentPerspective, deckLength 
    # The gameHistory will not be visible until the option stick has be chosen.
    # It is only the gameHistoryAgentPerspective that the agent will see until stick. 

#%%
    

def dealer(dealerHand, *options):
    """
    This will be a passive dealer, with 
    
    """
    if options == 'stick':
        


#%%
def agentsDecisionProcess(agentsGameKnowledge):
    
    '''
    Calculates score current, probabilities and recording choices in qTable .
    
    The Prior (discrete) Probability will be the probability before the dealer reveals his
    hidden card, that is the probability of each card. The Posterior (discrete) Probability
    will be the probability after revealing.The choices will be made based on the probabilities.
    These will make up the states. The value of the states will then be determined 
    by the score. These choices will then be updated after each episode using the Bellman equation.
    '''
    
    cardsInHand = agentsGameKnowledge['Cards in Hand']
    sizeOfDeckRemaining = agentsGameKnowledge['Size of Deck Remaining']
    history = agentsGameKnowledge['History'] # this history INCLUDES THE DEALERS HAND VISIBLE TO AGENT!
    
    for 
    priorCardsProbability = 4/52 * np.ones(1,13)  # prob distribution over ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    # using Bayes theorem to infer posteriorProb
    cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    probsOfCurrentHand = []
    for i in range(len(cardsInHand)):
       probsOfCurrentHand.append( priorCardsProbability[cards.index(cardsInHand)] )
        
    
    posteriorCardsProbability =     # can only be calculated after stick. 
    
    option = ['hitMe1', 'hitMe2','hitMe3', 'hitMe4'
             ,'hitMe5', 'stick', 'newRound', 'Aup', 'Adown']
    
    choice =['hitMe1', 'hitMe2','hitMe3', 'hitMe4'
             ,'hitMe5', 'stick', 'Aup', 'Adown']
    
    qTable = {'Prior Cards Probability':,
              'Posterior Cards Probability':,
              'Probability to Hit':,       # NOTICE THAT WE ONLY NEED ONE VALUE FOR THIS PROB, SINCE BINARY OPTION
              'Choice':,
              'score': }
    
    possValsCorrespondingToFaceValueOfCards = {'2':2, '3':3, '4':4, '5':5,
                                              '6':6, '7':7, '8':8, '9':9,
                                              '10':10, 'J':10, 'Q':10, 'K':10,
                                              'Aup':11 , 'Adown':1 }


    return option



#%%
def agent(agentHand, dealerHand, gameHistory,
          gameHistoryAgentPerspective, deck, deckLength):
    
    
    

    options = ['hitMe1', 'hitMe2','hitMe3', 'hitMe4'
               ,'hitMe5', 'stick', 'newRound']
    
    agentsGameKnowledge = {'Cards in Hand':agentHand,              # Make sure he only  
                           'Size of Deck Remaining':deckLength,    # sees first card of  
                           'History': gameHistoryAgentPerspective} # dealers hand until stick
                                                                   # hence different 
                                                                   # game histories,
                                                                   # will update with
                                                                   # game history once 
                                                                   # option stick has 
                                                                   # been selected
    
    option = agentsDecisionProcess(agentsGameKnowledge)

    if option == options[0]: # first hit
       deckLength, gameHistoryAgentPerspective, gameHistory, deck,  dealerHand, agentHand  = gameDealing(deck, options[0])
       
       agentsGameKnowledge['Cards in Hand'].update(agentHand)
       agentsGameKnowledge['Size of Deck Remaining'] = deckLength
       agentsGameKnowledge['History'].update(gameHistoryAgentPerspective)
    
    if option == options[1]: # second hit
       deckLength, gameHistoryAgentPerspective, gameHistory, deck,  dealerHand, agentHand = gameDealing(deck, options[1])
       
       agentsGameKnowledge['Cards in Hand'].update(agentHand)
       agentsGameKnowledge['Size of Deck Remaining'] = deckLength
       agentsGameKnowledge['History'].update(gameHistoryAgentPerspective)    

    if option == options[2]: #  third hit
       deckLength, gameHistoryAgentPerspective, gameHistory, deck,  dealerHand, agentHand = gameDealing(deck, options[2])
       
       agentsGameKnowledge['Cards in Hand'].update(agentHand)
       agentsGameKnowledge['Size of Deck Remaining'] = deckLength)
       agentsGameKnowledge['History'].update(gameHistoryAgentPerspective)
       
    if option == options[3]: #  forth hit
       deckLength, gameHistoryAgentPerspective, gameHistory, deck,  dealerHand, agentHand = gameDealing(deck, options[3])
       
       agentsGameKnowledge['Cards in Hand'].update(agentHand)
       agentsGameKnowledge['Size of Deck Remaining'] = deckLength
       agentsGameKnowledge['History'].update(gameHistoryAgentPerspective)
    
    if option == options[4]: #  Fith and final possible hit
       deckLength, gameHistoryAgentPerspective, gameHistory, deck,  dealerHand, agentHand = gameDealing(deck, options[4])
       
       agentsGameKnowledge['Cards in Hand'].update(agentHand)
       agentsGameKnowledge['Size of Deck Remaining'] = deckLength
       agentsGameKnowledge['History'].update(gameHistoryAgentPerspective)
       
    if option == options[5]: # stick
       deckLength, gameHistoryAgentPerspective, gameHistory, deck,  dealerHand, agentHand = gameDealing(deck, options[5])
       
       agentsGameKnowledge['Cards in Hand'].update(agentHand)
       agentsGameKnowledge['Size of Deck Remaining'] = deckLength
       agentsGameKnowledge['History'].update(gameHistory) # since at stick we enlighten the  <- WE OVERLAP GAMEHISTORY DIC WITH AGENTS KNOWLEDGE
                                                          # agent of the dealers card,
                                                          # which is information contained
                                                          # in the gameHistory, as well as 
                                                          # containing the information about
                                                          # his own hand. 
    
                                                          
    if option == options[6]: #  new round
       deckLength, gameHistoryAgentPerspective, gameHistory, deck,  dealerHand, agentHand = gameDealing(deck, options[6])
       
       agentsGameKnowledge['Cards in Hand'].update(agentHand)
       agentsGameKnowledge['Size of Deck Remaining'] = deckLength
       agentsGameKnowledge['History'].update(gameHistoryAgentPerspective)
       
      # Plan to use agents knowledge to make choices    
    
# needs to calculate posterior probabilities 
# include gambling amount, plot and animate shift in probability 


    
    # how many times can we possible hit during a round?
    # if option == 'stick':
        #score = sum(int(agentHand))**2
    # if option == 'hitMe'

    return options 
#%%





def game_start(D):
    """A function for drawing 2 cards from the deck into a newly generated hand."""
    hand = create_hand()
    #check for enough cards in deck to draw from
    if (D.sum(axis=1) <= 1).all() == True:
        print("Not enough cards in deck.")
        ########update this for finite case
        return (hand, D)
    else:
        #drawing 2 cards to player hand
        for i in range(0,2):
            #making sure card is available to be drawn
            test = D.sample(1,axis=1)
            while (test.sum(axis=1) == 0).all() == True:
                #idea for optimisation, sample from non zero elements
                test = D.sample(1,axis=1)
            #moving card quantity from deck to hand
            for cname in test.columns:
                hand[cname] += 1    
                D[cname] -= 1

        return (hand, D)

def check_value(hand):
    """This function returns the value of a current hand."""
    hand_val = 0
    card_vals = np.array([2,3,4,5,6,7,8,9,10,10,10,10,1])
    hand_val = int(np.sum(card_vals * hand, axis=1))
    #check if ace can be 11 instead of 1
    if hand_val <= 11 and (hand.loc[0,"A"] >= 1).all() == True:
        hand_val +=  10
    return hand_val

def Stand(score, hand):
    hand_val = check_value(hand)
    if hand_val <= 21:
        score += hand_val**2
        print("Game was won with a hand value of {}." .format(hand_val))
    else:
        score += 0
        print("Game was lost with a hand value of {}." .format(hand_val))
    return

#start on creating a Q table, idk how to construct it.
def create_ptable():
    """Creates an array with rows stick and hit with the probabilities of choosing
    those actions with a given hand value."""
    
    
    test_p = pd.DataFrame(np.zeros((2,18)), index=["Hit", "Stick"], columns=["4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21"])
    for cname in test_p.columns:
        a = np.random.randint(low=1,high=9, size=1)/10
        test_p.loc["Hit", cname] = a
        test_p.loc["Stick", cname] = 1-a
    return test_p

#%%
#not too sure about these
#Can you think of a better way to implement?
def create_qtable():
    q_out = {} # key: [(hand_value, ace in hand)][action] = value
    #Value of first 2 cards
    for i in range(4,22):
        #if there is an ace in the hand
        for j in [True, False]:
            if i == 21:
                q_out[(i,j)] = 1
            else:
                q_out[(i,j)] = 0
    return q_out
#%%
###########################ignore this part, testing out stuff
expect_val = [1,2,3,4,5,6,7,8,9,10,10,10,10]
n = len(expect_val)
prob_vals = [1,1,1,1,1,1,1,1,1,4]
m = len(prob_vals)
for i in range(n):
    expect_val[i] *= 1/n
for i in range(m):
    prob_vals[i] *= 1/n
print("Sum of probabilities is {}" .format(sum(prob_vals)))
#####################################################################
#%%
#need to clarify q update rule and then implement it
#added learning epxperiance value, unsure about how to properly implement it
def choose_action(hand_in, exp_val):
    hand_val = check_value(hand_in)
    if hand_val <= 11:
        act_out = 1
    elif exp_val > 1:
        act_out = exp_val
    else:
        act_out = 0
    return (act_out)

#need to get this function working, clarify the update rule
def update_qtable(hand_in, q_in):

    return q_out
#%%
#Doing all the stuff
#check to see if shit works basically
deck = create_deck(1)
p_hand, deck = game_start(deck)
print(check_value(p_hand))    
q_tab = create_qtable()
p_tab = create_ptable()