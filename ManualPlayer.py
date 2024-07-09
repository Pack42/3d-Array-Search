import tkinter as tk
from Board import *
# Constants
CELL_SIZE = 60
COLOR_EMPTY = "white"
COLOR_WALL = "gray26"
COLOR_PLAYER = "gold2"
COLOR_VISITED = "light goldenrod"
class GridDisplay(tk.Tk):
    def __init__(self):
        super().__init__()
        self.b = board()[0]
        n = [random.randint(0,maxZ-1),random.randint(0,maxY-1),random.randint(0,maxX-1)]
        while self.b[n[0]][n[1]][n[2]] != 0:
            n = [random.randint(0,maxZ-1),random.randint(0,maxY-1),random.randint(0,maxX-1)]
        self.b[n[0]][n[1]][n[2]] = 5
        self.x,self.y,self.z = n[2],n[1],n[0]
        grid = self.b[self.z]
        self.title("Grid Display with Character Movement")
        self.canvas = tk.Canvas(self, width=len(grid[0]) * CELL_SIZE, height=len(grid) * CELL_SIZE)
        self.canvas.pack()
        self.floor_label = tk.Label(self, text="Floor: 0", font=("Helvetica", 14))
        self.floor_label.pack()
        self.create_buttons()
        self.draw_grid()
        
        

    def draw_grid(self):
        grid = self.b[self.z]
        self.canvas.delete("all")  # Clear previous drawings
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                x1, y1 = col * CELL_SIZE, row * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                if grid[row][col] == 8:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_WALL, outline="black")
                elif grid[row][col] == 0:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_EMPTY, outline="black")
                elif grid[row][col] == 5:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_PLAYER, outline="black")
                elif grid[row][col] == 2:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_VISITED, outline="black")
        self.floor_label.config(text=f"Floor: {self.z}")
        if self.y-1 >= 0 and self.b[self.z][self.y-1][self.x] !=8:
            self.move_up_button.config(text = "Up")
        else:
            self.move_up_button.config(text = "")
        if self.y+1 < maxY and self.b[self.z][self.y+1][self.x] !=8:
            self.move_down_button.config(text = "Down")
        else:
            self.move_down_button.config(text = "")
        if self.x+1 < maxX and self.b[self.z][self.y][self.x+1] !=8:
            self.move_right_button.config(text = "Right")
        else:
            self.move_right_button.config(text = "")
        if self.x-1 >= 0 and self.b[self.z][self.y][self.x-1] !=8:
            self.move_left_button.config(text = "Left")
        else:
            self.move_left_button.config(text = "")
        if self.z+1 < maxZ and self.b[self.z+1][self.y][self.x] !=8:
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


    def move_character_up(self):
        if self.y-1 >= 0 and self.b[self.z][self.y-1][self.x] !=8:
            self.b[self.z][self.y][self.x] = 2
            self.y-=1
            self.b[self.z][self.y][self.x] = 5
            self.draw_grid()

    def move_character_down(self):
        if self.y+1 < maxY and self.b[self.z][self.y+1][self.x] !=8:
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
        if self.x+1 < maxX and self.b[self.z][self.y][self.x+1] !=8:
            self.b[self.z][self.y][self.x] = 2
            self.x+=1
            self.b[self.z][self.y][self.x] = 5
            self.draw_grid()
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
if __name__ == "__main__":
    app = GridDisplay()
    app.mainloop()
    