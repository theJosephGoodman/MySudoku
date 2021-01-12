from random import randint
import pickle
import sys
class Instruments:
    """класс для вспомогательных инструментов"""
    
    def findNextCellToFill(grid, i, j):
            """функция для нахождения следующей ячейки, чтобы ее заполнить"""
            for x in range(i,9):
                    for y in range(j,9):
                            if grid[x][y] == 0:
                                    return x,y
            for x in range(0,9):
                    for y in range(0,9):
                            if grid[x][y] == 0:
                                    return x,y
            return -1,-1
    
    def isValid(grid, i, j, e):
            """проверка элементов на валидность"""
            rowOk = all([e != grid[i][x] for x in range(9)])
            if rowOk:
                    columnOk = all([e != grid[x][j] for x in range(9)])
                    if columnOk:
                            # finding the top left x,y co-ordinates of the section containing the i,j cell
                            secTopX, secTopY = 3 *(i//3), 3 *(j//3) #floored quotient should be used here. 
                            for x in range(secTopX, secTopX+3):
                                    for y in range(secTopY, secTopY+3):
                                            if grid[x][y] == e:
                                                    return False
                            return True
            return False
    
    def solveSudoku(grid, i=0, j=0, tracking = False):
            """решатель судоку"""
            i,j = Instruments.findNextCellToFill(grid, i, j)
            if i == -1:
                    return True
            for e in range(1,10):
                    if Instruments.isValid(grid,i,j,e):
                            grid[i][j] = e
                            
                            if tracking == True:
                                print(f'--Устанавливаем в координатах ({i},{j}) значение {e}--')
                            if Instruments.solveSudoku(grid, i, j, tracking=tracking):
                                    return True
                            # Undo the current cell for backtracking
                            grid[i][j] = 0
            return False
    
    def clear():
        """очистка игрвого поля"""
        print('\n' * 100)
    
    
    def swap_rows(field):
        """поменять местами строки"""
        row1 = randint(0, 1)
        row2 = row1 + 1
        k = randint(0, 2)
        row1, row2 = map(lambda x: x + 3 * k, [row1, row2])
        tmp = field[row1]
        field[row1] = field[row2]
        field[row2] = tmp
    
    
    def swap_cols(field):
        """поменять местами столбцы"""
        col1 = randint(0, 1)
        col2 = col1 + 1
        k = randint(0, 2)
        col1, col2 = map(lambda x: x + 3 * k, [col1, col2])
        for i in range(9):
            tmp = field[i][col1]
            field[i][col1] = field[i][col2]
            field[i][col2] = tmp
    
    
    def transp(field):
        """транспонирование - тоже можно использовать как функцию для перемешивания судоку"""
        for i in range(9):
            for j in range(9):
                tmp = field[i][j]
                field[i][j] = field[j][i]
                field[j][i] = tmp


class Session:
    """класс нашей игры"""
    
    def start_menu(self):
        """запуск стартового меню и начало игры"""
        
        self.state = int(input("Выберите режим\n \t1 - играть самому \n\t2 - дать играть алгоритму \nВведите число: "))
        Instruments.clear()
        if self.state == 1:
            self.stage = int(input("Загрузить сохрание или начать новую игру?\n"
                          "\t 1 - Новая игра\n"
                          "\t 2 - Загрузить сохрание\n"))
            Instruments.clear()
            if self.stage == 1:
                self.set_field(int(input("Укажите количество заполненных ячеек:\n")))
                Instruments.clear()
                self.print_field()
            elif self.stage == 2:
                self.load_game()
                Instruments.clear()
                self.print_field()
            while True:
                inp = input("Напишите 'end', чтобы покинуть игру\n"
                    "Напишите 'save', чтобы сохранить игру, или же\n"
                    "Впишите ваш ход в формате <<row column number>>, чтобы поставить число на игровое поле:\n")
                if inp == 'save':
                    self.save_game()
                    Instruments.clear()
                    self.print_field()
                    print('Game saved')
                elif inp == 'end':
                    break
                else:
                    inp = list(map(lambda x: int(x), inp.split(' ')))
                    self.get_num(inp[0], inp[1], inp[2])
                    self.print_field()
                    
                    temp = True
                    for i in self.field:
                        if 0 in i:
                            temp = False
                    if temp == True:
                        break
                            
            if self.check_sol():
                print('Поздравляем с победой!')
                
            else:
                print('Игра проиграна')
                
        elif self.state == 2:
            self.set_field(int(input("Укажите количество заполненных ячеек:\n")))
    # clear()
            self.print_field()
            
            print('Отображать производимые вычисления? 1 - да, 2 - нет')
            if int(input('Введите число: '))==1:
                self.tracking = True
            else:
                self.tracking = False
            
            input("Нажмите 'Enter', чтобы победить в игре:\n")
    # clear()
            Instruments.solveSudoku(self.field, tracking=self.tracking)
            self.print_field()
        elif self.state == 'exit':
            print('Выходим из игры')
            sys.exit(0)
            
    def __init__(self):
        """конструктор нашего класса"""
        
       # self.state = state
        self.stage = None
        self.field = None
        self.n = None
        self.start_menu()

    def set_field(self, n):
        """создание игрового поля"""
        
        self.n = n
        self.field = [[((j * 3 + j // 3 + i) % 9 + 1) for i in range(9)] for j in range(9)]
        cnt = 0
        while cnt < 81 - n:
            i = randint(0, 8)
            j = randint(0, 8)
            if self.field[i][j] != 0:
                self.field[i][j] = 0
                cnt += 1
        for i in range(randint(15, 30)):
            Instruments.swap_cols(self.field)
        for i in range(randint(15, 30)):
            Instruments.swap_rows(self.field)
        for i in range(randint(0, 1)):
            Instruments.transp(self.field)

    def print_field(self):
        """вывод игрового поля"""
        print("   ", end='')
        for i in range(9):
            print("[{}]".format(i+1)+(" " if (i + 1) % 3 == 0 else ""), end='')
        print("")
        for i in range(9):
            print("[{}]".format(i+1), end=' ')
            for j in range(9):
                print(self.field[i][j], ("|" if (j + 1) % 3 == 0 else ""), end=' ')
            print(('\n    ' + "-" * 28) if (i + 1) % 3 == 0 else "")

    def get_num(self, i, j, n):
        """получить число по его координатам"""
        self.field[i-1][j-1] = n

    def check_sol(self):
        """проверка решения"""
        flag = True
        for row in self.field:
            if len(set(row)) != 9:
                flag = False
        for i in range(9):
            set_arr = set([self.field[j][i] for j in range(9)])
            if len(set_arr) != 9:
                flag = False
        for i in range(0, 7, 3):
            for j in range(0, 7, 3):
                set_arr = []
                arr = [row[j:(j+3)] for row in self.field[i:(i+3)]]
                for row in arr:
                    set_arr += list(row)
                if len(set(set_arr)) != 9:
                    flag = False
        return flag

    def save_game(self):
        """сохранить игру"""
        
        with open('data.pickle', 'wb') as f:                
            pickle.dump(self.field, f)

    def load_game(self):
        """загрузить игру"""
        
        with open('data.pickle', 'rb') as f:
            self.field = pickle.load(f)
            
# создаем экземпляр нашей игры
session = Session()