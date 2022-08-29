from random import randint

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"

class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"

class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"

class BoardWrongShipException(BoardException):
    pass

class Cell(object):
    empty_cell = '0'
    ship_cell = '■'
    damaged_ship = 'X'
    miss_cell = '•'

class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l      # длина корабля
        self.o = o      # ориентация корабля
        self.lives = l  # кол-во жизни корабля = длине корабля

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots


    def shooten(self, shot):
        return shot in self.dots

class Board:
    def __init__(self, size, hid = False):
        self.size = size
        self.hid = hid
        self.count = 0
        self.field = [[Cell.empty_cell for _ in range(size)] for _ in range(size)]

        self.busy = []
        self.ships = []

    def add_ship(self, ship):

        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = Cell.ship_cell
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb = False):
        near = [
            (-1, -1), (-1, 0) , (-1, 1),
            (0, -1), (0, 0) , (0 , 1),
            (1, -1), (1, 0) , (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not(self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = Cell.miss_cell
                    self.busy.append(cur)


    def __str__(self):
        res = ""
        if self.hid:
            for i in range(0, self.size):
                for j in range(0, len(self.field[i])):
                    if self.field[i][j] == Cell.ship_cell:
                        self.field[i][j]= Cell.empty_cell
                        continue

        for y in range(-1, self.size):
            for x in range(-1, self.size):
                if x == -1 and y == -1:
                    print("  ", end="")
                    continue
                if x == -1 and y >= 0:
                    print(y + 1 , end=" ")
                    continue
                if x >= 0 and y == -1:
                    print("",letters[x], end='')
                    continue
                print(" " + self.field[x][y], end='')
            print("")
        return res

    def out(self, d):
        return not((0<= d.x < self.size) and (0<= d.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = Cell.damaged_ship
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb = True)
                    print("Корабль уничтожен!")
                    return True
                else:
                    print("Корабль ранен!")
                    return True

        self.field[d.x][d.y] = Cell.miss_cell #"."
        print("Мимо!")
        return False


    def begin(self):
        self.busy = []

class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)

class AI(Player):
    def ask(self):
        d = Dot(randint(0,5), randint(0, 5))
        print(f"Ход компьютера: {d.x+1} {d.y+1}")
        return d

class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not(x.isdigit()) or not(y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x-1, y-1)

class Game:
    def __init__(self, size):
        self.size = size

        pl = self.user_place()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def user_place(self):
        board = Board(size = self.size)
        o = 0

        for i in range(len(ships_rules)):
            print(Board(field_size))
            while True:
                if int(ships_rules[i])>1:
                    place=input('Введите координаты левого верхнего угла ' + str(ships_rules[i]) + '-х клеточного корабля в формате X Y и направления корабля числом 0 - Вправо или 1 - Вниз:').split()
                    if len(place) != 3:
                        print(" Введите 3 координаты! ")
                        continue
                    x,y,o= place
                    if not(x.isdigit()) or not(y.isdigit()) or not(o.isdigit()):
                        print(" Введите числа! ")
                        continue
                    x,y,o= map(int, place)
                    if not(o == 0) and not (o == 1):
                        print("O - направления корабля числом 0 - Вправо или 1 - Вниз")
                        continue
                else:
                    place=input('Введите координаты ' + str(ships_rules[i]) + '-х клеточного корабля в формате X Y :').split()
                    if len(place) != 2:
                        print(" Введите 2 координаты! ")
                        continue
                    x,y = place
                    if not(x.isdigit()) or not(y.isdigit()):
                        print(" Введите числа! ")
                        continue
                    x,y= map(int, place)


                ship = Ship(Dot(x-1,y-1),ships_rules[i], o)
                try:
                    board.add_ship(ship)
                    print(board)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_place(self):
        board = Board(size = self.size)
        attempts = 0
        for l in ships_rules:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0,1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")


    def loop(self):
        num = 0
        while True:
            print("-"*20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-"*20)
            print("Доска компьютера:")
            print(self.ai.board)
            if num % 2 == 0:
                print("-"*20)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-"*20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == len(ships_rules):
                print("-"*20)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == len(ships_rules):
                print("-"*20)
                print("Компьютер выиграл!")
                break
            num += 1


    def start(self):
        self.greet()
        self.loop()

letters = ("1", "2", "3", "4", "5", "6")
field_size = len(letters)
ships_rules = [3, 2, 2, 1, 1, 1, 1]

g = Game(field_size)
g.start()





