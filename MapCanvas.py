import random

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics

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
                if ((i == 2) and (j == 1)) or ((i == 1) and (j == 2)) or ((i == (len(tiles) - 2)) and (j == (len(tiles) - 3))) or ((i == (len(tiles) - 2)) and (j == (len(tiles) - 3))):
                    pass
                else:
                    self.__draw_narrow_spot(tiles, i, j, tile_size, pointX, pointY, painter)
                pointX = pointX + tile_size
            pointX = 0
            pointY = pointY + tile_size
        painter.end()

    def __draw_narrow_spot(self, tiles, i, j, tile_size, pointX, pointY, painter):
        right = False
        left = False
        top = False
        bot = False
        nb = 0
        if tiles[i][j] == 1 and (tile_size > 15):
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
                    painter.drawRect(pointX, pointY + 2 * black_zone, tile_size, tile_size)
                elif top and bot:
                    painter.drawRect(pointX, pointY, black_zone, tile_size)
                    painter.drawRect(pointX + 2 * black_zone, pointY, tile_size, tile_size)
                elif top and left:
                    painter.drawRect(pointX, pointY, black_zone, black_zone)
                    painter.drawRect(pointX + 2 * black_zone, pointY, tile_size, tile_size)
                    painter.drawRect(pointX, pointY + 2 * black_zone, tile_size, tile_size)
                elif top and right:
                    painter.drawRect(pointX, pointY, black_zone, tile_size)
                    painter.drawRect(pointX + 2 * black_zone, pointY, tile_size, black_zone)
                    painter.drawRect(pointX, pointY + 2 * black_zone, tile_size, tile_size)
                elif bot and left:
                    painter.drawRect(pointX, pointY, tile_size, black_zone)
                    painter.drawRect(pointX, pointY + 2 * black_zone, black_zone, tile_size)
                    painter.drawRect(pointX + 2 * black_zone, pointY, tile_size, tile_size)
                elif bot and right:
                    painter.drawRect(pointX, pointY, tile_size, black_zone)
                    painter.drawRect(pointX, pointY, black_zone, tile_size)
                    painter.drawRect(pointX + 2 * black_zone, pointY + 2 * black_zone, tile_size, tile_size)

    def draw_map(self, tiles):
        self.__draw_original_map(tiles)

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
        pen.setColor(Qt.white)
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
