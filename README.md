# Blackjack: Reinforcement Learning Approach
________________________________________________________________________________________________________________________________________

## Overview 
________________________________________________________________________________________________________________________________________

This repository contains the class of an agent whom is trained in a simplified Blackjack environment. This environment is described
by the dealing class. The training of the agent is conducted using three different policy iteration approaches:
* Q-Learning (QL) 
* State action reward state action (SARSA)
* Tempoal Difference (TD) 
<br>
The results of training for 10000 games, with a split of 5000 games of exploration and 5000 of exploitation, over each policy iteration method is presented below. 
<br>
<img src = "https://github.com/akinolawilson/Reinforcement-Learning-in-Blackjack/blob/master/winLossDraw.png?raw=true">
<br>
Averaging over each policy search method and multiples of the standard deck trained upon, the agent optimised their decision process to achieve a win, draw and loss rate of 48.37,  33.21  and 20.91 percent respectively in terms of dealer-agent interactions.

## Environment Details 
________________________________________________________________________________________________________________________________________

The game play is simplified in the sense that the dealer will not attempt to draw any more cards after 
the initial two at the start of each round. The agent is then trained to achieved the highest in round score, <a href="https://www.codecogs.com/eqnedit.php?latex=\xi" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\xi" title="\xi" /></a>, is determined as 
<br>
<a href="https://www.codecogs.com/eqnedit.php?latex=\xi&space;=&space;\big(&space;\sum&space;c_{i}&space;\big)^2" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\xi&space;=&space;\big(&space;\sum&space;c_{i}&space;\big)^2" title="\xi = \big( \sum c_{i} \big)^2" /></a>.
<br>
If the agent's collective hand value,
<br>
<a href="https://www.codecogs.com/eqnedit.php?latex=\sum&space;c_{i}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\sum&space;c_{i}" title="\sum c_{i}" /></a>,
<br>
where the <a href="https://www.codecogs.com/eqnedit.php?latex=c_{i}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?c_{i}" title="c_{i}" /></a>'s represent the numerical value of the agent's in hand cards is greater than the dealers. Otherwise, the in round score was set to 
<br>
<a href="https://www.codecogs.com/eqnedit.php?latex=\xi&space;=&space;0" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\xi&space;=&space;0" title="\xi = 0" /></a>.
<br>
The dynamics of the game play are as follows: Two cards a dealt from a pre-specified multiple of the standard deck of 52 cards to the agent and passive dealer. Then the agent is able to choose from the action space
<br>
<a href="https://www.codecogs.com/eqnedit.php?latex=\mathbb{A}(s)$&space;=&space;$\{Hit,Stick\}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\mathbb{A}(s)$&space;=&space;$\{Hit,Stick\}" title="\mathbb{A}(s)$ = $\{Hit,Stick\}" /></a>.
<br>
The agent is encouraged to maximise the over game total score defined as
<br>
<a href="https://www.codecogs.com/eqnedit.php?latex=\Xi&space;=&space;\sum\limits_{\substack{i}}^{S}&space;\xi_{i}$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\Xi&space;=&space;\sum\limits_{\substack{i}}^{S}&space;\xi_{i}$" title="\Xi = \sum\limits_{\substack{i}}^{S} \xi_{i}$" /></a>,
<br>
where S is the total number of times the agent submitted to stick. 
<br>
<br>
The figure below shows the agent's average achieved over game quadratic score,<a href="https://www.codecogs.com/eqnedit.php?latex=\Xi" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\Xi" title="\Xi" /></a> , for the different deck multiples and policy iteration methods.
<br>
<img src ="https://github.com/akinolawilson/Reinforcement-Learning-in-Blackjack/blob/master/optimalScore1to10games.png?raw=true">

## File Details 
________________________________________________________________________________________________________________________________________


```agent.py```:
<br>
This script contains a class that describes agent's decision process, i.e. how it chooses it's
action and the updating of the Q values for a given policy search method.

```dealing.py```:
<br>
This script contain the class of the Blackjack game play. The actions taken by the agent 
interact with an instance of this class in a self-perpetuating manner; you only need to call
the newRound method to begin the game play. All other aspects of the game play; score, ace count etc,
will be determined from the agent's actions and the class  attributes update as a consequence.   

```training.py```:
<br>
This script contains a function that trains the agent for a given deck size, method, exploration and exploitation
period. A count of wins, losses and draws for the exploration and exploitation period is kept and returned. 

```trainingWithAllMethods.py```:
<br>

This script trains the agent for ten different regimes, 1-10 decks, for each policy search method. The Q-table 
for these are then saved as csv files. 

```validating.py```: 
<br>
This script allows one to reduce the parameter space and request the agent plays the dealer given the 
optimal policy found from the corresponding QTables. Please make sure that the compressed QTables file
is extracted and placed in the working directory when trying to run this script.

```QTables.zip```:
<br>
This compressed file contains the QTables for the various regimes the agent was trained on and can be downloaded <a href="https://drive.google.com/file/d/1FktDulCeBNC99lXllJE6ht3bbR1fpAuw/view?usp=sharing">here</a> . Please unzip this
file and place it in the working directory when attempted to run the ```validating.py``` script. 

### Further Development and Reading
________________________________________________________________________________________________________________________________________

The next task is to separate the dealer from the dealing class into its own class. This will allow implementing dealer actions. Furthermore, there is a clear necessity to find ways to reduce the Q Tables. For a formal review of this project please find my
<a href="https://www.researchgate.net/publication/338992214_Blackjack_Reinforcement_Learning_Approaches_to_an_Incomplete_Information_Game">ResearchGate</a> account. 
