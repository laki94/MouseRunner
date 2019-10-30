from PyQt5 import QtGui, QtWidgets
from TileEnum import Tile
from MapGenerator import MapGen
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QColor, QPainter

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
                    pen.setColor(QtGui.QColor('white'))
                elif j == 1:
                    pen.setColor(QtGui.QColor('black'))
                elif j == 2:
                    pen.setColor(QtGui.QColor('red'))
                else:
                    pen.setColor(QtGui.QColor('blue'))
                painter.setPen(pen)
                painter.drawPoint(pointX, pointY)
                pointX = pointX + round(MAPSIZE * TILESIZE)
            pointX = round(MAPSIZE * TILESIZE) / 2
            pointY = pointY + round(MAPSIZE * TILESIZE)
        painter.end()


class Map(QtWidgets.QMainWindow):

    def generatemap(self):
        generated = MapGen(round(MAPSIZE / (MAPSIZE * TILESIZE)))
        stage1 = MapSetting("Stage 1", generated.generate_map())
        self.canvas = Canvas()
        self.title = QtWidgets.QLabel()
        self.title.setText(stage1.map_name)
        self.canvas.draw_map(stage1.tiles)
        self.l = QtWidgets.QVBoxLayout()
        w = QtWidgets.QWidget()
        w.setLayout(self.l)
        self.l.addWidget(self.title)
        self.l.addWidget(self.canvas)
        self.setCentralWidget(w)

    def __init__(self, ):
        super().__init__()
        self.generatemap()
