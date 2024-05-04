from sense_hat import SenseHat
from time import sleep

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
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
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

    def FindPath(self):
        #part2
        pass

    def GetGyroSense(self):
        # Sense HAT에서 가속도 및 방향 데이터 가져오기
        acceleration = sense.get_accelerometer_raw()
        # X, Y, Z 축 가속도 값 가져오기
        acc_x = acceleration['x']
        acc_y = acceleration['y']
        acc_z = acceleration['z']
        # X, Y 축의 기울기 계산 (라디안 값)
        roll_rad = -1 * (acc_x / ((acc_y ** 2 + acc_z ** 2) ** 0.5))
        pitch_rad = -1 * (acc_y / ((acc_x ** 2 + acc_z ** 2) ** 0.5))
        # 라디안 값을 각도로 변환 (degrees)
        roll = roll_rad * 180 / 3.14
        pitch = pitch_rad * 180 / 3.14
        # 결과 출력
        #print("Roll: {:.2f} degrees".format(roll))
        #print("Pitch: {:.2f} degrees".format(pitch))
        return [roll, pitch]

        #### prev.
        gyro = sense.get_gyroscope()
        x = gyro['pitch']
        y = gyro['roll']
        z = gyro['yaw']
        #print(f"Gyro - X:{x}, Y:{y}, Z:{z}")
        return [x, y, z]

    def Left(self):
        y, x = self.player
        nx = x - 1
        if nx < 0 or self.board[y][nx]: return [y, x]
        else: return [y, nx]

    def Right(self):
        y, x = self.player
        nx = x + 1
        if nx >= self.size or self.board[y][nx]: return [y, x]
        else: return [y, nx]

    def Top(self):
        y, x = self.player
        ny = y - 1
        if ny < 0 or self.board[ny][x]: return [y, x]
        else: return [ny, x]

    def Down(self):
        y, x = self.player
        ny = y + 1
        if ny >= self.size or self.board[ny][x]: return [y, x]
        else: return [ny, x]

    def Run(self):
        sense.set_pixel(self.player[1], self.player[0], white)
        x, y = self.GetGyroSense()
        print(f"Gyro - roll:{x}, pitch:{y}")
        # print(f"Player - X:{self.player[1]}, Y:{self.player[0]}")
        if x > 20 and x < 180:
            print("Left")
            self.player = self.Left()
        elif x < -20 and x > -180:
            print("Right")
            self.player = self.Right()
        elif y < -20 and y > -180:
            print("Down")
            self.player = self.Down()
        elif y < 180 and y > 20:
            print("Top")
            self.player = self.Top()
        sense.set_pixel(self.player[1], self.player[0], green)
        sleep(1)

    def __del__(self):
        sense.clear()


def main():
    print("main!")
    game = Game()
    game.PrintInfo()
    game.PrintMap()
    while True:
        game.Run()

if __name__ == "__main__":
    main()
