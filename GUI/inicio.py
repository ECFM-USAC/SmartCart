from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QIcon
from widgets import MainWidget, LogWidget, Dialog
import sys

server = False
app = QtWidgets.QApplication(sys.argv)
w = MainWidget()
y = Dialog()
y.setWindowTitle("Servidor")
w.show()
while not(w.server):
    if y.exec_() == QtWidgets.QDialog.Accepted:
        address = y.textBox1.text()
        name = y.textBox2.text()
        try:
            w.client.hostname = address
            w.client.connectToHost()
            w.server = True
        except:
            w.server = False
            print(u"Valores no válidos")
        if address == "":
            w.server = False
            print(u"Valores no válidos")
        else:
            print(u'Dirección: %s' % address)
            print('Usuario: %s' % name)
    else:
        w.server = False
        print('Cancelled')
        break
y.deleteLater()
sys.exit(app.exec_())
        
