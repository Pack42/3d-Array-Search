# TITLE: 3d board searcher visualization
# AUTHOR: Pack
# DATE: 7/9/2024
# LAST UPDATE: 7/9/2024
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

# Class for display
class GridDisplay(tk.Tk):
    def __init__(self):
        super().__init__()
        # Variable setup
        self.score = 0
        self.steps = 0
        self.progress = 0
        self.path = []
        self.b = board()
        self.maxScore = self.b[1]
        self.b = self.b[0]
        # Choses starting point
        n = [random.randint(0,maxZ-1),random.randint(0,maxY-1),random.randint(0,maxX-1)]
        while self.b[n[0]][n[1]][n[2]] != 0:
            n = [random.randint(0,maxZ-1),random.randint(0,maxY-1),random.randint(0,maxX-1)]
        self.b[n[0]][n[1]][n[2]] = 5
        self.x,self.y,self.z = n[2],n[1],n[0]
        self.create_layout()
        # Create list to allow squares to be updated without fully reloading each time
        self.rectangles = {}
        self.draw_grid()
        self.create_buttons()
        
    # Multi-Threading barely one thread runs display other handles algorithm
    def threading(self):
            t1=Thread(target=self.start) 
            t1.start()

    def create_layout(self):
        # Create layout for display
        # Set display to 2d array based on what floor agent is on
        grid = self.b[self.z]
        self.title("Simple Agent")
        self.canvas = tk.Canvas(self, width=len(grid[0]) * CELL_SIZE, height=len(grid) * CELL_SIZE)
        self.canvas.pack()
        self.floor_label = tk.Label(self, text="Floor: 0", font=("Helvetica", 14))
        self.floor_label.pack()
        self.score_frame = tk.Frame(self)
        self.score_frame.pack(side="top", pady=(10, 0)) 
        self.steps_label = tk.Label(self.score_frame, text="Steps: 0", font=("Helvetica", 14))
        self.steps_label.pack(side="left", padx=(10, 5))
        self.score_label = tk.Label(self.score_frame, text="Score: 0", font=("Helvetica", 14))
        self.score_label.pack(side="left", padx=(10, 5))
        self.progress_label = tk.Label(self.score_frame, text="Progress: 0", font=("Helvetica", 14))
        self.progress_label.pack(side="left", padx=(10, 5))
        self.score2_frame = tk.Frame(self)
        self.score2_frame.pack()
        max_label = tk.Label(self.score2_frame, text=f"Max Score: {self.maxScore}", font=("Helvetica", 14))
        max_label.pack(side="left", padx=(10, 5))
        self.act_progress_label = tk.Label(self.score2_frame, text="Actual Progress: 0", font=("Helvetica", 14))
        self.act_progress_label.pack(side="left", padx=(10, 5))

    # Creates buttons
    def create_buttons(self):
        self.start_frame = tk.Frame(self)
        self.start_frame.pack(side="top", pady=(10, 0))  # Top line container
        self.start_button = tk.Button(self.start_frame, text="Start", command=self.threading, width=10, height=3)
        self.start_button.pack(side="left", padx=(10, 5))  # Start button

    def draw_grid(self):
        grid = self.b[self.z]
        self.canvas.delete("all")  # Clear previous drawings
        for row in range(len(grid)):
            self.rectangles[row] = {}
            for col in range(len(grid[0])):
                x1, y1 = col * CELL_SIZE, row * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
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
                self.rectangles[row][col] = self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="black")
        self.floor_label.config(text=f"Floor: {self.z}")


    def move_character_up(self):
        if self.y-1 >= 0 and self.b[self.z][self.y-1][self.x] !=8:
            self.b[self.z][self.y][self.x] = 2
            self.canvas.itemconfig(self.rectangles[self.y][self.x], fill=COLOR_VISITED)
            self.y-=1
            self.b[self.z][self.y][self.x] = 5
            self.canvas.itemconfig(self.rectangles[self.y][self.x], fill=COLOR_PLAYER)

    def move_character_down(self):
        if self.y+1 < maxY and self.b[self.z][self.y+1][self.x] !=8:
            self.b[self.z][self.y][self.x] = 2
            self.canvas.itemconfig(self.rectangles[self.y][self.x], fill=COLOR_VISITED)
            self.y+=1
            self.b[self.z][self.y][self.x] = 5
            self.canvas.itemconfig(self.rectangles[self.y][self.x], fill=COLOR_PLAYER)

    def move_character_left(self):
        if self.x-1 >= 0 and self.b[self.z][self.y][self.x-1] !=8:
            self.b[self.z][self.y][self.x] = 2
            self.canvas.itemconfig(self.rectangles[self.y][self.x], fill=COLOR_VISITED)
            self.x-=1
            self.b[self.z][self.y][self.x] = 5
            self.canvas.itemconfig(self.rectangles[self.y][self.x], fill=COLOR_PLAYER)

    def move_character_right(self):
        if self.x+1 < maxX and self.b[self.z][self.y][self.x+1] !=8:
            self.b[self.z][self.y][self.x] = 2
            self.canvas.itemconfig(self.rectangles[self.y][self.x], fill=COLOR_VISITED)
            self.x+=1
            self.b[self.z][self.y][self.x] = 5
            self.canvas.itemconfig(self.rectangles[self.y][self.x], fill=COLOR_PLAYER)
    def move_character_ascend(self):
        if self.z+1 < maxZ and self.b[self.z+1][self.y][self.x] !=8:
            self.b[self.z][self.y][self.x] = 2
            self.z+=1
            self.b[self.z][self.y][self.x] = 5
            self.draw_grid()
    def move_character_descend(self):
        if self.z-1 >= 0 and self.b[self.z-1][self.y][self.x] !=8:
            self.b[self.z][self.y][self.x] = 2
            self.z-=1
            self.b[self.z][self.y][self.x] = 5
            self.draw_grid()

    def start(self):
        while True:
            time.sleep(.05)
            print("trying")
            if self.y-1 >= 0 and self.b[self.z][self.y-1][self.x] ==0:
                self.score+=1
                self.path.append("down")
                self.move_character_up()
            elif self.y+1 < maxY and self.b[self.z][self.y+1][self.x] ==0:
                self.score+=1
                self.path.append("up")
                self.move_character_down()
            elif self.x+1 < maxX and self.b[self.z][self.y][self.x+1] ==0:
                self.score+=1
                self.path.append("left")
                self.move_character_right()
            elif self.x-1 >= 0 and self.b[self.z][self.y][self.x-1] ==0:
                self.score+=1
                self.path.append("right")
                self.move_character_left()
            elif self.z+1 < maxZ and self.b[self.z+1][self.y][self.x] ==0:
                self.score+=1
                self.path.append("descend")
                self.move_character_ascend()
            elif self.z-1 >= 0 and self.b[self.z-1][self.y][self.x] ==0:
                self.score+=1
                self.path.append("ascend")
                self.move_character_descend()
            elif len(self.path) > 0:
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
            else:
                break
            self.score_label.config(text=f"Score: {self.score}")
            self.steps +=1
            self.steps_label.config(text=f"Steps: {self.steps}")
            self.progress = ((self.steps-self.score)* 100 //self.score )
            self.progress_label.config(text=f"Progress: {self.progress}")
            temp = self.steps * 100 // (self.maxScore * 2)
            self.act_progress_label.config(text=f"Actual Progress: {temp}")
    def step(self):
        print("trying")
        if self.y-1 >= 0 and self.b[self.z][self.y-1][self.x] ==0:
            self.path.append("down")
            self.move_character_up()
        elif self.y+1 < maxY and self.b[self.z][self.y+1][self.x] ==0:
            self.path.append("up")
            self.move_character_down()
        elif self.x+1 < maxX and self.b[self.z][self.y][self.x+1] ==0:
            self.path.append("left")
            self.move_character_right()
        elif self.x-1 >= 0 and self.b[self.z][self.y][self.x-1] ==0:
            self.path.append("right")
            self.move_character_left()
        elif self.z+1 < maxZ and self.b[self.z+1][self.y][self.x] ==0:
            self.path.append("descend")
            self.move_character_ascend()
        elif self.z-1 >= 0 and self.b[self.z-1][self.y][self.x] ==0:
            self.path.append("ascend")
            self.move_character_descend()
        elif len(self.path) > 0:
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
        else:
            exit()
if __name__ == "__main__":
    app = GridDisplay()
    app.mainloop()
    