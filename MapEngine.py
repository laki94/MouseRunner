from PyQt5 import QtGui, QtWidgets
from TileEnum import Tile
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QColor, QPainter

from MapSetting import MapSetting

black_color = '#000000'
white_color = '#ffffff'
MAPSIZE = 300
TILESIZE = 0.1


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
            if i == Tile.WHITE:
                pen.setColor(QtGui.QColor('white'))
            elif i == Tile.BLACK:
                pen.setColor(QtGui.QColor('black'))
            elif i == Tile.RED:
                pen.setColor(QtGui.QColor('red'))
            painter.setPen(pen)
            painter.drawPoint(pointX, pointY)
            if pointX + round(MAPSIZE * TILESIZE) > MAPSIZE:
                pointX = round(MAPSIZE * TILESIZE) / 2
                pointY = pointY + round(MAPSIZE * TILESIZE)
            else:
                pointX = pointX + round(MAPSIZE * TILESIZE)

        painter.end()


class Map(QtWidgets.QMainWindow):
    def __init__(self,):
        super().__init__()
        stage1 = MapSetting("Stage 1", [Tile.WHITE, Tile.WHITE, Tile.WHITE, Tile.WHITE, Tile.WHITE, Tile.WHITE,
                                        Tile.WHITE, Tile.BLACK, Tile.BLACK, Tile.RED, Tile.BLACK, Tile.BLACK, Tile.RED])
        self.canvas = Canvas()
        title = QtWidgets.QLabel()
        title.setText(stage1.map_name)
        self.canvas.draw_map(stage1.tiles)
        w = QtWidgets.QWidget()
        l = QtWidgets.QVBoxLayout()
        w.setLayout(l)
        l.addWidget(title)
        l.addWidget(self.canvas)
        self.setCentralWidget(w)
