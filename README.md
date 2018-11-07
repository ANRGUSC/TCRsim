# Votesim

Votesim is a Token Curated Registry (TCR) simuation in which we evaluate a token-inflation mechanism for enhancing engagement in TCRs. In the simulation, we are able to change the parameters of the TCR (number of voters, number of items in TCR, number of tokens, inflation rate) to view how different parameters effect the overall value of a TCR. The simulation generates items and voters and simulates a voting process based on the likeliness of voting and the probaility of voting correctly. It then generates 3 plots that aid in viewing the results. 

## Getting Started

Please follow these instructions to get the project up and running on your local machine.

### Prerequisites

Python 

```
brew install python
```

### Installing

A step by step series of examples that tell you how to get a development env running

Clone the project onto your local machine

```
git clone https://github.com/ANRGUSC/votesim.git
```

Change into the directory votesim and run 
```
python Simulation.py
```

You can either change the parameters through the command line prompt when you first run the simulation or you can go into Simulation.py and change the member variables of the Simuation class to appropriate numbers. 