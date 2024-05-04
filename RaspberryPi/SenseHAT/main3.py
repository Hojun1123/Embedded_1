from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from time import sleep
from signal import pause
from collections import deque

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


    def FindPath(self):
        dy = [1, -1, 0, 0]
        dx = [0, 0, 1, -1]
        check = [[0 for i in range(self.size)] for j in range(self.size)]
        path = [[[] for i in range(self.size)] for j in range(self.size)]
        y, x = self.player
        queue = deque([[y, x]])
        check[y][x] = 1
        flag = False
        while len(queue):
            qSize = len(queue)
            for i in range(qSize):
                now = queue.popleft()
                if now[0] == self.goal[0] and now[1] == self.goal[1]:
                    print("end!")
                    flag = True
                    break
                for k in range(4):
                    y = dy[k] + now[0]
                    x = dx[k] + now[1]
                    if y < 0 or x < 0 or y >= self.size or x >= self.size or check[y][x] or self.board[y][x]: continue
                    path[y][x] = now
                    queue.append([y, x])
                    check[y][x] = 1
            if flag:
                break

        #print path
        start = self.goal
        while path[start[0]][start[1]]:
            sense.set_pixel(start[1], start[0], blue)
            sleep(0.1)
            start = path[start[0]][start[1]]

        sleep(1)
        start = self.goal
        while path[start[0]][start[1]]:
            sense.set_pixel(start[1], start[0], white)
            start = path[start[0]][start[1]]

    def pushed_up(self, event):
        if event.action != ACTION_RELEASED:
            y, x = self.player
            #sense.set_pixel(x, y, white)
            if y - 1 < 0 or self.board[y - 1][x]: return
            self.player = [y - 1, x]
            y, x = self.player
            print("y:%d, x:%d" %(y, x))
            sense.clear()
            self.PrintMap()
            self.FindPath()
            sense.set_pixel(x, y, green)


    def pushed_down(self, event):
        if event.action != ACTION_RELEASED:
            y, x = self.player
            #sense.set_pixel(x, y, white)
            if y + 1 >= self.size or self.board[y + 1][x]: return
            self.player = [y + 1, x]
            y, x = self.player
            print("y:%d, x:%d" %(y, x))
            sense.clear()
            self.PrintMap()
            self.FindPath()
            sense.set_pixel(x, y, green)


    def pushed_left(self, event):
        if event.action != ACTION_RELEASED:
            y, x = self.player
            #sense.set_pixel(x, y, white)
            if x - 1 < 0 or self.board[y][x - 1]: return
            self.player = [y, x - 1]
            y, x = self.player
            print("y:%d, x:%d" %(y, x))
            sense.clear()
            self.PrintMap()
            self.FindPath()
            sense.set_pixel(x, y, green)


    def pushed_right(self, event):
        if event.action != ACTION_RELEASED:
            y, x = self.player
            #sense.set_pixel(x, y, white)
            if x + 1 >= self.size or self.board[y][x + 1]: return
            self.player = [y, x + 1]
            y, x = self.player
            print("y:%d, x:%d" %(y, x))
            sense.clear()
            self.PrintMap()
            self.FindPath()
            sense.set_pixel(x, y, green)


    def refresh(self):
        sleep(0.2)
        y, x = self.player
        print("y:%d, x:%d" %(y, x))
        sense.clear()
        self.PrintMap()
        self.FindPath()
        sense.set_pixel(x, y, green)

    def Run(self):
        sense.stick.direction_up = self.pushed_up
        sense.stick.direction_down = self.pushed_down
        sense.stick.direction_left = self.pushed_left
        sense.stick.direction_right = self.pushed_right
        #sense.stick.direction_any = self.refresh
        pause()

    def __del__(self):
        sense.clear()


def main():
    print("main!")
    game = Game()
    game.PrintInfo()
    game.PrintMap()
    game.Run()

if __name__ == "__main__":
    main()
