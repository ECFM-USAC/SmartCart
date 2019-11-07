from mqtt_process import MqttClient
from widgets import MainWidget, LogWidget, Dialog
from PyQt5 import QtWidgets, QtCore, QtGui
import sys

class signals(QtCore.QObject):   
    def MainWidgetSignals(self):
        self.chxAx.stateChanged.connect(actions.on_chx1)
        self.chxAy.stateChanged.connect(actions.on_chx2)
        self.chxAz.stateChanged.connect(actions.on_chx3)
        self.chxAcx.stateChanged.connect(actions.on_chx4)
        self.chxAcy.stateChanged.connect(actions.on_chx5)
        self.chxAcz.stateChanged.connect(actions.on_chx6)
        self.chxGx.stateChanged.connect(actions.on_chx7)
        self.chxGy.stateChanged.connect(actions.on_chx8)
        self.chxGz.stateChanged.connect(actions.on_chx9)
        self.chxVs.stateChanged.connect(actions.on_chx10)
        self.chxPs.stateChanged.connect(actions.on_chx11)
        self.chxI.stateChanged.connect(actions.on_chx12)        
        
class actions:
    def on_chx1(state):
        if (QtCore.Qt.Checked == state):
            w.state[0] = 1
        else:
            w.state[0] = 0

    def on_chx2(state):
        if (QtCore.Qt.Checked == state):
            w.state[1] = 1
        else:
            w.state[1] = 0

    def on_chx3(state):
        if (QtCore.Qt.Checked == state):
            w.state[2] = 1
        else:
            w.state[2] = 0

    def on_chx4(state):
        if (QtCore.Qt.Checked == state):
            w.state[3] = 1
        else:
            w.state[3] = 0

    def on_chx5(state):
        if (QtCore.Qt.Checked == state):
            w.state[4] = 1
        else:
            w.state[4] = 0

    def on_chx6(state):
        if (QtCore.Qt.Checked == state):
            w.state[5] = 1
        else:
            w.state[5] = 0

    def on_chx7(state):
        if (QtCore.Qt.Checked == state):
            w.state[6] = 1
        else:
            w.state[6] = 0
            
    def on_chx8(state):
        if (QtCore.Qt.Checked == state):
            w.state[7] = 1
        else:
            w.state[7] = 0

    def on_chx9(state):
        if (QtCore.Qt.Checked == state):
            w.state[8] = 1
        else:
            w.state[8] = 0
            
    def on_chx10(state):
        if (QtCore.Qt.Checked == state):
            w.state[9] = 1
        else:
            w.state[9] = 0

    def on_chx11(state):
        if (QtCore.Qt.Checked == state):
            w.state[10] = 1
        else:
            w.state[10] = 0

    def on_chx12(state):
        if (QtCore.Qt.Checked == state):
            w.state[11]= 1
        else:
            w.state[11] = 0


if __name__ == '__main__':
    server = False
    app = QtWidgets.QApplication(sys.argv)
    w = MainWidget()
    y = Dialog()
    y.setWindowTitle("Servidor")
    signals.MainWidgetSignals(w)
    w.show()
    print(w.server)
    while not(w.server):
        if y.exec_() == QtGui.QDialog.Accepted:
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
        
