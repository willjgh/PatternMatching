# Pattern Matching

*Heavily* inspired by [Markov Junior](https://github.com/mxgmn/MarkovJunior) I have designed several programs based around 'Pattern Matching', taking a grid of coloured squares and procedurally re-colouring squares matching a given pattern to create images or complete tasks.

## MJ/mj.py

The 2 key components are the grid: coloured squares (referred to by letters) which represent the current state, and the program: a nested collection of Nodes and Rules which are applied to the grid to update the state.

Rules are the fundamental building blocks, consisting of an input and output pattern and settings on how they are applied. When the Rule is run, it searches the grid for the location of all patterns matching the input pattern and selects one or more (settings) to replace by the output pattern. The simplest program consists of a single rule with input pattern 'B' and output pattern 'W' which is repeatedly applied to a grid initialised with all black squares ('B' in letters), replacing them one by one until ending with a grid of all white squares:

(add example of fill)

Nodes allow the building of more complex programs and consist of a list of contents: Rules or even other Nodes, which are applied in different orders according to type:
- Sequential Nodes simply run each of their items in order
- Markov Nodes run items in order until a change to the grid, at which point they 'reset' and run the first item (memory-less)
- Limit Nodes run each item a specified number of times (regardless of whether they make any changes to the grid)
- Random Nodes run items in a random order (unexpected I know)
With the exception of the Limit type, Nodes keep running until a full pass over all contents makes no changes to the grid

An example of program using Nodes is 'Repeating-Voroni':

(add example of repeating-voroni)

Red and white seeds are spawned on a black grid, each of which exapands to fill the space until all squares fade to black and the process repeats. The program is a nesting of Sequential Nodes:

Sequential Node(
  Rule: spawn Red seed
  Rule: spawn White seed
  Sequential Node(
    Rule: Red expands into Black
    Rule: White expands into Black
  )
  Sequential Node(
    Rule: Red turns to Black
    Rule: White turns to Black
  )
)

The combination of different types of Nodes and Rules allows a huge variety of programs from the random spreads seen above to chess movements, flowers, creatures and houses:

(add example of flowers, chess and crawlers, etc)


## Pathfinder

An incredibly simple maze exploration algorithm that guides a blue square thorugh a maze of white air and black walls to find a green goal.

(add example of pathfinder program)

The blue square moves randomly into white squares, leaving a red path behind, until it reaches a dead end at which point it backtracks to its previous square, leaving a grey path behind, and either continues exploring or backtracks further. Repeating these simple rules the square can explore all available squares in the maze and determine if it is possible to reach the green goal from the starting point.

## Credits

As stated initially this work is *heavily* inspired by MarkovJunior, a complete implementation of a probabilistic programming language that runs programs formed of re-write rules and performs inference by propagating constraints across a grid: MJ/mj.py is my own python implementation which explores the same idea. 
