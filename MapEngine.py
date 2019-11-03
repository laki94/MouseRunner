from PyQt5 import QtGui, QtWidgets, QtCore
from MapGenerator import MapGen
from PyQt5.QtGui import QColor, QPainter, QFontMetrics
import PyQt5
import pyautogui
import numpy
import threading
import time


white_color = '#ffffff'
MAPSIZE = 600
TILESIZE = 0.1


class Canvas(QtWidgets.QLabel):
    def __init__(self,):
        super().__init__()
        pixmap = QtGui.QPixmap(MAPSIZE, MAPSIZE)
        self.board_color = QtGui.QColor(white_color)
        pixmap.fill(self.board_color)
        self.setPixmap(pixmap)

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

    def show_won_map_info(self):
        self.__clear_canvas()
        self.__write_main_info_on_screen("Wygrana!")
        self.__write_info_on_screen("Generowanie mapy...")

    def show_lost_map_info(self):
        self.__clear_canvas()
        self.__write_main_info_on_screen("Porażka!")
        self.__write_info_on_screen("Generowanie mapy...")


def is_pointer_on_color(rgb, e):
    return pyautogui.pixelMatchesColor(e.globalPos().x(), e.globalPos().y(), rgb, 10)


def is_pointer_on_black_pixel(e):
    return is_pointer_on_color(QColor('black').getRgb(), e)


def is_pointer_on_green_pixel(e):
    return is_pointer_on_color(QColor('green').getRgb(), e)


def is_pointer_on_red_pixel(e):
    return is_pointer_on_color(QColor('red').getRgb(), e)


class Map(QtWidgets.QMainWindow):

    def __after_generate_callback(self, tiles):
        self.canvas.draw_map(tiles)
        time.sleep(1)
        self.update()
        self.__set_start_pos_pointer()
        self.generating_map = False

    def __generate_random_map(self):
        self.generating_map = True
        generated = MapGen(round(MAPSIZE / (MAPSIZE * TILESIZE)))
        generated.generate_map(self.__after_generate_callback)

    def __init_ui(self):
        self.canvas = Canvas()
        self.l = QtWidgets.QVBoxLayout()
        w = QtWidgets.QWidget()
        w.setLayout(self.l)
        self.l.addWidget(self.canvas)
        self.setCentralWidget(w)
        w.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

    def __init__(self, ):
        super().__init__()
        self.__init_ui()
        self.canvas.show_loading_map_info()
        self.setMouseTracking(True)
        self.score = 0

    def __center(self):
        frame_gm = self.frameGeometry()
        screen = PyQt5.QtWidgets.QApplication.desktop().screenNumber(
            PyQt5.QtWidgets.QApplication.desktop().cursor().pos())
        center_point = PyQt5.QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

    def __set_start_pos_pointer(self):
        self.act_pos = (self.mapToGlobal(self.centralWidget().pos()).x() - 8 + round(MAPSIZE * TILESIZE),
                          self.mapToGlobal(self.centralWidget().pos()).y() - 8 + round(MAPSIZE * TILESIZE))
        pyautogui.moveTo(self.act_pos)

    def __set_score_text(self):
        self.setWindowTitle("MouseRunner - Wynik: %d" % self.score)

    def __new_game(self):
        threading.Thread(target=self.__generate_random_map).start()
        self.__set_score_text()

    def show(self):
        super(Map, self).show()
        self.__center()
        self.__new_game()

    def __did_pointer_jump(self, e):
        tmp_pos = (e.globalPos().x(), e.globalPos().y())
        val = numpy.abs(numpy.subtract(self.act_pos, tmp_pos))
        return any(val > (MAPSIZE * TILESIZE)) and (not is_pointer_on_red_pixel(e))

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
            if is_pointer_on_black_pixel(e) or self.__did_pointer_jump(e):
                self.__do_on_game_lost()
            elif is_pointer_on_green_pixel(e):
                self.__do_on_game_won()
            else:
                self.act_pos = (e.globalPos().x(), e.globalPos().y())

    def keyPressEvent(self, ev):
        if self.generating_map:
            pass
        else:
            if ev.key() == QtCore.Qt.Key_R:
                self.canvas.show_loading_map_info()
                self.__do_on_new_game()
