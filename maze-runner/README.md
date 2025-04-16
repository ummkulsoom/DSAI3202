# Maze Explorer Game

A simple maze exploration game built with Pygame where you can either manually navigate through a maze or watch an automated solver find its way to the exit.

## Getting Started

### 1. Connect to Your VM

1. Open **<span style="color:red">Visual Studio Code</span>**
2. Install the "Remote - SSH" extension if you haven't already
3. Connect to your VM using SSH:
   - Press `Ctrl+Shift+P` to open the command palette
   - Type "Remote-SSH: Connect to Host..."
   - Enter your VM's SSH connection details
   - Enter your credentials when prompted

4. Install required VS Code extensions:
   - Press `Ctrl+Shift+X` to open the Extensions view
   - Search for and install "Python Extension Pack"
   - Search for and install "Jupyter"
   - These extensions will provide Python language support, debugging, and Jupyter notebook functionality

### 2. Project Setup

1. Create and activate a Conda environment:
```bash
# Create a new conda environment with Python 3.12
conda create -n maze-runner python=3.12

# Activate the conda environment
conda activate maze-runner
```

2. Install Jupyter and the required dependencies:
```bash
# Install Jupyter
pip install jupyter

# Install project dependencies
pip install -r requirements.txt
```

3. Open the project in Visual Studio Code and select the interpreter:
   - Press `Ctrl+Shift+P` to open the command palette
   - Type "Python: Select Interpreter"
   - Choose the interpreter from the `maze-runner` environment

## Running the Game

### Basic Usage
Run the game with default settings (30x30 random maze):
```bash
python main.py
```

### Manual Mode (Interactive)
Use arrow keys to navigate through the maze:
```bash
# Run with default random maze
python main.py

# Run with static maze
python main.py --type static

# Run with custom maze dimensions
python main.py --width 40 --height 40
```

### Automated Mode (Explorer)
The explorer will automatically solve the maze and show statistics:

#### Without Visualization (Text-only)
```bash
# Run with default random maze
python main.py --auto

# Run with static maze
python main.py --type static --auto

# Run with custom maze dimensions
python main.py --width 40 --height 40 --auto
```

#### With Visualization (Watch the Explorer in Action)
```bash
# Run with default random maze
python main.py --auto --visualize

# Run with static maze
python main.py --type static --auto --visualize

# Run with custom maze dimensions
python main.py --width 40 --height 40 --auto --visualize
```

### Jupyter Notebook Visualization
To run the maze visualization in Jupyter Notebook:

1. Make sure you have activated your virtual environment and installed all dependencies
2. Open the project in Visual Studio Code
3. Select the correct Python interpreter:
   - Press `Ctrl+Shift+P` to open the command palette
   - Type "Python: Select Interpreter"
   - Choose the interpreter from your created environment:
     - If using venv: Select the interpreter from `venv/bin/python` (Linux/Mac) or `venv\Scripts\python.exe` (Windows)
     - If using Conda: Select the interpreter from the `maze-runner` environment
4. Open the `maze_visualization.ipynb` notebook in VS Code
5. VS Code will automatically start a Jupyter server
6. Run all cells to see the maze visualization in action

Available arguments:
- `--type`: Choose between "random" (default) or "static" maze generation
- `--width`: Set maze width (default: 30, ignored for static mazes)
- `--height`: Set maze height (default: 30, ignored for static mazes)
- `--auto`: Enable automated maze exploration
- `--visualize`: Show real-time visualization of the automated exploration

## Maze Types

### Random Maze (Default)
- Generated using depth-first search algorithm
- Different layout each time you run the program
- Customizable dimensions
- Default type if no type is specified

### Static Maze
- Predefined maze pattern
- Fixed dimensions (50x50)
- Same layout every time
- Width and height arguments are ignored

## How to Play

### Manual Mode
1. Controls:
- Use the arrow keys to move the player (<span style="color:blue">blue circle</span>)
- Start at the <span style="color:green">green square</span>
- Reach the <span style="color:red">red square</span> to win
- Avoid the <span style="color:black">black walls</span>

### Automated Mode
- The explorer uses the right-hand rule algorithm to solve the maze
- Automatically finds the path from start to finish
- Displays detailed statistics at the end:
  - Total time taken
  - Total moves made
  - Number of backtrack operations
  - Average moves per second
- Works with both random and static mazes
- Optional real-time visualization:
  - Shows the explorer's position in <span style="color:blue">blue</span>
  - Updates at 30 frames per second
  - Pauses for 2 seconds at the end to show the final state

