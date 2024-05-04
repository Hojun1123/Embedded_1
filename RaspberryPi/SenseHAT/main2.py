from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from time import sleep
from signal import pause

sense = SenseHat()
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)

class Game():
    def __init__(self):
        self.size = 8
        self.board = [
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0, 1, 0],
        [0, 0, 1, 0, 0, 0, 1, 0],
        [0, 0, 1, 0, 1, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 0]
        ]
        self.player = [0, 0]
        self.goal = [self.size - 1, self.size - 1]

    def PrintInfo(self):
        print("size : ", self.size)
        for i in self.board:
            for j in i:
                print(j, end='')
            print()

    def PrintMap(self):
        #sense.set_pixel(self.player[1], self.player[0], green)
        for i in range(self.size):
            for j in range(self.size):
                sense.set_pixel(j, i, red if self.board[i][j] else white)
        sense.set_pixel(self.player[1], self.player[0], green)
        #sense.set_pixel(self.goal[1], self.goal[0], green)

    def dfs(self, p, y, x):
        if y == self.goal[0] and x == self.goal[1]:
            self.path.append(p.copy())
            return
        dy = [1, 0, -1, 0]
        dx = [0, 1, 0, -1]
        for k in range(4):
            yy = dy[k] + y
            xx = dx[k] + x
            if xx < 0 or yy < 0 or xx >= self.size or yy >= self.size or self.check[yy][xx] or self.board[yy][xx]: continue
            self.check[yy][xx] = 1
            p.append([yy, xx])
            self.dfs(p, yy, xx)
            p.pop()
            self.check[yy][xx] = 0


    def FindPath(self):
        self.check = [[0 for i in range(self.size)] for j in range(self.size)]
        self.path = []
        self.dfs([], self.player[0], self.player[1])
        self.btnCnt = 0
        print(len(self.path))

    def PrintPath(self):
        currPathNum = self.btnCnt % len(self.path)
        # map init
        self.PrintMap()
        for i in self.path[currPathNum]:
            sense.set_pixel(i[1], i[0], green)
            sleep(0.1)

    def PushButton(self, event):
        if event.action != ACTION_RELEASED:
            self.PrintPath()
            self.btnCnt += 1

    def Run(self):
        # sense.set_pixel(self.player[1], self.player[0], white)
        # sense.set_pixel(self.player[1], self.player[0], green)
        sense.stick.direction_any = self.PushButton
        #sense.clear()
        pause()

    def __del__(self):
        sense.clear()


def main():
    print("main!")
    game = Game()
    game.PrintInfo()
    game.PrintMap()
    game.FindPath()
    game.Run()
    #sense.clear()

if __name__ == "__main__":
    main()
