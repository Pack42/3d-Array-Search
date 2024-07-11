# TITLE: 3d board searcher visualization with audio
# AUTHOR: Pack
# CREATION DATE: 7/11/2024
# LAST UPDATE: 7/11/2024
# SUMMARY: Run file and press start to start the visualization.  Change any of the constants based on preference.
#           This version adds audio to the explorer


import SimplePlayer as sp
from nava import play
MAXX = 7
MAXY = 4
MAXZ = 10
NUM_WALLS = 250
ALPH = ["A", "B", "C", "D", "E", "F", "G"]
DELAY = .25
class AudioExplorer(sp.GridDisplay):
    def __init__(self):
        super().__init__()
    # Function to set maxScore, and create grid and starting point
    # Calls board function to create board
    # Called by init and reset
    def create_grid(self):
        # Create board
        self.b = sp.board(MAXX, MAXY, MAXZ,NUM_WALLS)
        # Set maxScore
        self.maxScore = self.b[1]
        # Clean variable b to not include max score
        self.b = self.b[0]
        # Chose starting point
        n = [sp.random.randint(0,MAXX-1),sp.random.randint(0,MAXY-1),sp.random.randint(0,MAXZ-1)]
        while self.b[n[2]][n[1]][n[0]] != 0:
            n = [sp.random.randint(0,MAXX-1),sp.random.randint(0,MAXY-1),sp.random.randint(0,MAXZ-1)]
        # Update board to have character at the starting point
        self.b[n[2]][n[1]][n[0]] = 5
        # Set agent location
        self.x,self.y,self.z = n[0],n[1],n[2]

    # Function for starting the algorithm to auto run
    # Called by threading
    # Calls step function until complete
    def start(self):
        # Hide start and stop button
        self.start_frame.pack_forget()
        # Run step until done then kills the thread
        while True:
            # Plays note
            play("Music/" + ALPH[self.x % 7] + str((self.y % 4)+2) + ".wav", async_mode=True)
            self.step()
            if self.done:
                break
    
    # Function for running one step of the algorithm
    # Called by start or by pressing the step button
    # Calls movement functions
    def step(self):
        sp.time.sleep(DELAY)
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
        elif self.y+1 < MAXY and self.b[self.z][self.y+1][self.x] ==0:
            self.score+=1
            self.steps +=1
            self.path.append("up")
            self.move_character_down()
        # If right is in bounds and is a empty square: 
        # Update score/steps, and move right and push left to path stack
        elif self.x+1 < MAXX and self.b[self.z][self.y][self.x+1] ==0:
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
        elif self.z+1 < MAXZ and self.b[self.z+1][self.y][self.x] ==0:
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


if __name__ == "__main__":
    app = AudioExplorer()
    app.mainloop()
    