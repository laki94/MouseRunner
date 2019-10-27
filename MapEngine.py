from PyQt5 import QtGui, QtWidgets

black_color = '#000000'
white_color = '#ffffff'


class Canvas(QtWidgets.QLabel):
    def __init__(self, ):
        super().__init__()
        pixmap = QtGui.QPixmap(600, 300)
        self.board_color = QtGui.QColor(white_color)
        pixmap.fill(self.board_color)
        self.setPixmap(pixmap)
        self.last_x, self.last_y = None, None


class Map(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.canvas = Canvas()
        w = QtWidgets.QWidget()
        l = QtWidgets.QVBoxLayout()
        w.setLayout(l)
        l.addWidget(self.canvas)
        self.setCentralWidget(w)