## Project Structure

```
maze-runner/
├── src/
│   ├── __init__.py
│   ├── constants.py
│   ├── maze.py
│   ├── player.py
│   ├── game.py
│   ├── explorer.py
│   └── visualization.py
├── main.py
├── maze_visualization.ipynb
├── requirements.txt
└── README.md
```

## Code Overview

### Main Files
- `main.py`: Entry point of the game. Handles command-line arguments and initializes the game with specified parameters.
- `requirements.txt`: Lists all Python package dependencies required to run the game.

### Source Files (`src/` directory)
- `__init__.py`: Makes the src directory a Python package.
- `constants.py`: Contains all game constants like colors, screen dimensions, cell sizes, and game settings.
- `maze.py`: Implements maze generation using depth-first search algorithm and handles maze-related operations.
- `player.py`: Manages player movement, collision detection, and rendering of the player character.
- `game.py`: Core game implementation including the main game loop, event handling, and game state management.
- `explorer.py`: Implements automated maze solving using the right-hand rule algorithm and visualization.
- `visualization.py`: Contains functions for maze visualization.

## Game Features

- Randomly generated maze using depth-first search algorithm
- Predefined static maze option
- Manual and automated exploration modes
- Real-time visualization of automated exploration
- Smooth player movement
- Collision detection with walls
- Win condition when reaching the exit
- Performance metrics (time and moves) for automated solving

## Development

The project is organized into several modules:
- `constants.py`: Game constants and settings
- `maze.py`: Maze generation and management
- `player.py`: Player movement and rendering
- `game.py`: Game implementation and main loop
- `explorer.py`: Automated maze solving implementation and visualization
- `visualization.py`: Functions for maze visualization

## Getting Started with the Assignment

Before attempting the questions below, please follow these steps:

1. Open the `maze_visualization.ipynb` notebook in VS Code
2. Run all cells in the notebook to:
   - Understand how the maze is generated
   - See how the explorer works
   - Observe the visualization of the maze solving process
   - Get familiar with the statistics and metrics

This will help you better understand the system before attempting the questions.

## Student Questions

### Question 1 (10 points)
Explain how the automated maze explorer works. Your answer should include:
1. The algorithm used by the explorer
2. How it handles getting stuck in loops
3. The backtracking strategy it employs
4. The statistics it provides at the end of exploration

To answer this question:
1. Run the explorer both with and without visualization
2. Observe its behavior in different maze types
3. Analyze the statistics it provides
4. Read the source code in `explorer.py` to understand the implementation details

Your answer should demonstrate a clear understanding of:
- The right-hand rule algorithm
- The loop detection mechanism
- The backtracking strategy
- The performance metrics collected

### Answer to Question 1

The automated maze explorer uses a sophisticated combination of the right-hand rule algorithm with backtracking to solve mazes. Through testing with different maze configurations (random, static, and varying sizes), we can observe the following key aspects:

1. **Algorithm Used by the Explorer**
The explorer implements the right-hand rule algorithm with the following characteristics:
- Always prioritizes turning right first when possible
- If right is blocked, tries to move forward
- If forward is blocked, attempts to turn left
- If all options are blocked, turns around
- Maintains a consistent direction preference throughout exploration
- Keeps track of visited positions to avoid redundant exploration

2. **Loop Handling Mechanism**
The explorer has a robust loop detection and handling system:
- Maintains a `move_history` deque that tracks the last 3 positions
- Uses the `is_stuck()` method to detect loops by checking if the last 3 moves are identical
- When a loop is detected, it triggers the backtracking mechanism
- This prevents the explorer from getting stuck in infinite loops
- Allows the explorer to explore alternative paths effectively

3. **Backtracking Strategy**
The explorer employs an intelligent backtracking strategy:
- Uses `find_backtrack_path()` to search backwards through move history
- Looks for positions with multiple available choices
- Returns to the last position with multiple options
- Resets the backtrack path after finding a new route
- Increments the backtrack counter for performance tracking
- Continues exploration from the new position with fresh options

4. **Statistics and Performance Metrics**
The explorer provides comprehensive statistics through the `print_statistics()` method:
- Total time taken to solve the maze
- Total number of moves made
- Number of backtrack operations performed
- Average moves per second

From our test runs, we observed:
- Random Maze (30x30):
  - Time: 11.81 seconds
  - Moves: 350
  - No backtrack operations
- Static Maze:
  - Time: 42.98 seconds
  - Moves: 1279
  - Average moves per second: 29.76
- Large Random Maze (50x50):
  - Time: 17.95 seconds
  - Moves: 533
  - No backtrack operations

These statistics demonstrate the explorer's adaptability to different maze configurations and its efficiency in finding solutions.

### Question 2 (30 points)
Modify the main program to run multiple maze explorers simultaneously. This is because we want to find the best route out of the maze. Your solution should:
1. Allow running multiple explorers in parallel
2. Collect and compare statistics from all explorers
3. Display a summary of results showing which explorer performed best

*Hints*:
- To get 20 points, use use multiprocessing.
- To get 30 points, use MPI4Py on multiple machines.
- Use Celery and RabbitMQ to distribute the exploration tasks. You will get full marks plus a bonus.
- Implement a task queue system
- Do not visualize the exploration, just run it in parallel
- Store results for comparison

### MPI Implementation (For 30 Points)

To run the maze solver using MPI across multiple machines:

1. First, ensure you have MPI installed on all machines:
```bash
# On Ubuntu/Debian
sudo apt-get install mpich

# On CentOS/RHEL
sudo yum install mpich-devel

# On Windows (using conda)
conda install mpi4py
```

2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

3. Create a hostfile (e.g., `hostfile.txt`) listing your machines:
```
localhost slots=4
machine1 slots=4
machine2 slots=4
```

4. Run the distributed maze solver:
```bash
# Run with 8 processes across machines listed in hostfile
mpirun -n 8 -f hostfile.txt python main_mpi.py --type static

# Run locally with 4 processes
mpirun -n 4 python main_mpi.py --type random --width 50 --height 50
```

The MPI implementation offers several advantages:
1. True distributed computing across multiple machines
2. Efficient communication using MPI's optimized protocols
3. Better scalability for large numbers of explorers
4. Reduced memory usage per machine

Key Features:
- Master process (rank 0) creates and broadcasts the maze
- Each process runs an independent explorer
- Results are gathered and analyzed by the master process
- Detailed statistics for each explorer and overall performance
- Works with both random and static mazes
- Supports custom maze dimensions

Example output:
```
Starting distributed maze solving with 4 processes...

=== Distributed Exploration Results ===
Explorer 1 (Process 0):
Time taken: 0.15 seconds
Number of moves: 1279
Backtrack operations: 0

Explorer 2 (Process 1):
Time taken: 0.14 seconds
Number of moves: 1285
Backtrack operations: 2

Explorer 3 (Process 2):
Time taken: 0.16 seconds
Number of moves: 1290
Backtrack operations: 1

Explorer 4 (Process 3):
Time taken: 0.15 seconds
Number of moves: 1282
Backtrack operations: 1

=== Summary Statistics ===
Total execution time: 0.18 seconds
Average moves per explorer: 1284.0
Average time per explorer: 0.15 seconds

=== Best Performer ===
Explorer 1 (Process 0) found the best solution:
Time: 0.15 seconds
Moves: 1279
```

### Question 3 (10 points)
Analyze and compare the performance of different maze explorers on the static maze. Your analysis should:

1. Run multiple explorers (at least 4 ) simultaneously on the static maze
2. Collect and compare the following metrics for each explorer:
   - Total time taken to solve the maze
   - Number of moves made
   - *Optional*:
     - Number of backtrack operations

3. What do you notice regarding the performance of the explorers? Explain the results and the observations you made.

### Question 4 (20 points)
Based on your analysis from Question 3, propose and implement enhancements to the maze explorer to overcome its limitations. Your solution should:

1. Identify and explain the main limitations of the current explorer:

2. Propose specific improvements to the exploration algorithm:

3. Implement at least two of the proposed improvements:

Your answer should include:
1. A detailed explanation of the identified limitations
2. Documentation of your proposed improvements
3. The modified code with clear comments explaining the changes

### Question 5 (20 points)

Compare the performance of your enhanced explorer with the original:
   - Run both versions on the static maze
   - Collect and compare all relevant metrics
   - Create visualizations showing the improvements
   - Document the trade-offs of your enhancements
Your answer should include:
1. Performance comparison results and analysis
2. Discussion of any trade-offs or new limitations introduced

### Final points 6 (10 points)
1. Solve the static maze in 150 moves or less to get 10 points.
2. Solve the static maze in 135 moves or less to get 15 points.
3. Solve the static maze in 130 moves or less to get 100% in your assignment.

### Bonus points
1. Fastest solver to get top  10% routes (number of moves)
2. Finding a solution with no backtrack operations
3. Least number of moves.