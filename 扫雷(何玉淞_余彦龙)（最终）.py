import random
import os


class SL:
    def __init__(self, width, height, mines):
        self.width = width
        self.height = height
        self.mines = mines
        self.back = []
        self.visible = []
        self.w_cell_lit = []
        self.finish_reveal = []
        self.game_over = False
        self.win = False
        self.first_click = True
        self.initialize_game()

    def initialize_game(self):
        self.back = [[' ' for _ in range(self.height)] for _ in range(self.width)]
        self.visible = [[' ' for _ in range(self.height)] for _ in range(self.width)]
        self.w_cell_lit = [['1' for _ in range(self.height)] for _ in range(self.width)]
        self.finish_reveal = [[' ' for _ in range(self.height)] for _ in range(self.width)]
        self.game_over = False
        self.win = False
        self.first_click = True

    def place_mines(self, safe_x, safe_y):
        positions = []
        self.back[safe_x][safe_y] = ' '
        for x in range(self.width):
            for y in range(self.height):
                positions.append((x, y))
        positions.remove((safe_x, safe_y))
        mine_positions = random.sample(positions, self.mines)
        for x, y in mine_positions:
            self.back[x][y] = 'X'
        self.count_numbers()

    def display_board(self):
        print("扫雷游戏")
        print(f"地雷数量: {self.mines}")
        print("操作说明: ")
        print("  r x y - 揭示格子 (例如: r 3 4)")
        print("  f x y - 标记/取消标记地雷 (例如: f 3 4)")
        print("  q - 退出游戏")
        print("   " + " ".join(str(i + 1) for i in range(self.width)))
        print("  !" + "-" * (self.width * 2) + "!")
        for y in range(self.height):
            line = f"{y + 1} |"
            for x in range(self.width):
                cell = self.visible[x][y]
                if cell == 'X':
                    line += "X "
                elif cell == 'F':
                    line += "# "
                elif cell == ' ':
                    line += "■ "
                elif cell == 'w':
                    line += "[]"
                else:
                    line += f"{cell} "
            print(line + "|")
        print("  !" + "-" * (self.width * 2) + "!")

    def reveal_all(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.visible[x][y] == ' ':
                    self.visible[x][y] = self.back[x][y]
                    if self.back[x][y] == ' ':
                        self.visible[x][y] = 'w'
                elif self.visible[x][y] == 'F':
                    self.visible[x][y] = 'F'

    def flagging(self, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        if self.visible[x][y] == ' ':
            self.visible[x][y] = 'F'
            return True
        elif self.visible[x][y] == 'F':
            self.visible[x][y] = ' '
            return True
        return False

    def count_surround_mines(self, x, y):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.back[nx][ny] == 'X':
                        count += 1
        return count

    def count_numbers(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.back[x][y] != 'X':
                    count = self.count_surround_mines(x, y)
                    if count > 0:
                        self.back[x][y] = str(count)
                    else:
                        self.back[x][y] = ' '

    def reveal(self, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height):
            return True
        if self.first_click:
            self.place_mines(x, y)

            self.first_click = False

        if self.back[x][y] == 'X' and self.visible[x][y] != 'F':
            self.visible[x][y] = 'X'
            self.game_over = True
            return False

        if self.finish_reveal[x][y] == '1':
            return True

        if self.back[x][y] != ' ' and self.back[x][y] != 'X':
            self.visible[x][y] = self.back[x][y]
            self.finish_reveal[x][y] = '1'

        if self.visible[x][y] == 'F':
            print("已标记")
            return True

        if self.back[x][y] == ' ':
            self.visible[x][y] = 'w'
            self.w_cell_lit[x][y] = '0'
            self.finish_reveal[x][y] = '1'
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        if dx != 0 or dy != 0:
                            if self.w_cell_lit[nx][ny] != '0':
                                self.reveal(nx, ny)
                            elif self.back[nx][ny] == 'X':
                                pass
        self.check_win()
        return True

    def check_win(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.back[x][y] != 'X' and self.visible[x][y] == ' ':
                    return
        self.win = True

    def play(self):

        while not self.game_over and not self.win:
            self.display_board()
            command = input("\n请输入命令: ").strip().split()
            if command[0] == 'q':
                print("游戏结束！")
                break

            if len(command) != 3:
                print("无效命令！请使用格式: r x y 或 f x y")
                continue

            action = command[0]
            a, b = command[1], command[2]

            if not a.isdigit() or not b.isdigit():
                print("无效输入！请确保 x 和 y 是正整数")
                continue

            x = int(a) - 1
            y = int(b) - 1

            if not (0 <= x < self.width and 0 <= y < self.height):
                print("坐标超出范围，请重新输入")
            if action == 'r':
                if not self.reveal(x, y):
                    self.display_board()
                    break
            elif action == 'f':
                self.flagging(x, y)
            else:
                print("无效操作！请使用 'r' 或 'f'")
        if self.game_over or self.win:
            self.reveal_all()
            self.display_board()
            if self.win:
                print("你赢了")
            else:
                print("游戏结束，你踩到地雷了")


def choose_difficulty():
    while True:
        print("\n选择难度:")
        print("1. 初级 (9x9, 10个地雷)")
        print("2. 中级 (16x16, 40个地雷)")
        print("3. 高级 (16x30, 99个地雷)")
        print("4. 退出")

        choice = input("请选择 (1-4): ").strip()

        if choice == '1':
            return 9, 9, 10
        elif choice == '2':
            return 16, 16, 40
        elif choice == '3':
            return 16, 30, 99
        elif choice == '4':
            return None
        else:
            print("无效选择,重新输入")


def main():
    print("扫雷")
    print("_" * 30)

    while True:
        choose = choose_difficulty()
        if choose is None:
            print("再见！")
            break

        width, height, mines = choose
        game = SL(width, height, mines)
        game.play()

        play_again = input("\n再玩一次？(y/n): ")
        if play_again == 'n':
            print("再见！")
            break
        else:
            print('离开点q+回车')


if __name__ == "__main__":
    main()
