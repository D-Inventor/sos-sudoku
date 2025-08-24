# SOS Sudoku
I get stuck on my sudokus sometimes, but I don't want some program to give away the answer; that's boring.
This small script analyses a sudoku and points out cells that I should be able to figure out.

This is a little hobby project that I built on the side, because I thought it would be fun. If it's useful to you, feel free to steal. I don't do support.

## What does it look like?
For example, given [sudoku 35](./35.txt), the console gives this output:

```
┏━━━━━━━┳━━━━━━━┳━━━━━━━┓
┃ 4 9 1 ┃ 8 3 7 ┃   5   ┃
┃ 5 6 3 ┃ 9     ┃ 4 8 7 ┃
┃ 7 8 2 ┃     4 ┃ 9     ┃
┣━━━━━━━╋━━━━━━━╋━━━━━━━┫
┃ 9 7   ┃     8 ┃       ┃
┃ 8 2> <┃ 1 7   ┃   9 5 ┃
┃ 1 3   ┃ 2   9 ┃ 8 7   ┃
┣━━━━━━━╋━━━━━━━╋━━━━━━━┫
┃ 6 5 8 ┃ 7     ┃     9 ┃
┃ 3   9 ┃   8 5 ┃ 7 2   ┃
┃ 2   7 ┃  > <  ┃ 5   8 ┃
┗━━━━━━━┻━━━━━━━┻━━━━━━━┛
```

The `> <` symbols point to cells that can be inferred from the current state of the puzzle

## Things I still want to add (but haven't felt like yet):
- Inference rules
  - Extrapolate blocks, rows and columns
  - X-wing
  - Y-wing
  - ... I don't know any other rules right now, but there are probably more rules
- Console UI
  - Edit sudoku in the console
  - Show a list of used inference rules that were used to find the hint
 
I don't really do python often, so I don't expect to be able to do all this, but that's whatever. This is a hobby project after all.
