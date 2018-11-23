# TCRsim

TCRsim is a Token Curated Registry (TCR) simuation, developed in order to evaluate a token-inflation mechanism for enhancing engagement in TCRs. In the simulation, we are able to change the parameters of the TCR (number of voters, number of items in TCR, number of tokens, inflation rate) to view how different parameters effect the overall value of a TCR. Setting the inflation rate to zero is equivalent to simulating a traditional TCR. The simulation generates items and voters and simulates a voting process based on the likeliness of voting and the probability of voting correctly. In these simulations, voters are divided into four classes based on whether they are engaged or not and whether they are informed or not. As an output, TCRsim logs the outcome of each item and the tokens belonging to each voter, and generates 3 plots that aid in viewing the results: these plots show a) the average wealth among each voter class b) total tokens in each voter class and c) TCR value over the course of multiple voting periods. 

## Getting Started

Please follow these instructions to get the project up and running on your local machine.

### Prerequisites

Python 2.7

```
brew install python
```

### Installing

A step by step series of examples that tell you how to get a development env running

Clone the project onto your local machine

```
git clone https://github.com/ANRGUSC/TCRsim.git
```

Change into the directory votesim and run 
```
python Simulation.py
```

You can either change the parameters through the command line prompt when you first run the simulation or you can go into Simulation.py and change the member variables of the Simuation class to appropriate numbers. 

### Reference
This simulator was used to produce results for the following paper that is included in the paper folder of this repository:
Yi Lucy Wang, Bhaskar Krishnamachari, "Enhancing Engagement in Token-Curated Registries via an Inflationary Mechanism," preprint manuscript, November 2018. 
