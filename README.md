# Ant Colony Algorithm Visualizer

This project is a personal experiment created in my free time. It visualizes the Ant Colony Optimization (ACO) algorithm, which is inspired by the natural path-finding behavior of ants. The algorithm simulates how ants find the shortest path between their colony and a food source, using pheromone trails to influence their decisions.

## Features
- **Real-time visualization** of the Ant Colony Optimization algorithm.
- Ability to **tune parameters** by modifying the `App` class in `app.py`.
- Simple **keyboard controls** to start, stop, and reset the simulation.

## How it Works
The ACO algorithm mimics the way ants search for paths. Each ant in the simulation leaves a pheromone trail as it moves. Over time, shorter paths accumulate stronger pheromone concentrations, encouraging other ants to follow them. This visualization helps to understand how the algorithm converges towards the optimal path.

## Getting Started

### Prerequisites
- **Python 3.x** is required to run the project.
- Ensure you have all necessary Python packages installed. You can install dependencies using `pip`:

### Controls
- **s** to start, or restart simulation.
- **spacebar** to stop simulation.
```bash
pip install -r requirements.txt