import random
import numpy
import os


class MapGen:
    def __init__(self, size):
        self.size = size
        self.fields = [[0 for x in range(self.size)] for y in range(self.size)]
        self.fields[0][0] = 1
        self.actX, self.actY = 0, 0
        self.validFields = []

    def __can_go_left(self):
        return (self.actX != 0) and (self.fields[self.actY][self.actX - 1] == 0) and (((self.actY == 0) or (self.fields[self.actY - 1][self.actX - 1] == 0)) and ((self.actY == self.size - 1) or (self.fields[self.actY + 1][self.actX - 1] == 0)) and ((self.actX < 1) or (self.fields[self.actY][self.actX - 2] == 0)))

    def __can_go_right(self):
        return (self.actX != (self.size - 1)) and (self.fields[self.actY][self.actX + 1] == 0) and (((self.actY == 0) or (self.fields[self.actY - 1][self.actX + 1] == 0)) and ((self.actY == self.size - 1) or (self.fields[self.actY + 1][self.actX + 1] == 0)) and ((self.size - self.actX < 3) or self.fields[self.actY][self.actX + 2] == 0))

    def __can_go_up(self):
        return (self.actY != 0) and (self.fields[self.actY - 1][self.actX] == 0) and (((self.actX == 0) or (self.fields[self.actY - 1][self.actX - 1] == 0)) and ((self.actX == (self.size - 1)) or (self.fields[self.actY - 1][self.actX + 1] == 0)) and ((self.actY < 1) or (self.fields[self.actY - 2][self.actX] == 0)))

    def __can_go_down(self):
        return (self.actY != (self.size - 1)) and (self.fields[self.actY + 1][self.actX] == 0) and (((self.actX == 0) or (self.fields[self.actY + 1][self.actX - 1] == 0)) and ((self.actX == (self.size - 1)) or (self.fields[self.actY + 1][self.actX + 1] == 0)) and ((self.size - self.actY < 3) or (self.fields[self.actY + 2][self.actX] == 0)))

    def __get_possible_moves(self):
        self.validFields.clear()
        # Sprawdzenie czy wokół 0 są jakieś 1
        if self.__can_go_left():
            self.validFields.append([self.actX - 1, self.actY])
        if self.__can_go_right():
            self.validFields.append([self.actX + 1, self.actY])
        if self.__can_go_up():
            self.validFields.append([self.actX, self.actY - 1])
        if self.__can_go_down():
            self.validFields.append([self.actX, self.actY + 1])

        # Jak nie ma 0 dookoła to wybieram najmniejszą wagę
        if len(self.validFields) == 0:
            leftVal, rightVal, topVal, botVal = 0, 0, 0, 0
            if self.actX == 0:
                rightVal = self.fields[self.actY][self.actX + 1]
            else:
                leftVal = self.fields[self.actY][self.actX - 1]
                if self.actX != self.size - 1:
                    rightVal = self.fields[self.actY][self.actX + 1]
            if self.actY == 0:
                botVal = self.fields[self.actY + 1][self.actX]
            else:
                topVal = self.fields[self.actY - 1][self.actX]
                if self.actY != self.size - 1:
                    botVal = self.fields[self.actY + 1][self.actX]
            if leftVal == 0:
                leftVal = 65535
            if rightVal == 0:
                rightVal = 65535
            if topVal == 0:
                topVal = 65535
            if botVal == 0:
                botVal = 65535
            if (leftVal <= rightVal) and (leftVal <= topVal) and (leftVal <= botVal):
                self.validFields.append([self.actX - 1, self.actY])
            elif (rightVal <= leftVal) and (rightVal <= topVal) and (rightVal <= botVal):
                self.validFields.append([self.actX + 1, self.actY])
            elif (topVal <= leftVal) and (topVal <= rightVal) and (topVal <= botVal):
                self.validFields.append([self.actX, self.actY - 1])
            else:
                self.validFields.append([self.actX, self.actY + 1])

    def __make_move(self):
        nextField = random.choice(self.validFields)
        self.actX = nextField[0]
        self.actY = nextField[1]
        print("choosen field ", [self.actX, self.actY])
        if self.fields[self.actY][self.actX] == 0:
            self.fields[self.actY][self.actX] = 1
        else:
            self.fields[self.actY][self.actX] = self.fields[self.actY][self.actX] + 1
            # obsługa błedu
            if self.fields[self.actY][self.actX] > 50:
                self.fields = [[0 for x in range(self.size)] for y in range(self.size)]
                self.fields[0][0] = 1
                self.actX, self.actY = 0, 0

    def __maze_ended(self):
        return ((self.actX == self.size - 2) and (self.actY == self.size - 1)) or ((self.actX == self.size - 1) and (self.actY == self.size - 2))

    def __remove_single_ones(self):
        for i in range(self.size):
            for j in range(self.size):
                neighbours = 0
                if ((j == 0) and (i == 0)) or ((j == self.size - 1) and (i == self.size - 1)):
                    continue
                if j != 0 and self.fields[i][j - 1] > 0:
                    neighbours = neighbours + 1
                if j != self.size - 1 and self.fields[i][j + 1] > 0:
                    neighbours = neighbours + 1
                if i != 0 and self.fields[i - 1][j] > 0:
                    neighbours = neighbours + 1
                if i != self.size - 1 and self.fields[i + 1][j] > 0:
                    neighbours = neighbours + 1

                if self.fields[i][j] == 1:
                    if neighbours != 2:
                        print('zmiana punktu', i, j, 'na 0 bo neighbours=', neighbours)
                        if j != 0:
                            print('left=', self.fields[i][j - 1])
                        if j != self.size - 1:
                            print('right=', self.fields[i][j + 1])
                        if i != 0:
                            print('top=', self.fields[i - 1][j])
                        if i != self.size - 1:
                            print('bot=', self.fields[i + 1][j])
                        self.fields[i][j] = 0

    def __repair_path_and_remove_remaining_values(self):
        for i in range(self.size):
            for j in range(self.size):
                neighbours = 0
                if ((i == 0) and (j == 0)) or ((i == self.size - 1) and (j == self.size - 1)):
                    # x = x + 1
                    continue
                if j != 0 and self.fields[i][j - 1] == 1:
                    neighbours = neighbours + 1
                if j != self.size - 1 and self.fields[i][j + 1] == 1:
                    neighbours = neighbours + 1
                if i != 0 and self.fields[i - 1][j] == 1:
                    neighbours = neighbours + 1
                if i != self.size - 1 and self.fields[i + 1][j] == 1:
                    neighbours = neighbours + 1

                if self.fields[i][j] > 1:
                    if neighbours > 1:
                        print("zmiana punktu", i, j, "na 1 bo teraz ma 2 i neighbours>1")
                        self.fields[i][j] = 1
                    else:
                        print("zmiana punktu", i, j, "na 0 bo teraz ma 2 i neighbours=", neighbours)
                        if j != 0:
                            print('left=', self.fields[i][j - 1])
                        if j != self.size - 1:
                            print('right=', self.fields[i][j + 1])
                        if i != 0:
                            print('top=', self.fields[i - 1][j])
                        if i != self.size - 1:
                            print('bot=', self.fields[i + 1][j])
                        self.fields[i][j] = 0

    def __clear_maze(self):
        self.__remove_single_ones()
        self.__repair_path_and_remove_remaining_values()

    def __finish_maze(self):
        print("maze ended")
        self.fields[self.size - 1][self.size - 1] = 1
        self.__clear_maze()
        self.fields[0][0] = 2
        self.fields[self.size - 1][self.size - 1] = 3

    def generate_map(self):
        try:
            os.remove("D:\\Projekty\\Python\\MouseRunner\\aa.txt")
        except FileNotFoundError:
            pass
        while True:
            self.__get_possible_moves()
            self.__make_move()
            f = open("D:\\Projekty\\Python\\MouseRunner\\aa.txt", 'ab')
            numpy.savetxt(f, self.fields, '%d')
            f.write(b"\n")
            f.close()
            # numpy.savetxt() ("D:\\Projekty\\Python\\MouseRunner\\aa.txt", self.fields, '%d')
            for i in self.fields:
                print(i)
            if self.__maze_ended():
                break
        self.__finish_maze()
        f = open("D:\\Projekty\\Python\\MouseRunner\\aa.txt", 'ab')
        numpy.savetxt(f, self.fields, '%d')
        f.write(b"\n")
        f.close()
        for i in self.fields:
            print(i)
        return self.fields
