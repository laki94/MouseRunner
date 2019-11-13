from PyQt5 import QtGui, QtWidgets, QtCore
from aenum import enum

from MapGenerator import MapGen
from PyQt5.QtGui import QColor, QPainter, QFontMetrics
from PyQt5.QtCore import Qt
import PyQt5
import numpy
import threading
import time
import win32api
import win32gui
import math
import random

MAPSIZE = 600


class Canvas(QtWidgets.QLabel):
    def __init__(self, tile_size):
        super().__init__()
        self.tile_size = tile_size
        pixmap = QtGui.QPixmap(MAPSIZE, MAPSIZE)
        self.setPixmap(pixmap)

    def __draw_original_map(self, tiles):
        self.pixmap().fill(Qt.black)
        painter = QtGui.QPainter(self.pixmap())
        pen = QtGui.QPen(Qt.SolidLine)
        pointX = 0
        pointY = 0
        tile_size = self.width() // len(tiles)
        for i in range(len(tiles)):
            for j in range(len(tiles[i])):
                right = False
                left = False
                top = False
                bot = False
                nb = 0
                if tiles[i][j] == 0:
                    pen.setColor(Qt.black)
                    painter.setBrush(QtGui.QBrush(Qt.black, Qt.SolidPattern))
                elif tiles[i][j] == 1:
                    pen.setColor(Qt.white)
                    painter.setBrush(QtGui.QBrush(Qt.white, Qt.SolidPattern))
                elif tiles[i][j] == 2:
                    pen.setColor(Qt.red)
                    painter.setBrush(QtGui.QBrush(Qt.red, Qt.SolidPattern))
                elif tiles[i][j] == 3:
                    pen.setColor(Qt.green)
                    painter.setBrush(QtGui.QBrush(Qt.green, Qt.SolidPattern))
                painter.setPen(pen)
                painter.drawRect(pointX, pointY, tile_size, tile_size)

                if tiles[i][j] == 1 and (tile_size > 15): #TODO przeniesc do funkcji
                    rand_int = random.randint(0, 100)
                    if rand_int < 20:
                        if (j < len(tiles) - 2) and (tiles[i][j + 1] == 1):
                            right = True
                            nb = nb + 1
                        if (j > 2) and (tiles[i][j - 1] == 1):
                            left = True
                            nb = nb + 1
                        if (i < len(tiles) - 2) and (tiles[i + 1][j] == 1):
                            bot = True
                            nb = nb + 1
                        if (i > 2) and (tiles[i - 1][j] == 1):
                            top = True
                            nb = nb + 1
                        if nb != 2:
                            pass
                        painter.setPen(QtGui.QPen(Qt.black, Qt.SolidLine))
                        painter.setBrush(QtGui.QBrush(Qt.black, Qt.SolidPattern))
                        black_zone = tile_size // 3
                        if left and right:
                            painter.drawRect(pointX, pointY, tile_size, black_zone)
                            painter.drawRect(pointX, pointY + 2*black_zone, tile_size, tile_size)
                        elif top and bot:
                            painter.drawRect(pointX, pointY, black_zone, tile_size)
                            painter.drawRect(pointX + 2*black_zone, pointY, tile_size, tile_size)
                        elif top and left:
                            painter.drawRect(pointX, pointY, black_zone, black_zone)
                            painter.drawRect(pointX + 2 *black_zone, pointY, tile_size, tile_size)
                            painter.drawRect(pointX, pointY + 2*black_zone, tile_size, tile_size)
                        elif top and right:
                            painter.drawRect(pointX, pointY, black_zone, tile_size)
                            painter.drawRect(pointX + 2*black_zone, pointY, tile_size, black_zone)
                            painter.drawRect(pointX, pointY + 2*black_zone, tile_size, tile_size)
                        elif bot and left:
                            painter.drawRect(pointX, pointY, tile_size, black_zone)
                            painter.drawRect(pointX, pointY + 2*black_zone, black_zone, tile_size)
                            painter.drawRect(pointX + 2*black_zone, pointY, tile_size, tile_size)
                        elif bot and right:
                            painter.drawRect(pointX, pointY, tile_size, black_zone)
                            painter.drawRect(pointX, pointY, black_zone, tile_size)
                            painter.drawRect(pointX + 2 * black_zone, pointY + 2* black_zone, tile_size, tile_size)
                pointX = pointX + tile_size
            pointX = 0
            pointY = pointY + tile_size
        painter.end()

    def __do_draw_narrow_line_horizontal(self, i, j, tile_size):
        painter = QtGui.QPainter(self.pixmap())
        pen = QtGui.QPen(Qt.SolidLine)
        pointX = j * tile_size
        pointY = i * tile_size
        painter.setPen(QtGui.QPen(Qt.black, Qt.SolidLine))
        painter.setBrush(QtGui.QBrush(Qt.black, Qt.SolidPattern))
        black_zone = round(tile_size / 3)
        painter.drawRect(pointX, pointY, tile_size - 1, black_zone)
        painter.drawRect(pointX, pointY + 2*black_zone, tile_size - 1, black_zone)
        painter.end()

    def __do_draw_narrow_line_vertical(self, i, j, tile_size):
        painter = QtGui.QPainter(self.pixmap())
        pen = QtGui.QPen(Qt.SolidLine)
        pointX = j * tile_size
        pointY = i * tile_size
        painter.setPen(QtGui.QPen(Qt.black, Qt.SolidLine))
        painter.setBrush(QtGui.QBrush(Qt.black, Qt.SolidPattern))
        black_zone = round(tile_size / 3)
        painter.drawRect(pointX, pointY, black_zone, tile_size - 1)
        painter.drawRect(pointX + 2 * black_zone, pointY, black_zone, tile_size - 1)
        painter.end()

                # elif left and top:
                #     __do_draw_narrow_l_left_to_top(i, j) # TODO reszta, i sprawdzic na wyzszym lvl i ekranie czy wszystko ok
                # elif left and bot:
                #     __do_draw_narrow_l_left_to_bot(i, j)
                # elif right and top:
                #     __do_draw_narrow_l_right_to_top(i, j)
                # elif right and bot:
                #     __do_draw_narrow_l_right_to_bot(i, j)


    def draw_map(self, tiles):
        self.__draw_original_map(tiles)
        # self.__narrow_map(tiles)

    def __write_info_on_screen(self, text):
        painter = QtGui.QPainter(self.pixmap())
        font = painter.font()
        font.setPixelSize(48)
        painter.setFont(font)
        pointX = round(MAPSIZE / 2)
        pointY = pointX
        fm = QFontMetrics(font)
        text_width = fm.width(text) / 2
        text_height = fm.height() / 2
        rectangle = QtCore.QRect(pointX - text_width, pointY - text_height, pointX + text_width, pointY + text_height)
        painter.drawText(rectangle, 0, text)

    def __clear_canvas(self):
        painter = QtGui.QPainter(self.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(MAPSIZE)
        pointX = round(MAPSIZE / 2)
        pointY = pointX
        pen.setColor(QtGui.QColor('white'))
        painter.setPen(pen)
        painter.drawPoint(pointX, pointY)
        painter.end()

    def show_loading_map_info(self):
        self.__clear_canvas()
        self.__write_info_on_screen("Generowanie mapy...")

    def __write_main_info_on_screen(self, text):
        painter = QtGui.QPainter(self.pixmap())
        font = painter.font()
        font.setPixelSize(48)
        painter.setFont(font)
        pointX = round(MAPSIZE / 2)
        pointY = pointX
        fm = QFontMetrics(font)
        text_width = fm.width(text) / 2
        text_height = fm.height() / 2
        rectangle = QtCore.QRect(pointX - text_width, pointY - 3 * text_height, pointX + text_width, pointY - text_height)
        painter.drawText(rectangle, 0, text)
        painter.end()

    def show_won_map_info(self):
        self.__clear_canvas()
        self.__write_main_info_on_screen("Wygrana!")
        self.__write_info_on_screen("Generowanie mapy...")

    def show_lost_map_info(self):
        self.__clear_canvas()
        self.__write_main_info_on_screen("Porażka!")
        self.__write_info_on_screen("Generowanie mapy...")


def get_pixel_colour(i_x, i_y):
    i_desktop_window_id = win32gui.GetDesktopWindow()
    i_desktop_window_dc = win32gui.GetWindowDC(i_desktop_window_id)
    long_colour = win32gui.GetPixel(i_desktop_window_dc, i_x, i_y)
    i_colour = int(long_colour)
    return (i_colour & 0xff), ((i_colour >> 8) & 0xff), ((i_colour >> 16) & 0xff)


def is_pointer_on_color(rgb, pos):
    act_color = get_pixel_colour(pos[0], pos[1])
    return (abs(act_color[0] - rgb[0]) + abs(act_color[1] - rgb[1]) + abs(act_color[2] - rgb[2])) < 10


def is_pointer_on_black_pixel(pos):
    return is_pointer_on_color(QColor(Qt.black).getRgb(), pos)


def is_pointer_on_green_pixel(pos):
    return is_pointer_on_color(QColor(Qt.green).getRgb(), pos)


def is_pointer_on_red_pixel(pos):
    return is_pointer_on_color(QColor(Qt.red).getRgb(), pos)


class Map(QtWidgets.QMainWindow):

    def __after_generate_callback(self, tiles):
        self.map_tiles = tiles
        self.canvas.draw_map(self.map_tiles)
        time.sleep(1)
        self.update()
        self.__set_start_pos_pointer()
        self.generating_map = False

    def __generate_random_map(self):
        self.generating_map = True
        generated = MapGen(round(MAPSIZE / (MAPSIZE * self.tile_size)))
        generated.generate_map(self.__after_generate_callback)

    def __init_ui(self):
        self.canvas = Canvas(self.tile_size)
        self.l = QtWidgets.QVBoxLayout()
        w = QtWidgets.QWidget()
        w.setLayout(self.l)
        self.l.addWidget(self.canvas)
        self.setCentralWidget(w)
        w.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

    def __init__(self,):
        super().__init__()
        self.map_tiles = []
        self.tile_size = 0.1
        self.__init_ui()
        self.canvas.show_loading_map_info()
        self.setMouseTracking(True)
        self.score = 0
        self.prev_dist = 0

    def __center(self):
        frame_gm = self.frameGeometry()
        screen = PyQt5.QtWidgets.QApplication.desktop().screenNumber(
            PyQt5.QtWidgets.QApplication.desktop().cursor().pos())
        center_point = PyQt5.QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

    def __set_start_pos_pointer(self):
        self.act_pos = (self.mapToGlobal(self.centralWidget().pos()).x() + self.canvas.pos().x() + round(MAPSIZE // len(self.map_tiles)),
                          self.mapToGlobal(self.centralWidget().pos()).y() + self.canvas.pos().y() + round(MAPSIZE // len(self.map_tiles)))
        win32api.SetCursorPos(self.act_pos)

    def __set_score_text(self):
        self.setWindowTitle("MouseRunner - Wynik: %d" % self.score)

    def __new_game(self):
        if 0.1 - ((self.score // 3) / 100) < 0.1:
            self.tile_size = 0.1 - ((self.score // 3) / 100)
            self.canvas.tile_size = self.tile_size
        threading.Thread(target=self.__generate_random_map).start()
        self.__set_score_text()

    def show(self):
        super(Map, self).show()
        self.window_pos = self.pos()
        self.__center()
        self.__new_game()

    def __did_pointer_jump(self, pos):
        prev_x = abs(self.act_pos[0] - self.window_pos.x())
        prev_y = abs(self.act_pos[1] - self.window_pos.y())
        act_x = abs(pos[0] - self.pos().x())
        act_y = abs(pos[1] - self.pos().y())
        act_dist = math.sqrt(pow(abs(prev_x - act_x), 2) + pow(abs(prev_y - act_y), 2))
        if self.prev_dist < act_dist:
            self.prev_dist = act_dist - self.prev_dist
        else:
            self.prev_dist = act_dist
        if self.prev_dist > (abs(prev_x - act_x) + abs(prev_y - act_y)):
            self.prev_dist = abs((abs(prev_x - act_x) + abs(prev_y - act_y)) - self.prev_dist)
        else:
            self.prev_dist = (abs(prev_x - act_x) + abs(prev_y - act_y))
        print('distance: %d' % self.prev_dist)
        return (self.prev_dist > (MAPSIZE // len(self.map_tiles))) and (not is_pointer_on_red_pixel(pos))

    def __do_on_new_game(self):
        self.update()
        self.__new_game()

    def __do_on_game_lost(self):
        self.canvas.show_lost_map_info()
        self.score = self.score - 1
        self.__do_on_new_game()

    def __do_on_game_won(self):
        self.canvas.show_won_map_info()
        self.score = self.score + 1
        self.__do_on_new_game()

    def mouseMoveEvent(self, e):
        if self.generating_map:
            pass
        else:
            x = e.globalPos().x()
            y = e.globalPos().y()

            if (x < (self.mapToGlobal(self.centralWidget().pos()).x() + 15)) or (x > (self.mapToGlobal(self.centralWidget().pos()).x() + self.centralWidget().height()) - 15) or (y < (self.mapToGlobal(self.centralWidget().pos()).y() + 15)) or (y > (self.mapToGlobal(self.centralWidget().pos()).y() + self.centralWidget().height()) - 15):
                pass
            elif is_pointer_on_black_pixel((x, y)) or self.__did_pointer_jump((x, y)):
                print('pointer on black pixel')
                self.__do_on_game_lost()
            elif is_pointer_on_green_pixel((x, y)):
                self.__do_on_game_won()
            else:
                self.act_pos = (x, y)
                self.window_pos = self.pos()

    def keyPressEvent(self, ev):
        if self.generating_map:
            pass
        else:
            if ev.key() == QtCore.Qt.Key_R:
                self.canvas.show_loading_map_info()
                self.__do_on_new_game()
            elif ev.key() == QtCore.Qt.Key_W:
                self.__do_on_game_won()
            elif ev.key() == QtCore.Qt.Key_L:
                self.__do_on_game_lost()
