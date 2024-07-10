# TITLE: 3d board searcher visualization
# AUTHOR: Pack
# CREATION DATE: 7/9/2024
# LAST UPDATE: 7/10/2024
# SUMMARY: Run file and press start to start the visualization.  Change any of the constants based on preference.
#           Although this agent has access to the actual board the algorithm would be able to work blind, and without knowing what cord it is on
#           I choose to allow this version to have full access as it is just a visualization of the concept.
#           This method of searching would work past the 3 dimensions shown and would be able to search an array of infinite dimensions.
#           This method also works if movements can be blocked, but not if movements are irrevisible.

import tkinter as tk
import time
from threading import *
from Board import *
# Constants
DELAY = 0.1
CELL_SIZE = 60
COLOR_EMPTY = "white"
COLOR_WALL = "gray26"
COLOR_PLAYER = "gold2"
COLOR_VISITED = "light goldenrod"
COLOR_NA = "brown"

# Class for Visualization of 3d search algorithm
class GridDisplay(tk.Tk):
    def __init__(self):
        super().__init__()
        # Variable setup
        self.done = False
        self.score = 0
        self.steps = 0
        self.progress = 0
        self.path = []
        self.create_grid()
        self.create_layout()
        # Create list to allow squares to be updated without fully reloading each time
        self.rectangles = {}
        self.create_buttons()
        self.draw_grid()


    # Function to set maxScore, and create grid and starting point
    # Calls board function to create board
    # Called by init and reset
    def create_grid(self):
        # Create board
        self.b = board()
        # Set maxScore
        self.maxScore = self.b[1]
        # Clean variable b to not include max score
        self.b = self.b[0]
        # Chose starting point
        n = [random.randint(0,maxZ-1),random.randint(0,maxY-1),random.randint(0,maxX-1)]
        while self.b[n[0]][n[1]][n[2]] != 0:
            n = [random.randint(0,maxZ-1),random.randint(0,maxY-1),random.randint(0,maxX-1)]
        # Update board to have character at the starting point
        self.b[n[0]][n[1]][n[2]] = 5
        # Set agent location
        self.x,self.y,self.z = n[2],n[1],n[0]


    # Function that creates the layout for the display
    # Called by init
    def create_layout(self):
        # Create layout for display
        # Set display to 2d array based on what floor agent is on
        grid = self.b[self.z]
        self.title("Simple Agent")
        self.canvas = tk.Canvas(self, width=len(grid[0]) * CELL_SIZE, height=len(grid) * CELL_SIZE)
        self.canvas.pack()  # Canvas
        self.floor_label = tk.Label(self, text="Floor: 0", font=("Helvetica", 14))
        self.floor_label.pack() # Floor label
        self.score_frame = tk.Frame(self)
        self.score_frame.pack(side="top", pady=(10, 0))  # Frame for scoreboard
        self.steps_label = tk.Label(self.score_frame, text="Steps: 0", font=("Helvetica", 14))
        self.steps_label.pack(side="left", padx=(10, 5)) # Steps label
        self.score_label = tk.Label(self.score_frame, text="Score: 0", font=("Helvetica", 14))
        self.score_label.pack(side="left", padx=(10, 5)) # Score label
        self.progress_label = tk.Label(self.score_frame, text="Progress: 0", font=("Helvetica", 14))
        self.progress_label.pack(side="left", padx=(10, 5)) # Estimated progress based on blind agent prediction
        self.score2_frame = tk.Frame(self)
        self.score2_frame.pack()    # Frame for second layer of scoreboard
        self.max_label = tk.Label(self.score2_frame, text=f"Max Score: {self.maxScore}", font=("Helvetica", 14))
        self.max_label.pack(side="left", padx=(10, 5))   # Max score label
        self.act_progress_label = tk.Label(self.score2_frame, text="Actual Progress: 0", font=("Helvetica", 14))
        self.act_progress_label.pack(side="left", padx=(10, 5)) # Actual progress based on number of steps

    # Function that creates buttons
    # Called by init
    def create_buttons(self):
        self.start_frame = tk.Frame(self)
        self.start_frame.pack(side="top", pady=(10, 0))  # Frame for start and step buttons
        self.start_button = tk.Button(self.start_frame, text="Start", command=self.threading, width=10, height=3)
        self.start_button.pack(side="left", padx=(10, 5))  # Start button
        self.step_button = tk.Button(self.start_frame, text="Step", command=self.step, width=10, height=3)
        self.step_button.pack(side="left", padx=(10, 5))  # Step button
        self.end_frame = tk.Frame(self) # Frame for Restart and Floor up/down buttons
        self.restart_button = tk.Button(self.end_frame, text="Restart", command=self.reset, width=10, height=3)
        self.restart_button.pack(side="left", padx=(10, 5))  # Restart button
        self.floorUp_button = tk.Button(self.end_frame, text="Floor up", command=self.floorUp, width=10, height=3)
        self.floorUp_button.pack(side="left", padx=(10, 5))  # Floor up button
        self.floorDown_button = tk.Button(self.end_frame, text="Floor down", command=self.floorDown, width=10, height=3)
        self.floorDown_button.pack(side="left", padx=(10, 5))  # Floor down button

    # Function that displays the grid
    # Called by init, reset, floorUp/floorDown, and ascend/descend
    def draw_grid(self):
        # Set grid to the current floor
        grid = self.b[self.z]
        self.canvas.delete("all")  # Clear previous drawings
        for row in range(len(grid)):
            # Clear row
            self.rectangles[row] = {}
            for col in range(len(grid[0])):
                # Get position for tile
                x1, y1 = col * CELL_SIZE, row * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                # Set color based on tile identity
                if grid[row][col] == 8:
                    fill_color = COLOR_WALL
                elif grid[row][col] == 0:
                    fill_color = COLOR_EMPTY
                elif grid[row][col] == 5:
                    fill_color = COLOR_PLAYER
                elif grid[row][col] == 9:
                    fill_color = COLOR_NA
                else:
                    fill_color = COLOR_VISITED
                # Create tile and add to dictionary of tiles for cleaner updates
                self.rectangles[row][col] = self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="black")
        # Update floor label
        self.floor_label.config(text=f"Floor: {self.z}")

    # Function that uses multi-threading one thread runs display other handles algorithm
    # Calls start function to start the algorithm
    # Called by pressing the start button
    def threading(self):
            t1=Thread(target=self.start) 
            t1.start()

    # Function for starting the algorithm to auto run
    # Called by threading
    # Calls step function until complete
    def start(self):
        # Hide start and stop button
        self.start_frame.pack_forget()
        # Run step until done then kills the thread
        while True:
            time.sleep(DELAY)
            self.step()
            if self.done:
                break

    # Function for resetting the visualization
    # Called by pressing the reset button
    # Calls create_grid and draw_grid
    def reset(self):
        # Reset variables
        self.score = 0
        self.steps = 0
        self.done = False
        # Hide end buttons and show start buttons
        self.end_frame.pack_forget()
        self.start_frame.pack()
        # Create and display grid
        self.create_grid()
        self.draw_grid()
        # Update max score
        self.max_label.config(text=f"Max Score: {self.maxScore}")

    # Function for running one step of the algorithm
    # Called by start or by pressing the step button
    # Calls movement functions
    def step(self):
        # Empty squares are squares that haven't been visited and are not walls
        # If up is in bounds and is a empty square: 
        # Update score/steps, and move up and push down to path stack
        if self.y-1 >= 0 and self.b[self.z][self.y-1][self.x] ==0:
            self.score+=1
            self.steps +=1
            self.path.append("down")
            self.move_character_up()
        # If down is in bounds and is a empty square: 
        # Update score/steps, and move down and push up to path stack
        elif self.y+1 < maxY and self.b[self.z][self.y+1][self.x] ==0:
            self.score+=1
            self.steps +=1
            self.path.append("up")
            self.move_character_down()
        # If right is in bounds and is a empty square: 
        # Update score/steps, and move right and push left to path stack
        elif self.x+1 < maxX and self.b[self.z][self.y][self.x+1] ==0:
            self.score+=1
            self.steps +=1
            self.path.append("left")
            self.move_character_right()
        # If up is in bounds and is a empty square: 
        # Update score/steps, and move left and push right to path stack
        elif self.x-1 >= 0 and self.b[self.z][self.y][self.x-1] ==0:
            self.score+=1
            self.steps +=1
            self.path.append("right")
            self.move_character_left()
        # If up is in bounds and is a empty square: 
        # Update score/steps, and move up a floor and push descend to path stack
        elif self.z+1 < maxZ and self.b[self.z+1][self.y][self.x] ==0:
            self.score+=1
            self.steps +=1
            self.path.append("descend")
            self.move_character_ascend()
        # If up is in bounds and is a empty square: 
        # Update score/steps, and move down a floor and push ascend to path stack
        elif self.z-1 >= 0 and self.b[self.z-1][self.y][self.x] ==0:
            self.score+=1
            self.steps +=1
            self.path.append("ascend")
            self.move_character_descend()
        # If no scoring moves are available pop from path stack and move accordingly
        elif len(self.path) > 0:
            # Update steps
            self.steps +=1
            move = self.path.pop()
            if move == "up":
                self.move_character_up()
            elif move == "down":
                self.move_character_down()
            elif move == "left":
                self.move_character_left()
            elif move == "right":
                self.move_character_right()
            elif move == "ascend":
                self.move_character_ascend()
            else:
                self.move_character_descend()
        # If back at the start and can't score board is complete
        else:
            # Update done variable and displays end buttons
            self.done = True
            self.end_frame.pack(side="top", pady=(10, 0))  # Restart and Floor up/down buttons
        # Update scoreboard
        self.score_label.config(text=f"Score: {self.score}")
        self.steps_label.config(text=f"Steps: {self.steps}")
        self.progress_label.config(text=f"Progress: {((self.steps-self.score)* 100 // self.score )}")
        self.act_progress_label.config(text=f"Actual Progress: {self.steps * 100 // (self.maxScore * 2)}")




    # Functions for moving character follows format (if can move: set current tile to visited, update tile, update cords, set tile to player, update tile)
    # Called by step

    # Function for moving up
    def move_character_up(self):
        if self.y-1 >= 0 and self.b[self.z][self.y-1][self.x] !=8:
            self.b[self.z][self.y][self.x] = 2
            self.canvas.itemconfig(self.rectangles[self.y][self.x], fill=COLOR_VISITED)
            self.y-=1
            self.b[self.z][self.y][self.x] = 5
            self.canvas.itemconfig(self.rectangles[self.y][self.x], fill=COLOR_PLAYER)

    # Function for moving down
    def move_character_down(self):
        if self.y+1 < maxY and self.b[self.z][self.y+1][self.x] !=8:
            self.b[self.z][self.y][self.x] = 2
            self.canvas.itemconfig(self.rectangles[self.y][self.x], fill=COLOR_VISITED)
            self.y+=1
            self.b[self.z][self.y][self.x] = 5
            self.canvas.itemconfig(self.rectangles[self.y][self.x], fill=COLOR_PLAYER)

    # Function for moving left
    def move_character_left(self):
        if self.x-1 >= 0 and self.b[self.z][self.y][self.x-1] !=8:
            self.b[self.z][self.y][self.x] = 2
            self.canvas.itemconfig(self.rectangles[self.y][self.x], fill=COLOR_VISITED)
            self.x-=1
            self.b[self.z][self.y][self.x] = 5
            self.canvas.itemconfig(self.rectangles[self.y][self.x], fill=COLOR_PLAYER)

    # Function for moving right
    def move_character_right(self):
        if self.x+1 < maxX and self.b[self.z][self.y][self.x+1] !=8:
            self.b[self.z][self.y][self.x] = 2
            self.canvas.itemconfig(self.rectangles[self.y][self.x], fill=COLOR_VISITED)
            self.x+=1
            self.b[self.z][self.y][self.x] = 5
            self.canvas.itemconfig(self.rectangles[self.y][self.x], fill=COLOR_PLAYER)
            
    # Function for moving up a floor
    def move_character_ascend(self):
        if self.z+1 < maxZ and self.b[self.z+1][self.y][self.x] !=8:
            self.b[self.z][self.y][self.x] = 2
            self.z+=1
            self.b[self.z][self.y][self.x] = 5
            self.draw_grid()
            
    # Function for moving down a floor
    def move_character_descend(self):
        if self.z-1 >= 0 and self.b[self.z-1][self.y][self.x] !=8:
            self.b[self.z][self.y][self.x] = 2
            self.z-=1
            self.b[self.z][self.y][self.x] = 5
            self.draw_grid()


    # Function for viewing floor above
    # Does nothing if no floor is above
    # Called by pressing the floor up button
    def floorUp(self):
        if self.z+1 < maxZ:
            self.z+=1
        self.draw_grid()

    # Function for viewing floor below
    # Does nothing if no floor is below
    # Called by pressing the floor down button
    def floorDown(self):
        if self.z-1 >= 0:
            self.z-=1
        self.draw_grid()


if __name__ == "__main__":
    app = GridDisplay()
    app.mainloop()
    