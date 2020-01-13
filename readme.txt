agent:
This script contains a class that describes agent's decision process, i.e. how it chooses it's
action and the updating of the Q values for a given policy search method.

dealing:
This script contain the class of the Blackjack game play. The actions taken by the agent 
interact with an instance of this class in a self-perpetuating manner; you only need to call
the newRound method to begin the game play. All other aspects of the game play; score, ace count etc,
will be determined from the agent's actions and the class atributes update as a consequence.   

training:
This script contains a function that trains the agent for a given deck size, method, exploration and exploitation
period. A count of wins, losses and draws for the exploration and exploitation period is kept and returned. 

trainingWithAllMethods:
This script trains the agent for ten different regimes, 1-10 decks, for each policy search method. The Q-table 
for these are then saved as csv files. 

validating: 
This script allows one to reduce the parameter space and request the agent plays the dealer given the 
optimal policy found from the corresponding QTables. Please make sure that the compressed QTables file
is extracted and placed in the working directory when trying to run this script.

QTables:
This compressed file contains the QTables for the various regimes the agent was trained on. Please unzip this
file and place it in the working directory when attempted to run the validating.py script.   