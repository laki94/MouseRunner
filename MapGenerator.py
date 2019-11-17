import random


class ETooManyIterations(Exception):
    pass


class MapGen:
    def __init__(self, size, name):
        self.name = name
        self.size = size
        self.fields = [[0 for x in range(self.size)] for y in range(self.size)]
        self.fields[0][0] = 1
        self.actX, self.actY = 0, 0
        self.validFields = []
        self.loop_count = 0

    def __can_go_left(self):
        return (self.actX != 0) and (self.fields[self.actY][self.actX - 1] == 0) and (((self.actY == 0) or (self.fields[self.actY - 1][self.actX - 1] == 0)) and ((self.actY == self.size - 1) or (self.fields[self.actY + 1][self.actX - 1] == 0)) and ((self.actX < 1) or (self.fields[self.actY][self.actX - 2] == 0)))# and ((self.actX != self.size - 2) or (self.actY != self.size - 2))

    def __can_go_right(self):
        return (self.actX != (self.size - 1)) and (self.fields[self.actY][self.actX + 1] == 0) and (((self.actY == 0) or (self.fields[self.actY - 1][self.actX + 1] == 0)) and ((self.actY == self.size - 1) or (self.fields[self.actY + 1][self.actX + 1] == 0)) and ((self.size - self.actX < 3) or self.fields[self.actY][self.actX + 2] == 0))# or ((self.actX == self.size - 2) and (self.actY == self.size - 2))

    def __can_go_up(self):
        return (self.actY != 0) and (self.fields[self.actY - 1][self.actX] == 0) and (((self.actX == 0) or (self.fields[self.actY - 1][self.actX - 1] == 0)) and ((self.actX == (self.size - 1)) or (self.fields[self.actY - 1][self.actX + 1] == 0)) and ((self.actY < 1) or (self.fields[self.actY - 2][self.actX] == 0)))# and ((self.actX != self.size - 2) or (self.actY != self.size - 2))

    def __can_go_down(self):
        return (self.actY != (self.size - 1)) and (self.fields[self.actY + 1][self.actX] == 0) and (((self.actX == 0) or (self.fields[self.actY + 1][self.actX - 1] == 0)) and ((self.actX == (self.size - 1)) or (self.fields[self.actY + 1][self.actX + 1] == 0)) and ((self.size - self.actY < 3) or (self.fields[self.actY + 2][self.actX] == 0)))# or ((self.actX == self.size - 2) and (self.actY == self.size - 2))

    def __maze_ended(self):
        return ((self.actX == self.size - 2) and (self.actY == self.size - 1)) or ((self.actX == self.size - 1) and (self.actY == self.size - 2))

    def __add_border(self):
        tmp_arr = [[0 for x in range(self.size + 2)] for y in range(self.size + 2)]
        for y in range(self.size + 2):
            if y == 0 or y == self.size + 1:
                pass
            else:
                for x in range(self.size + 1):
                    if (x == 0) or (x == self.size + 2):
                        pass
                    else:
                        tmp_arr[y][x] = self.fields[y - 1][x - 1]
        tmp_arr[0][0] = tmp_arr[0][1] = tmp_arr[1][0] = 2
        self.fields = tmp_arr

    def __finish_maze(self):
        if len(self.fields) > 0:
            self.fields[self.size - 1][self.size - 1] = 1
            self.fields[0][0] = 2
            self.fields[self.size - 1][self.size - 1] = 3
            self.__add_border()

    def __get_possible_moves(self):
        valid_fields = []
        if self.__can_go_left():
            valid_fields.append([self.actX - 1, self.actY])
        if self.__can_go_right():
            valid_fields.append([self.actX + 1, self.actY])
        if self.__can_go_up():
            valid_fields.append([self.actX, self.actY - 1])
        if self.__can_go_down():
            valid_fields.append([self.actX, self.actY + 1])
        return valid_fields

    def __do_generate_maze(self):
        self.loop_count = self.loop_count + 1
        if self.loop_count > 30000:
            raise ETooManyIterations
        fields = self.__get_possible_moves()
        while len(fields) > 0:
            next_move = random.choice(fields)
            fields.remove(next_move)
            self.actX = next_move[0]
            self.actY = next_move[1]
            self.fields[self.actY][self.actX] = 1
            if self.__maze_ended():
                return True
            if self.__do_generate_maze():
                return True
            else:
                self.actX = next_move[0]
                self.actY = next_move[1]
                self.fields[self.actY][self.actX] = 0
        return False

    def generate_map(self, after_generate):
        print('%s: start generating maze' % self.name)
        while True:
            try:
                self.__do_generate_maze()
                break
            except RecursionError:
                print('%s: recursion error' % self.name)
                self.fields = []
                break
            except ETooManyIterations:
                print('%s: too many loops, trying again' % self.name)
                self.fields = [[0 for x in range(self.size)] for y in range(self.size)]
                self.fields[0][0] = 1
                self.actX, self.actY = 0, 0
                self.validFields = []
                self.loop_count = 0

        print('%s: maze generated, finishing, loops: %d' % (self.name, self.loop_count))
        self.__finish_maze()
        print('%s: maze finished, doing callback' % self.name)
        after_generate(self.fields)
