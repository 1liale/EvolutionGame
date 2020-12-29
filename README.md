# EvolutionGame

Explore using an evolutionary algorithm with ML 

Purpose:  
Create an AI that finds an optimized solution to a survival 
game (block jumping over obstacles) 

The block character is allowed 2 degrees of freedom
1. jump up and down
2. move forward and backward

The block(character)'s goal is to dodge incoming obstacles coming
from the right at random intervals and speeds

This project will combine the Genetic Algo(GA) with a neural network(NN)

Here we will only outline the input and output layers of NN:
1. The input layer will have 4 nodes
  a. Obstacle's direction vector from player (X)
  b. Obstacle's direction vector from player (Y)
  c. Obstacles's relative speed from player (X)
  d. Obstacles's relative speed from player (Y)
2.  the output layer will have 5 nodes
  a. Player Jumps
  b. Player Jumps while moving forward for t seconds
  c. Player Jumps while moving backward for t seconds
  d. Player moves forward
  e. Player moves backward

Overall, the project can be summarized into 8 steps
1. Create the game 
2. Decide on neural network architecture
3. Generate the initial population
4. Fitness function (to help select "fit" individuals)
5. Play the game and sort individuals based on their "fitness" scores
6. Using the "fittest" individuals from each population and generate the remaining population using Crossover and Mutation.
7. The new population/ generation is created
8. Go to step 5 and loop until the stopping criteria isn't satisfied anymore.

Below is a flowchart that can be used to help illustrate this process:

