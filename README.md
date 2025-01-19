# Pattern Matching

*Heavily* inspired by [Markov Junior](https://github.com/mxgmn/MarkovJunior), several programs based around 'Pattern Matching', taking a grid of coloured squares and procedurally re-colouring squares matching a given pattern to create images, animations or generate terrain.

## Programs

A program, a tree like structure of Nodes and Rules, is applied to a grid of coloured pixels to iteratively update via matching and replacing patterns.
<p align="center">
<img src="/Videos/voroni.gif" width="200">
<img src="/Videos/competition.gif" width="200">
<img src="/Videos/cellular_automata.gif" width="200">
<img src="/Videos/flowers_example_1.gif" width="200">
</p>

Rules contain an input and output pattern, and when run search the grid for matches to the input pattern before sampling one (or more) to replace with the output pattern. Additional settings control how many matches are sampled, the sampling distribution over matches, and the symmetries allowed when matching patterns.

Nodes allow the construction of more complex problems. They store a list of contents, Rules or even other Nodes, and apply them according to their type:

<img src="/Images/city.png" align="right" width="150">

- Sequential Nodes loop over contents in order
- Markov Nodes reset their loop after a change to the grid
- Limit Nodes loop a set number of times
- Random Nodes apply items randomly

(all Nodes terminate if a full pass over all contents makes no changes to the grid)

Combining the different types of Nodes and Rules allows a huge variety of programs as shown in the examples above of a voroni diagram, spreading regions, cellular automata and flower growth. Programs are easy to create and a few well selected Nodes and Rules can generate amazing images and patterns:

<p align="center">
<img src="/Images/single_river.png" width="100">
<img src="/Images/multiple_rivers.png" width="100">
<img src="/Images/river_example_1.png" width="100">
<img src="/Images/river_example_2.png" width="100">
<img src="/Images/river_example_3.png" width="100">
</p>

## Multi-grid

Current work on running a grid of multiple programs with the aim to implement genetic algorithms for evolution of programs

<img src="/Images/multigrid.png">

## Pathfinder

An incredibly simple maze exploration algorithm that guides a blue square thorugh a maze of white air and black walls to find a green goal.

The blue square moves randomly into white squares, leaving a red path behind, until it reaches a dead end at which point it backtracks to its previous square, leaving a grey path behind, and either continues exploring or backtracks further. Repeating these simple rules the square can explore all available squares in the maze and determine if it is possible to reach the green goal from the starting point.

## Credits

As stated initially this work is *heavily* inspired by MarkovJunior, a complete implementation of a probabilistic programming language that runs programs formed of re-write rules and performs inference by propagating constraints across a grid: MJ/mj.py is my own python implementation which explores the same idea. 
