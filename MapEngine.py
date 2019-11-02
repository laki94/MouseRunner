import keyboard
from PyQt5 import QtGui, QtWidgets, QtCore
from TileEnum import Tile
from MapGenerator import MapGen
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QColor, QPainter
import PyQt5
import pyautogui

from MapSetting import MapSetting

black_color = '#000000'
white_color = '#ffffff'
MAPSIZE = 600
TILESIZE = 0.05 #0.05 max


class Canvas(QtWidgets.QLabel):
    def __init__(self,):
        super().__init__()
        pixmap = QtGui.QPixmap(MAPSIZE, MAPSIZE)
        self.board_color = QtGui.QColor(white_color)
        pixmap.fill(self.board_color)
        self.setPixmap(pixmap)
        self.last_x, self.last_y = None, None

    def draw_map(self, tiles):
        painter = QtGui.QPainter(self.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(round(MAPSIZE * TILESIZE))
        pointX = round(MAPSIZE * TILESIZE) / 2
        pointY = pointX
        for i in tiles:
            for j in i:
                if j == 0:
                    pen.setColor(QtGui.QColor('black'))
                elif j == 1:
                    pen.setColor(QtGui.QColor('white'))
                elif j == 2:
                    pen.setColor(QtGui.QColor('red'))
                elif j == 3:
                    pen.setColor(QtGui.QColor('green'))
                painter.setPen(pen)
                painter.drawPoint(pointX, pointY)
                pointX = pointX + round(MAPSIZE * TILESIZE)
            pointX = round(MAPSIZE * TILESIZE) / 2
            pointY = pointY + round(MAPSIZE * TILESIZE)
        painter.end()


def is_pointer_on_black_pixel(e):
    return pyautogui.pixelMatchesColor(e.globalPos().x(), e.globalPos().y(), QColor('black').getRgb(), 10)


class Map(QtWidgets.QMainWindow):

    def __generate_map(self):
        generated = MapGen(round(MAPSIZE / (MAPSIZE * TILESIZE)))
        stage1 = MapSetting("Stage 1", generated.generate_map())
        self.canvas = Canvas()
        self.canvas.draw_map(stage1.tiles)
        self.l = QtWidgets.QVBoxLayout()
        w = QtWidgets.QWidget()
        w.setLayout(self.l)
        self.l.addWidget(self.canvas)
        self.setCentralWidget(w)
        w.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

    def __init__(self, ):
        super().__init__()
        self.__generate_map()
        self.setMouseTracking(True)

    def __center(self):
        frame_gm = self.frameGeometry()
        screen = PyQt5.QtWidgets.QApplication.desktop().screenNumber(
            PyQt5.QtWidgets.QApplication.desktop().cursor().pos())
        center_point = PyQt5.QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

    def __set_start_pos_pointer(self):
        pyautogui.moveTo(self.mapToGlobal(self.centralWidget().pos()).x() - 8 + round(MAPSIZE * TILESIZE),
                         self.mapToGlobal(self.centralWidget().pos()).y() - 8 + round(MAPSIZE * TILESIZE))

    def __new_game(self):
        self.__generate_map()
        self.__set_start_pos_pointer()
        self.update()

    def show(self):
        super(Map, self).show()
        self.__center()
        self.__new_game()

    def mouseMoveEvent(self, e):
        if is_pointer_on_black_pixel(e):
            self.__new_game()

    def keyPressEvent(self, ev):
        self.__new_game()
