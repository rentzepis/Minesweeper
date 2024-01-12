import tkinter as tk
from tkinter import font
from tkinter import messagebox
from collections import deque
import random
import sys
import os

ROWS = 16
COLS = 16
MINES = 45

class Minesweeper:
    num_flags = int(MINES)

    def __init__(self, root, ):

        # window + labels
        self.root = root
        self.root.attributes("-topmost", True)
        self.root.title("Minesweeper")
        self.root.geometry()

        self.info = tk.Frame(self.root, borderwidth=20)
        self.info.pack()

        self.text = font.Font(family='Arial', size=18, weight="bold")

        self.flags = tk.Label(self.info, font=self.text, text = "Flags Left: 0")
        self.flags.grid(row=0, column=int(COLS/2), pady= 15, columnspan = int(COLS/2))
        self.update_flags()

        self.instructions = tk.Button(self.info, font=self.text, text="Instructions", bg="lightgray", command=self.show_instructions)
        self.instructions.grid(row=0,column=0,pady= 15, columnspan = int(COLS/2))


        self.colors = {
            1: "blue",
            2: "green",
            3: "red",
            4: "darkblue",
            5: "darkred",
            6: "cyan",
            7: "black",
            8: "darkgray"
        }

        # flag and cell trackers
        self.num_flags = int(MINES)
        self.opened = 0
        
        # first loop creating cells and their info
        self.cells = dict({})
        for x in range(0,ROWS):
            for y in range(0,COLS):
                if y == 0:
                    self.cells[x] = {}

                # dictionary storing cell information
                cell = {
                    "num": x*y+y,
                    "x": x,
                    "y": y,
                    "adj_mines": 0,
                    "is_flagged": False,
                    "is_mine": False,
                    "open": False,
                    "button": tk.Button(self.info, font=self.text, bg="gray", text=" ",width=3,height=1)}

                cell["button"].bind("<Button-1>", self.leftclick(x, y))
                cell["button"].bind("<Button-3>", self.rightclick(x, y))
                cell["button"].grid(row=x+1, column=y)

                self.cells[x][y] = cell
        
        # loop randomizing mines
        for i in range(0,MINES):
            x = random.randint(0,ROWS-1)
            y = random.randint(0,COLS-1)
            if not self.cells[x][y]["is_mine"]: # if cell does not have a mine
                self.cells[x][y]["is_mine"] = True
            else:
                i -= 1
        
        # loop to count adjacent mines
        for x in range(0,ROWS):
            for y in range(0, COLS):
                minecount = 0
                for i in self.get_neighbors(x,y):                    
                    minecount += 1 if i["is_mine"] else 0
                    self.cells[x][y]["adj_mines"] = minecount

    def leftclick(self,x,y):
        return lambda Button: self.open(self.cells[x][y])
    
    def rightclick(self,x,y):
        return lambda Button: self.flag(self.cells[x][y])
    
    def show_instructions(self):
        text = ("The board is divided into cells, with randomly distributed mines. To win, you need to open all the cells. " +
            "The number on a cell shows the number of mines adjacent to it. Using this information, you can determine cells that are safe, and cells that contain mines.\n\n" +
            "To open a cell, left-click, and to flag/unflag a cell suspected of being a mines, right-click. You cannot accidentally open a cell while it is flagged.")
        messagebox.showinfo("Instructions",text)
        pass
    
    def open(self,cell):
        #mine opened
        if cell["is_mine"]:
            cell["button"].config(text="☼",bg="red")
            self.end("lost") # lose screen
            return
        
        # cell is flagged
        if cell["is_flagged"]:
            return
        
        #no adjacent mines
        elif cell["adj_mines"] == 0:
            cell["button"].config(bg="lightgray", text=(" "),state="disabled") 
            if cell["open"] == False:
               self.opened += 1
               if self.opened == ROWS * COLS - MINES:
                   self.end("win")
            cell["open"] = True
            self.clear_neighbors(cell)
        #has adjacent mines
        else: 
           cell["button"].config(text=(str)(cell["adj_mines"]), bg="lightgray",state="disabled",disabledforeground=self.colors[cell["adj_mines"]]) 
           if cell["open"] == False:
               self.opened += 1
               if self.opened == ROWS * COLS - MINES:
                   self.end("win")
           cell["open"] = True

    def flag(self,cell):
        if cell["open"] == False:
            if not cell["is_flagged"]:
                cell["button"].config(text="⚑")
                self.num_flags -= 1
                cell["button"].unbind("<Button-1>")
            else:
                cell["button"].config(text=" ")
                self.num_flags += 1
                cell["button"].bind("<Button-1>", self.leftclick(cell["x"], cell["y"]))
            self.update_flags()

            cell["is_flagged"] = not cell["is_flagged"]
        pass

    def get_neighbors(self, x, y):
        neighbors = []
        adjacent = [
            {"x": x-1, "y": y-1}, 
            {"x": x-1, "y": y},    
            {"x": x-1, "y": y+1},  
            {"x": x, "y": y-1},  
            {"x": x, "y": y+1},  
            {"x": x+1, "y": y-1},  
            {"x": x+1, "y": y},   
            {"x": x+1, "y": y+1}, 
        ]
        for i in adjacent:
            try:
                neighbors.append(self.cells[i["x"]][i["y"]])
            except KeyError:
                pass
        return neighbors
    
    def clear_neighbors(self, clickedcell):
        clear = deque([clickedcell])

        while len(clear) != 0:
            cell = clear.popleft()
            x = cell["x"]
            y = cell["y"]
            for neighbor in self.get_neighbors(x,y):
                if not neighbor["open"]:
                    if neighbor["adj_mines"] == 0:
                        clear.append(neighbor)
                    self.open(neighbor)

    def update_flags(self):
        self.flags.config(text = f"Flags Left: {self.num_flags}")
    
    def end(self, win_state):
        s = f"You {win_state}! \nPlay again?"
        if messagebox.askyesno("Game Over", s):
            python = sys.executable
            os.execl(python, python, *sys.argv)
        else:
            self.root.quit()
            
def main():
    root = tk.Tk()    
    Minesweeper(root)
    root.mainloop()

main()