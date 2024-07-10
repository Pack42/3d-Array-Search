# TITLE: 3d board searcher Manual-Version
# AUTHOR: Pack
# CREATION DATE: 7/9/2024
# LAST UPDATE: 7/10/2024
# SUMMARY: Change any of the constants based on preference.
#           Allows the user to press buttons to move a character across a 3d environment represented as a stack of 2d grids

import tkinter as tk
from Board import *
# Constants
MAXX = 10
MAXY = 10
MAXZ = 10
NUM_WALLS = 500
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
        # Create board
        self.b = board(MAXX, MAXY, MAXZ, NUM_WALLS)[0]
        # Create starting point and spawn player
        n = [random.randint(0,MAXZ-1),random.randint(0,MAXY-1),random.randint(0,MAXX-1)]
        while self.b[n[0]][n[1]][n[2]] != 0:
            n = [random.randint(0,MAXZ-1),random.randint(0,MAXY-1),random.randint(0,MAXX-1)]
        self.b[n[0]][n[1]][n[2]] = 5
        # Set player location variables
        self.x,self.y,self.z = n[2],n[1],n[0]
        # Set grid for current floor
        grid = self.b[self.z]
        self.title("3d Explorer Manual")
        self.canvas = tk.Canvas(self, width=len(grid[0]) * CELL_SIZE, height=len(grid) * CELL_SIZE)
        self.canvas.pack() # Canvas
        self.floor_label = tk.Label(self, text="Floor: 0", font=("Helvetica", 14))
        self.floor_label.pack() # Floor label
        self.create_buttons()
        self.draw_grid()
        
        

    # Function that displays the grid
    # Called by init and all the move_character functions
    def draw_grid(self):
        # Set grid to the current floor
        grid = self.b[self.z]
        self.canvas.delete("all")  # Clear previous drawings
        for row in range(len(grid)):
            # Clear row
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
                # Create tile
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="black")
        # Update floor label
        self.floor_label.config(text=f"Floor: {self.z}")
        # Show text on buttons only if the move is possible
        if self.y-1 >= 0 and self.b[self.z][self.y-1][self.x] !=8:
            self.move_up_button.config(text = "Up")
        else:
            self.move_up_button.config(text = "")
        if self.y+1 < MAXY and self.b[self.z][self.y+1][self.x] !=8:
            self.move_down_button.config(text = "Down")
        else:
            self.move_down_button.config(text = "")
        if self.x+1 < MAXX and self.b[self.z][self.y][self.x+1] !=8:
            self.move_right_button.config(text = "Right")
        else:
            self.move_right_button.config(text = "")
        if self.x-1 >= 0 and self.b[self.z][self.y][self.x-1] !=8:
            self.move_left_button.config(text = "Left")
        else:
            self.move_left_button.config(text = "")
        if self.z+1 < MAXZ and self.b[self.z+1][self.y][self.x] !=8:
            self.move_ascend_button.config(text="Ascend")
        else:
            self.move_ascend_button.config(text="")
        if self.z-1 >= 0 and self.b[self.z-1][self.y][self.x] !=8:
            self.move_descend_button.config(text = "Descend")
        else:
            self.move_descend_button.config(text = "")

    def create_buttons(self):
        # Create buttons for character movement
        self.up_down_frame = tk.Frame(self)
        self.up_down_frame.pack(side="top", pady=(10, 0))  # Top line container

        self.move_blank_button = tk.Button(self.up_down_frame, text="", width=10, height=3)
        self.move_blank_button.pack(side="left", padx=(10, 5))  # Blank
        
        self.move_up_button = tk.Button(self.up_down_frame, text="Up", command=self.move_character_up, width=10, height=3)
        self.move_up_button.pack(side="left", padx=(10, 5))  # Up button in the top line

        self.move_ascend_button = tk.Button(self.up_down_frame, text="Ascend", command=self.move_character_ascend, width=10, height=3)
        self.move_ascend_button.pack(side="left", padx=(5, 10))  # Ascend button to the right of Up button in the top line

        self.left_right_frame = tk.Frame(self)
        self.left_right_frame.pack(side="top", pady=10)  # Middle line container
        
        self.move_left_button = tk.Button(self.left_right_frame, text="Left", command=self.move_character_left, width=10, height=3)
        self.move_left_button.pack(side="left", padx=(10, 5))  # Left button in the middle line

        self.move_blank2_button = tk.Button(self.left_right_frame, text="", width=10, height=3)
        self.move_blank2_button.pack(side="left", padx=(10, 5))  # Blank

        self.move_right_button = tk.Button(self.left_right_frame, text="Right", command=self.move_character_right, width=10, height=3)
        self.move_right_button.pack(side="left", padx=(5, 10))  # Right button in the middle line

        self.down_frame = tk.Frame(self)
        self.down_frame.pack(side="top", pady=(0, 10))  # Bottom line container
        
        self.move_descend_button = tk.Button(self.down_frame, text="Descend", command=self.move_character_descend, width=10, height=3)
        self.move_descend_button.pack(side="left", padx=(10, 5))  # Descend button to the left of Down button in the bottom line
        
        self.move_down_button = tk.Button(self.down_frame, text="Down", command=self.move_character_down, width=10, height=3)
        self.move_down_button.pack(side="left", padx=(5, 10))  # Down button in the bottom line

        self.move_blank3_button = tk.Button(self.down_frame, text="", width=10, height=3)
        self.move_blank3_button.pack(side="left", padx=(10, 5))  # Blank


    # Movement functions follows the format (If can move: set square to visited, update cords, set square to player, update display)

    def move_character_up(self):
        if self.y-1 >= 0 and self.b[self.z][self.y-1][self.x] !=8:
            self.b[self.z][self.y][self.x] = 2
            self.y-=1
            self.b[self.z][self.y][self.x] = 5
            self.draw_grid()

    def move_character_down(self):
        if self.y+1 < MAXY and self.b[self.z][self.y+1][self.x] !=8:
            self.b[self.z][self.y][self.x] = 2
            self.y+=1
            self.b[self.z][self.y][self.x] = 5
            self.draw_grid()

    def move_character_left(self):
        if self.x-1 >= 0 and self.b[self.z][self.y][self.x-1] !=8:
            self.b[self.z][self.y][self.x] = 2
            self.x-=1
            self.b[self.z][self.y][self.x] = 5
            self.draw_grid()

    def move_character_right(self):
        if self.x+1 < MAXX and self.b[self.z][self.y][self.x+1] !=8:
            self.b[self.z][self.y][self.x] = 2
            self.x+=1
            self.b[self.z][self.y][self.x] = 5
            self.draw_grid()

    def move_character_ascend(self):
        if self.z+1 < MAXZ and self.b[self.z+1][self.y][self.x] !=8:
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

if __name__ == "__main__":
    app = GridDisplay()
    app.mainloop()
    