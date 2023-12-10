# 지뢰찾기 게임

from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox as tkMessageBox
from collections import deque
import random
import platform
import time
from datetime import time, date, datetime

STATE_DEFAULT = 0
STATE_CLICKED = 1
STATE_FLAGGED = 2

BTN_CLICK = "<Button-1>"
BTN_FLAG = "<Button-2>" if platform.system() == 'Darwin' else "<Button-3>"

window = None

class Minesweeper:

    def __init__(self, tk, size_x, size_y, mode, difficulty):

        # 이미지 불러오기
        self.images = {
            "plain": PhotoImage(file = "images/tile_plain.gif", master = window),
            "clicked": PhotoImage(file = "images/tile_clicked.gif", master = window),
            "mine": PhotoImage(file = "images/tile_mine.gif", master = window),
            "flag": PhotoImage(file = "images/tile_flag.gif", master = window),
            "wrong": PhotoImage(file = "images/tile_wrong.gif", master = window),
            "numbers": []
        }
        for i in range(1, 9):
            self.images["numbers"].append(PhotoImage(file = "images/tile_"+str(i)+".gif", master = window))

        # 프레임 생성
        self.tk = tk
        self.frame = Frame(self.tk)
        self.frame.pack()

        # 레이블/UI 생성
        self.labels = {
            "time": Label(self.frame, text = "00:00:00"),
            "mines": Label(self.frame, text = "지뢰 수: 0"),
            "flags": Label(self.frame, text = "깃발 수: 0")
        }
        
        self.size_x = size_x
        self.size_y = size_y
        self.mode = mode
        self.difficulty = difficulty

        self.restart() 
        self.updateTimer() 


    def setup(self):
        
        self.flagCount = 0
        self.correctFlagCount = 0
        self.clickedCount = 0
        self.startTime = None
        
        if self.difficulty == 0:
            minesamount = 0.1
        elif self.difficulty == 1:
            minesamount = 0.2
        else:
            minesamount = 0.3

        # 버튼 만들기
        self.tiles = dict({})
        self.mines = 0
        for x in range(0, self.size_x):
            for y in range(0, self.size_y):
                if y == 0:
                    self.tiles[x] = {}

                id = str(x) + "_" + str(y)
                isMine = False

                gfx = self.images["plain"]

                if random.uniform(0.0, 1.0) < minesamount:
                    isMine = True
                    self.mines += 1

                tile = {
                    "id": id,
                    "isMine": isMine,
                    "state": STATE_DEFAULT,
                    "coords": {
                        "x": x,
                        "y": y
                    },
                    "button": Button(self.frame, image = gfx),
                    "mines": 0 
                }

                tile["button"].bind(BTN_CLICK, self.onClickWrapper(x, y))
                tile["button"].bind(BTN_FLAG, self.onRightClickWrapper(x, y))
                tile["button"].grid( row = x+1, column = y ) 

                self.tiles[x][y] = tile

        # 인접한 지뢰 개수 찾고 표시하기
        for x in range(0, self.size_x):
            for y in range(0, self.size_y):
                mc = 0
                for n in self.getNeighbors(x, y):
                    mc += 1 if n["isMine"] else 0
                self.tiles[x][y]["mines"] = mc      
                    
    
    def restart(self):
        self.boardSize()
        self.gameMode()
        self.getDifficulty()
        self.setup()
        self.refreshLabels()
        self.startTime = None
        
        
    def gameMode(self):
        self.mode = simpledialog.askinteger("지뢰찾기", "모드(0 : 일반, 1 : 십자, 2 : 체스):", initialvalue=0)
        
    def getDifficulty(self):
        self.difficulty = simpledialog.askinteger("지뢰찾기", "난이도(0 : 쉬움, 1 : 보통, 2 : 어려움):", initialvalue=0)

    def boardSize(self):
        self.size_x = simpledialog.askinteger("지뢰찾기", "열의 수:", initialvalue=10)
        self.size_y = simpledialog.askinteger("지뢰찾기", "행의 수:", initialvalue=10)
        self.labels["time"].grid(row = 0, column = 0, columnspan = self.size_y)
        self.labels["mines"].grid(row=self.size_x + 1, column=0, columnspan=int(self.size_y / 2))
        self.labels["flags"].grid(row=self.size_x + 1, column=int(self.size_y / 2) - 1, columnspan=int(self.size_y / 2))

    def refreshLabels(self):
        self.labels["flags"].config(text = "깃발 수: "+str(self.flagCount))
        self.labels["mines"].config(text = "지뢰 수: "+str(self.mines))

    def gameOver(self, won):
        for x in range(0, self.size_x):
            for y in range(0, self.size_y):
                if self.tiles[x][y]["isMine"] == False and self.tiles[x][y]["state"] == STATE_FLAGGED:
                    self.tiles[x][y]["button"].config(image = self.images["wrong"])
                if self.tiles[x][y]["isMine"] == True and self.tiles[x][y]["state"] != STATE_FLAGGED:
                    self.tiles[x][y]["button"].config(image = self.images["mine"])

        self.tk.update()

        msg = "게임 클리어! 다시 하시겠습니까?" if won else "실패! 다시 하시겠습니까?"
        res = tkMessageBox.askyesno("Game Over", msg)
        if res:
            self.restart()
        else:
            self.tk.quit()

    def updateTimer(self):
        ts = "00:00:00"
        if self.startTime != None:
            delta = datetime.now() - self.startTime
            ts = str(delta).split('.')[0] 
            if delta.total_seconds() < 36000:
                ts = "0" + ts 
        self.labels["time"].config(text = ts)        
        self.frame.after(100, self.updateTimer)

    def getNeighbors(self, x, y):
        if self.mode == 0 or 3:
            neighbors = []
            coords = [
                {"x": x-1,  "y": y-1},  
                {"x": x-1,  "y": y},    
                {"x": x-1,  "y": y+1},  
                {"x": x,    "y": y-1},  
                {"x": x,    "y": y+1},  
                {"x": x+1,  "y": y-1},  
                {"x": x+1,  "y": y},    
                {"x": x+1,  "y": y+1},  
                ]
            for n in coords:
                try:
                    neighbors.append(self.tiles[n["x"]][n["y"]])
                except KeyError:
                    pass
            return neighbors
        if self.mode == 1:
            neighbors = []
            coords = [
                {"x": x-1,  "y": y},    
                {"x": x,    "y": y-1},  
                {"x": x,    "y": y+1},  
                {"x": x+1,  "y": y},    
                {"x": x-2,  "y": y},    
                {"x": x,    "y": y-2},  
                {"x": x,    "y": y+2},  
                {"x": x+2,  "y": y},    
                ]
            for n in coords:
                try:
                    neighbors.append(self.tiles[n["x"]][n["y"]])
                except KeyError:
                    pass
            return neighbors
        if self.mode == 2:
            neighbors = []
            coords = [
                {"x": x-2,  "y": y-1},    
                {"x": x-2,  "y": y+1},  
                {"x": x+2,  "y": y-1},  
                {"x": x+2,  "y": y+1},    
                {"x": x-1,  "y": y-2},    
                {"x": x+1,  "y": y-2},  
                {"x": x-1,  "y": y+2},  
                {"x": x+1,  "y": y+2},   
                ]
            for n in coords:
                try:
                    neighbors.append(self.tiles[n["x"]][n["y"]])
                except KeyError:
                    pass
            return neighbors
            

    def onClickWrapper(self, x, y):
        return lambda Button: self.onClick(self.tiles[x][y])

    def onRightClickWrapper(self, x, y):
        return lambda Button: self.onRightClick(self.tiles[x][y])

    def onClick(self, tile):
        if self.startTime == None:
            self.startTime = datetime.now()

        if tile["isMine"] == True:
            self.gameOver(False)
            return

        # 이미지 변경
        if tile["mines"] == 0:
            tile["button"].config(image = self.images["clicked"])
            self.clearSurroundingTiles(tile["id"])
        else:
                tile["button"].config(image = self.images["numbers"][tile["mines"]-1])
            
        if tile["state"] != STATE_CLICKED:
            tile["state"] = STATE_CLICKED
            self.clickedCount += 1
        if self.clickedCount == (self.size_x * self.size_y) - self.mines:
            self.gameOver(True)

    def onRightClick(self, tile):
        if self.startTime == None:
            self.startTime = datetime.now()

        # 클릭되지 않았다면
        if tile["state"] == STATE_DEFAULT:
            tile["button"].config(image = self.images["flag"])
            tile["state"] = STATE_FLAGGED
            tile["button"].unbind(BTN_CLICK)
            # 지뢰라면
            if tile["isMine"] == True:
                self.correctFlagCount += 1
            self.flagCount += 1
            self.refreshLabels()
        # 지뢰였다면, 지뢰 표시를 없앰
        elif tile["state"] == 2:
            tile["button"].config(image = self.images["plain"])
            tile["state"] = 0
            tile["button"].bind(BTN_CLICK, self.onClickWrapper(tile["coords"]["x"], tile["coords"]["y"]))
            # 지뢰라면
            if tile["isMine"] == True:
                self.correctFlagCount -= 1
            self.flagCount -= 1
            self.refreshLabels()

    def clearSurroundingTiles(self, id):
        queue = deque([id])

        while len(queue) != 0:
            key = queue.popleft()
            parts = key.split("_")
            x = int(parts[0])
            y = int(parts[1])

            for tile in self.getNeighbors(x, y):
                self.clearTile(tile, queue)

    def clearTile(self, tile, queue):
        if tile["state"] != STATE_DEFAULT:
            return

        if tile["mines"] == 0:
            tile["button"].config(image = self.images["clicked"])
            queue.append(tile["id"])
        else:
            tile["button"].config(image = self.images["numbers"][tile["mines"]-1])

        tile["state"] = STATE_CLICKED
        self.clickedCount += 1

### 클래스 끝 ###

def main():
    
    window = Toplevel()

    window.title("지뢰찾기")

    minesweeper = Minesweeper(window,10,10,0,0)

    window.mainloop()

if __name__ == "__main__":
    main()
