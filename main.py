import sys
from PyQt5 import QtWidgets
from MapEngine import Map

app = QtWidgets.QApplication(sys.argv)

window = Map()
window.show()
app.exec_()
