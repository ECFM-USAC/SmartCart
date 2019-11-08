from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QGroupBox, QAction, qApp
from PyQt5.QtGui import QIcon
import numpy as np
import sys
import time
import threading

import plot as pgraph
from mqtt_process import MqttClient

class MainWidget(QtWidgets.QMainWindow):
    count = 0
    ptr = 0

    ########################################   MAINWIDGET  #########################################################
    def __init__(self, parent=None):
        ######################################   Variables  ########################################################
        self.state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #Indica que se debe graficar en el eje vertical
        self.stateN = 0                                   #Indica los datos del eje horizontal
        self.graph = [0, 0, 0, 0, 0]                      #Contiene los parametros de los ejes de nuestra grafica
        self.server = False                               #Nos indica si hay conexion con el servidor

        self.graph[1] = 200                               #Zoom eje vertical
        self.graph[2] = 0                                 #Centro eje vertical

        self.graph[1] = 200                               #Zoom eje horizontal
        self.graph[2] = 0                                 #Centro eje horizontal
                 
        ############################   Configuracion ventana principal  ############################################
        super(MainWidget, self).__init__(parent)          #Inheritance
        self.setGeometry(100, 100, 800, 600)              #Tamaño ventana principal
        self.setWindowTitle("Interfaz")                   #Titulo
        self.setStyleSheet("background-color:white;")     #Color de fondo

        #################################   Creacion Layout  #######################################################

        self.main_widget = QtWidgets.QWidget()
        lay = QtWidgets.QGridLayout(self.main_widget)
        
        lay.setRowStretch(1, 1)
        lay.setRowStretch(2, 5)
        lay.setRowStretch(3, 2)
        lay.setRowStretch(4, 2)
        lay.setColumnStretch(0, 1)
        lay.setColumnStretch(1, 5)

        ##############################   Creacion Widget Grafica  ##################################################

        self.label1 = QtWidgets.QLabel("Grafica")                           #Etiqueta:"Grafica"
        self.label1.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))     #Fuente de la etiqueta
        lay.addWidget(self.label1, 0, 1, QtCore.Qt.AlignCenter)

        self.Plot = pgraph.RealTimePlot(self, width=5, height=4, dpi=100)   #Objeto grafica, derivado de la clase "RealTimePlot" en nuestro archivo "plot.py"
        lay.addWidget(self.Plot, 1, 1, 3, 1)                                #Se agrega el objeto a nuestra layout

        

        ##################################   Creacion ToolBar  #####################################################

        self.tb = QtWidgets.QToolBar()                                     #Objeto ToolBar
        self.myQMenuBar = QtWidgets.QMenuBar()                             #Objeto QMenuBar
        
        #Se agrega menu "Servidor" a QMenuBar
        self.fileMenu = self.myQMenuBar.addMenu("Servidor")               

        ##Se crea accion (submenu) "Desconectar" en menu "Servidor"
        desconectarAction = QAction("Desconectar", self)                   
        desconectarAction.setShortcut("Ctrl+d")
        self.fileMenu.addAction(desconectarAction)

        ##Se crea accion (submenu) "Conectar" en menu "Servidor"
        conectarAction = QAction("Conectar", self)                         
        conectarAction.setShortcut("Ctrl+o")
        self.fileMenu.addAction(conectarAction)
        self.fileMenu.triggered[QAction].connect(self.process_server)

        #Se agrega menu "Grafica" a QMenuBar
        self.fileMenu1 = self.myQMenuBar.addMenu(u"Gráfica")                
        self.fileMenu1.triggered[QAction].connect(self.process_graph)       

        ##Se crea accion (submenu) "Datos" en menu "Grafica"
        self.subMenu = QtWidgets.QMenu("Datos")
        ###Se crea sub-accion "Acelerometro" en accion (submenu) "Datos"
        self.selectAce = QAction("Acelerómetro", self)
        self.selectAce.setShortcut("Ctrl+c")
        self.subMenu.addAction(self.selectAce)
        ###Se crea sub-accion "Giroscopio" en accion (submenu) "Datos"
        self.selectGir = QAction("Giroscopio", self)
        self.selectGir.setShortcut("Ctrl+g")
        self.subMenu.addAction(self.selectGir)
        ###Se crea sub-accion "Angulos" en accion (submenu) "Datos"
        self.selectAng = QAction(u"Ángulos", self)
        self.selectAng.setShortcut("Ctrl+a")
        self.subMenu.addAction(self.selectAng)
        ###Se crea sub-accion "Velocidad" en accion (submenu) "Datos"
        self.selectVel = QAction("Velocidad", self)
        self.selectAng.setShortcut("Ctrl+v")
        self.subMenu.addAction(self.selectAng)
        ###Se crea sub-accion "Impacto" en accion (submenu) "Datos"
        self.selectImp = QAction("Impacto", self)
        self.selectImp.setShortcut("Ctrl+i")
        self.subMenu.addAction(self.selectImp)
        ###Se crea sub-accion "Todos" en accion (submenu) "Datos"
        self.selectAll = QAction(QIcon("check.png"),"Todos", self)
        self.selectAll.setShortcut("Ctrl+t")
        self.subMenu.addAction(self.selectAll)

        self.fileMenu1.addMenu(self.subMenu)                               #Se agrega submenu "Datos" a menu "Grafica"

        self.tb.addWidget(self.myQMenuBar)                                 #Se agrega QMenuBar a objeto ToolBar
        self.tb.setFloatable(False)                                        
        self.tb.setMovable(False)
        self.addToolBar(self.tb)                                           #Se agrega ToolBar a nuestro MainWidget

        #########################   Creacion GroupBox para seleccion de datos  #####################################

        #Objeto GroupBox y caracteristicas
        self.Box = QtWidgets.QGroupBox()
        self.Box.setMinimumHeight(400)
        self.Box.setMinimumWidth(300)

        #Etiquetas para datos eje horizontal y eje vertical
        self.labelX = QtWidgets.QLabel("Eje horizontal")
        self.labelX.setFont(QtGui.QFont("Times", 9, QtGui.QFont.Bold))
        self.labelY = QtWidgets.QLabel("Eje vertical")
        self.labelY.setFont(QtGui.QFont("Times", 9, QtGui.QFont.Bold))

        #Seleccion de datos del eje horizontal (Se usa RadioButton pues solo se puede seleccionar uno a la vez)
        ##Creacion RadioButtons
        self.rbT = QtWidgets.QRadioButton("Tiempo")
        self.rbM = QtWidgets.QRadioButton("Muestras")
        self.rbAx = QtWidgets.QRadioButton(u"Ángulo-x")
        self.rbAy = QtWidgets.QRadioButton(u"Ángulo-y")
        self.rbAz = QtWidgets.QRadioButton(u"Ángulo-z")
        self.rbAcx = QtWidgets.QRadioButton(u"Aceleración-x")
        self.rbAcy = QtWidgets.QRadioButton(u"Aceleración-y")
        self.rbAcz = QtWidgets.QRadioButton(u"Aceleración-z")
        self.rbGx = QtWidgets.QRadioButton("Giroscopio-x")
        self.rbGy = QtWidgets.QRadioButton("Giroscopio-y")
        self.rbGz = QtWidgets.QRadioButton("Giroscopio-z")
        self.rbM.setChecked(True)
        ##Conexion con proceso para handler RadioButton
        self.rbT.toggled.connect(self.on_rbT)
        self.rbM.toggled.connect(self.on_rbM)
        self.rbAx.toggled.connect(self.on_rbAx)
        self.rbAy.toggled.connect(self.on_rbAy)
        self.rbAz.toggled.connect(self.on_rbAz)
        self.rbAcx.toggled.connect(self.on_rbAcx)
        self.rbAcy.toggled.connect(self.on_rbAcy)
        self.rbAcz.toggled.connect(self.on_rbAcz)
        self.rbGx.toggled.connect(self.on_rbGx)
        self.rbGy.toggled.connect(self.on_rbGy)
        self.rbGz.toggled.connect(self.on_rbGz)

        #Seleccion de datos del eje vertical (Se usa CheckBox pues se pueden seleccionar varios)
        ##Creacion CheckBox
        self.chxAx = QtWidgets.QCheckBox(u"Ángulo-x")
        self.chxAy = QtWidgets.QCheckBox(u"Ángulo-y")
        self.chxAz = QtWidgets.QCheckBox(u"Ángulo-z")
        self.chxAcx = QtWidgets.QCheckBox(u"Aceleración-x")
        self.chxAcy = QtWidgets.QCheckBox(u"Aceleración-y")
        self.chxAcz = QtWidgets.QCheckBox(u"Aceleración-z")
        self.chxGx = QtWidgets.QCheckBox("Giroscopio-x")
        self.chxGy = QtWidgets.QCheckBox("Giroscopio-y")
        self.chxGz = QtWidgets.QCheckBox("Giroscopio-z")
        self.chxVs = QtWidgets.QCheckBox("vueltas")
        self.chxPs = QtWidgets.QCheckBox("pulsos")
        self.chxI = QtWidgets.QCheckBox("peso")
        ##Conexion con proceso handler CheckBox
        self.chxAx.stateChanged.connect(self.on_chx1)
        self.chxAy.stateChanged.connect(self.on_chx2)
        self.chxAz.stateChanged.connect(self.on_chx3)
        self.chxAcx.stateChanged.connect(self.on_chx4)
        self.chxAcy.stateChanged.connect(self.on_chx5)
        self.chxAcz.stateChanged.connect(self.on_chx6)
        self.chxGx.stateChanged.connect(self.on_chx7)
        self.chxGy.stateChanged.connect(self.on_chx8)
        self.chxGz.stateChanged.connect(self.on_chx9)
        self.chxVs.stateChanged.connect(self.on_chx10)
        self.chxPs.stateChanged.connect(self.on_chx11)
        self.chxI.stateChanged.connect(self.on_chx12)  

        #Se agregan objetos a layout de nuestra GroupBox
        self.vbox = QtWidgets.QGridLayout(self.Box)
        self.vbox.setAlignment(QtCore.Qt.AlignTop)
        self.vbox.addWidget(self.labelX,0,0)
        self.vbox.addWidget(self.rbT,1,0)
        self.vbox.addWidget(self.rbM,2,0)
        self.vbox.addWidget(self.labelY,3,0)
        self.vbox.addWidget(self.chxAx,4,0)
        self.vbox.addWidget(self.chxAy,5,0)
        self.vbox.addWidget(self.chxAz,6,0)
        self.vbox.addWidget(self.chxAcx,7,0)
        self.vbox.addWidget(self.chxAcy,8,0)
        self.vbox.addWidget(self.chxAcz,9,0)
        self.vbox.addWidget(self.chxGx,10,0)
        self.vbox.addWidget(self.chxGy,11,0)
        self.vbox.addWidget(self.chxGz,12,0)
        self.vbox.addWidget(self.chxI,15,0)
        self.Box.setLayout(self.vbox)

        #Se agrega GroupBox a layout de MainWidget
        lay.addWidget(self.Box, 2, 0)
       
        ######################   Creacion GroupBox para estado del servidor  ##############################
        #Creacion GroupBox
        self.Box1 = QtWidgets.QGroupBox()
        self.Box1.setMinimumWidth(350)

        #Creacion Etiquetas
        self.labelS = QtWidgets.QLabel("Server:")
        self.labelS.setFont(QtGui.QFont("Times", 14))
        self.labelS1 = QtWidgets.QLabel("- - - - -")
        self.labelS1.setFont(QtGui.QFont("Times", 14))
        self.labelE = QtWidgets.QLabel("Estado: ")
        self.labelE.setFont(QtGui.QFont("Times", 14))
        self.labelE1 = QtWidgets.QLabel("Desconectado")
        self.labelE1.setFont(QtGui.QFont("Times", 14))

        #Se agregan widgets a layout GroupBox
        self.vbox1 = QtWidgets.QGridLayout()
        self.vbox1.addWidget(self.labelS, 0, 0)
        self.vbox1.addWidget(self.labelS1, 0, 1)
        self.vbox1.addWidget(self.labelE, 1, 0)
        self.vbox1.addWidget(self.labelE1, 1, 1)
        self.Box1.setLayout(self.vbox1)

        #Se agrega GroupBox a layout MainWidget
        lay.addWidget(self.Box1,0,0,2,1)


        #########################   Creacion GroupBox parametros grafica  #################################
        #Creacion GroupBox
        self.Box2 = QtWidgets.QGroupBox()
        self.Box2.setMinimumWidth(300)

        #Layout GroupBox
        self.vbox2 = QtWidgets.QGridLayout()

        #Etiqueta y Slider para zoom eje vertical
        ##Creacion widgets
        self.zoomyLabel = QtWidgets.QLabel("Zoom y")
        self.zoomyLabel.setFont(QtGui.QFont("Times", 12))
        self.zoomySlider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.zoomySlider.valueChanged[int].connect(self.on_valueChangedy)
        self.zoomySlider.setMinimum(0)
        self.zoomySlider.setMaximum(300)
        self.zoomySlider.setSingleStep(0.25)
        ##Se agregan widgets a layout GroupBox
        self.vbox2.addWidget(self.zoomyLabel,0,0)
        self.vbox2.addWidget(self.zoomySlider, 0, 1)

        #Etiquetas y Slider para centrar eje vertical
        ##Creacion Widgets
        self.centeryLabel = QtWidgets.QLabel("Centrar y")
        self.centeryLabel.setFont(QtGui.QFont("Times", 12))
        self.centerySlider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.centerySlider.valueChanged[int].connect(self.on_valueChangedcy)
        self.centerySlider.setMinimum(-200)
        self.centerySlider.setMaximum(200)
        self.centerySlider.setSingleStep(0.25)
        self.centerySlider.setValue(0)
        ##Se agregan widgets a layout GroupBox
        self.vbox2.addWidget(self.centeryLabel,1,0)
        self.vbox2.addWidget(self.centerySlider, 1, 1)

        #Etiquetas y Slider para zoom eje horizontal
        ##Creacion Widgets
        self.zoomxLabel = QtWidgets.QLabel("Zoom x")
        self.zoomxLabel.setFont(QtGui.QFont("Times", 12))
        self.zoomxSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.zoomxSlider.valueChanged[int].connect(self.on_valueChangedx)
        self.zoomxSlider.setMinimum(0)
        self.zoomxSlider.setMaximum(300)
        self.zoomxSlider.setSingleStep(0.25)
        ##Se agregan widgets a layout GroupBox
        self.vbox2.addWidget(self.zoomxLabel,2,0)
        self.vbox2.addWidget(self.zoomxSlider, 2, 1)

        #Etiquetas y Slider para centrar eje horizontal
        ##Creacion Widgets
        self.centerxLabel = QtWidgets.QLabel("Centrar x")
        self.centerxLabel.setFont(QtGui.QFont("Times", 12))
        self.centerxSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.centerxSlider.valueChanged[int].connect(self.on_valueChangedcx)
        self.centerxSlider.setMinimum(-200)
        self.centerxSlider.setMaximum(200)
        self.centerxSlider.setSingleStep(0.25)
        self.centerxSlider.setValue(0)
        ##Se agregan widgets a layout GroupBox
        self.vbox2.addWidget(self.centerxLabel,3,0)
        self.vbox2.addWidget(self.centerxSlider, 3, 1)

        #Etiquetas y Slider para numero de muestras o tiempo
        ##Creacion Widgets
        self.muestrasLabel = QtWidgets.QLabel("Muestras")
        self.muestrasLabel.setFont(QtGui.QFont("Times", 12))
        self.muestrasLabel = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        #self.centerxSlider.valueChanged[int].connect(self.on_valueChangedcx)
        self.muestrasLabel.setMinimum(0)
        self.muestrasLabel.setMaximum(200)
        self.muestrasLabel.setSingleStep(5)
        self.muestrasLabel.setValue(20)

        #Texto Sliders
        self.textZx = QtWidgets.QLineEdit()
        self.textZy = QtWidgets.QLineEdit()
        self.textCx = QtWidgets.QLineEdit()
        self.textCy = QtWidgets.QLineEdit()
        self.textM = QtWidgets.QLineEdit()
        self.vbox2.addWidget(self.textZx,2,2)
        self.vbox2.addWidget(self.textZy,0,2)
        self.vbox2.addWidget(self.textCx,3,2)
        self.vbox2.addWidget(self.textCy,1,2)
        self.textZx.setFixedWidth(50)
        self.textCx.setFixedWidth(50)
        self.textZy.setFixedWidth(50)
        self.textCy.setFixedWidth(50)

        self.textZx.setText("300")
        self.textCx.setText("0")
        self.textZy.setText("300")
        self.textCy.setText("0")
        
        #Se agrega layout a GroupBox
        self.Box2.setLayout(self.vbox2)

        #Se agrega GroupBox a layout MainWidgets
        lay.addWidget(self.Box2, 3, 0)

        ###############################   Creacion GroupBox datos  ########################################
        #Creacion GroupBox
        self.Box4 = QtWidgets.QGroupBox()
        self.Box4.setMinimumWidth(300)

        #Creacion layout GroupBox
        self.vbox4 = QtWidgets.QGridLayout()

        #Etiquetas titulos
        self.labelE = QtWidgets.QLabel("")
        self.labelV = QtWidgets.QLabel("Valor Actual")
        self.labelVmed = QtWidgets.QLabel("Media")
        self.labelVmax = QtWidgets.QLabel("Valor máximo")
        self.labelVmin = QtWidgets.QLabel("Valor mínimo")
        self.labelV.setFont(QtGui.QFont("Times", 8,  QtGui.QFont.Bold))
        self.labelVmed.setFont(QtGui.QFont("Times", 8,  QtGui.QFont.Bold))
        self.labelVmax.setFont(QtGui.QFont("Times", 8,  QtGui.QFont.Bold))
        self.labelVmin.setFont(QtGui.QFont("Times", 8,  QtGui.QFont.Bold))

        #Se agrega layout a GroupBox
        self.Box4.setLayout(self.vbox4)

        #Se agrega GroupBox a MainWidget
        lay.addWidget(self.Box4, 4, 1)

        #Etiquetas datos
        ##Valores
        self.vAx = QtWidgets.QLabel()
        self.vAy = QtWidgets.QLabel()
        self.vAz = QtWidgets.QLabel()
        self.vGx = QtWidgets.QLabel()
        self.vGy = QtWidgets.QLabel()
        self.vGz = QtWidgets.QLabel()
        self.vAcx = QtWidgets.QLabel()
        self.vAcy = QtWidgets.QLabel()
        self.vAcz = QtWidgets.QLabel()
        self.vVel = QtWidgets.QLabel()
        self.vImp = QtWidgets.QLabel()
        self.medAx = QtWidgets.QLabel()
        self.medAy = QtWidgets.QLabel()
        self.medAz = QtWidgets.QLabel()
        self.medGx = QtWidgets.QLabel()
        self.medGy = QtWidgets.QLabel()
        self.medGz = QtWidgets.QLabel()
        self.medAcx = QtWidgets.QLabel()
        self.medAcy = QtWidgets.QLabel()
        self.medAcz = QtWidgets.QLabel()
        self.medVel = QtWidgets.QLabel()
        self.medImp = QtWidgets.QLabel()
        self.minAx = QtWidgets.QLabel()
        self.minAy = QtWidgets.QLabel()
        self.minAz = QtWidgets.QLabel()
        self.minGx = QtWidgets.QLabel()
        self.minGy = QtWidgets.QLabel()
        self.minGz = QtWidgets.QLabel()
        self.minAcx = QtWidgets.QLabel()
        self.minAcy = QtWidgets.QLabel()
        self.minAcz = QtWidgets.QLabel()
        self.minVel = QtWidgets.QLabel()
        self.minImp = QtWidgets.QLabel()
        self.maxAx = QtWidgets.QLabel()
        self.maxAy = QtWidgets.QLabel()
        self.maxAz = QtWidgets.QLabel()
        self.maxGx = QtWidgets.QLabel()
        self.maxGy = QtWidgets.QLabel()
        self.maxGz = QtWidgets.QLabel()
        self.maxAcx = QtWidgets.QLabel()
        self.maxAcy = QtWidgets.QLabel()
        self.maxAcz = QtWidgets.QLabel()
        self.maxVel = QtWidgets.QLabel()
        self.maxImp = QtWidgets.QLabel()
        ##Titulos
        ###Creacion objetos
        self.tAx = QtWidgets.QLabel(u"Ángulo-x")
        self.tAy = QtWidgets.QLabel(u"Ángulo-y")
        self.tAz = QtWidgets.QLabel(u"Ángulo-z")
        self.tGx = QtWidgets.QLabel("Giroscopio-x")
        self.tGy = QtWidgets.QLabel("Giroscopio-y")
        self.tGz = QtWidgets.QLabel("Giroscopio-z")
        self.tAcx = QtWidgets.QLabel(u"Aceleración-x")
        self.tAcy = QtWidgets.QLabel(u"Aceleración-y")
        self.tAcz = QtWidgets.QLabel(u"Aceleración-z")
        self.tVel = QtWidgets.QLabel("Velocidad")
        self.tImp = QtWidgets.QLabel("Impacto")
        ###Fuente de las letras
        self.tAx.setFont(QtGui.QFont("Times", 8,  QtGui.QFont.Bold))
        self.tAy.setFont(QtGui.QFont("Times", 8,  QtGui.QFont.Bold))
        self.tAz.setFont(QtGui.QFont("Times", 8,  QtGui.QFont.Bold))
        self.tGx.setFont(QtGui.QFont("Times", 8,  QtGui.QFont.Bold))
        self.tGy.setFont(QtGui.QFont("Times", 8,  QtGui.QFont.Bold))
        self.tGz.setFont(QtGui.QFont("Times", 8,  QtGui.QFont.Bold))
        self.tAcx.setFont(QtGui.QFont("Times", 8,  QtGui.QFont.Bold))
        self.tAcy.setFont(QtGui.QFont("Times", 8,  QtGui.QFont.Bold))
        self.tAcz.setFont(QtGui.QFont("Times", 8,  QtGui.QFont.Bold))
        self.tVel.setFont(QtGui.QFont("Times", 8,  QtGui.QFont.Bold))
        self.tImp.setFont(QtGui.QFont("Times", 8,  QtGui.QFont.Bold))

        #########################   Se agrega main_widget como central widget  ##################################

        self.setCentralWidget(self.main_widget)

        ################################   Creacion cliente MQTT  ###############################################
        
        self.client = MqttClient(self)                              #Se crea objeto cliente derivado de la clase "MqttClient" de "mqtt_process.py" 
        self.client.stateChanged.connect(self.on_stateChanged)      #Proceso handler de conexion al servidor
        self.client.messageSignal.connect(self.on_messageSignal)    #Proceso handler de mensajes
        self.Data = pgraph.DataPlot()                               #Se crea objeto "Data" derivado de clase "DataPlot" de "plot.py" para manejar los datos a graficar


    #######################################   ACCIONES  #########################################################

    ###################################   Checkbox handler  #####################################################
    def on_chx1(self, state):
        if (QtCore.Qt.Checked == state):
            self.state[0] = 1
        else:
            self.state[0] = 0

    def on_chx2(self, state):
        if (QtCore.Qt.Checked == state):
            self.state[1] = 1
        else:
            self.state[1] = 0

    def on_chx3(self, state):
        if (QtCore.Qt.Checked == state):
            self.state[2] = 1
        else:
            self.state[2] = 0

    def on_chx4(self, state):
        if (QtCore.Qt.Checked == state):
            self.state[3] = 1
        else:
            self.state[3] = 0

    def on_chx5(self, state):
        if (QtCore.Qt.Checked == state):
            self.state[4] = 1
        else:
            self.state[4] = 0

    def on_chx6(self, state):
        if (QtCore.Qt.Checked == state):
            self.state[5] = 1
        else:
            self.state[5] = 0

    def on_chx7(self, state):
        if (QtCore.Qt.Checked == state):
            self.state[6] = 1
        else:
            self.state[6] = 0
            
    def on_chx8(self, state):
        if (QtCore.Qt.Checked == state):
            self.state[7] = 1
        else:
            self.state[7] = 0

    def on_chx9(self, state):
        if (QtCore.Qt.Checked == state):
            self.state[8] = 1
        else:
            self.state[8] = 0
            
    def on_chx10(self, state):
        if (QtCore.Qt.Checked == state):
            self.state[9] = 1
        else:
            self.state[9] = 0

    def on_chx11(self, state):
        if (QtCore.Qt.Checked == state):
            self.state[10] = 1
        else:
            self.state[10] = 0

    def on_chx12(self, state):
        if (QtCore.Qt.Checked == state):
            self.state[11]= 1
        else:
            self.state[11] = 0
    
    #####################################   MQTT  ##############################################################
    #Cambio en el estado (activo/inactivo)
    @QtCore.pyqtSlot(int)
    def on_stateChanged(self, state):
        if state == MqttClient.Connected:
            print("Estado:",state)
            self.client.subscribe([("anx",0),("any",0),("anz",0),("gx",0),("gy",0),("gz",0),("acx",0),("acy",0),("acz",0),("pulsos",0),("vueltas",0),("peso",0),("tiempo",0)])
            self.labelS1.setText(self.client.hostname)
            self.labelE1.setText("Conectado")
            print(u"Se ha efectuado la conexión")

    #Mensajes a los topics subscritos
    @QtCore.pyqtSlot(list)
    def on_messageSignal(self, msg):
        val1 = float(msg[0])
        val2 = float(msg[1])
        val3 = float(msg[2])
        self.count += 1
        self.Data.add(self.count, msg)
        self.Plot.update_figure(self.Data, self.state, self.stateN, self.graph)
        self.actualizarV(self.Data.axis_y, self.Data.Vmed, self.Data.Vmax, self.Data.Vmin)

    ###################################   Menu Bar  ############################################################
    #Menu "Server"
    def process_server(self, q):
        print(q.text())
        if(q.text()=="Conectar"):
            y = Dialog()
            y.setWindowTitle("Servidor")

            if (self.server == True):
                z = DialogAnuncio()
                z.setWindowTitle("Aviso")
                if z.exec_() == QtGui.QDialog.Accepted:
                    self.server = False
                else:
                    self.server = True
                    print("Conectado a:",self.client.hostname)
                z.deleteLater()
                
            if (self.server == False):
                while not(self.server):
                    if y.exec_() == QtGui.QDialog.Accepted:
                        address = y.textBox1.text()
                        name = y.textBox2.text()
                        try:
                            self.client.hostname = address
                            self.client.connectToHost()
                            self.server = True
                        except:
                            self.server = False
                            print(u"Valores no válidos")
                        if address == "":
                            self.server = False
                            print(u"Valores no válidos")
                        else:
                            print(u'Dirección: %s' % address)
                            print('Usuario: %s' % name)
                    else:
                        self.server = False
                        print('Cancelled')
                        break
                    y.deleteLater()
                
        if(q.text()=="Desconectar"):
            self.client.disconnectFromHost()
            self.labelS1.setText("- - - -")
            self.labelE1.setText("Desconectado")
            self.server = False
            
    #Menu "Gráfica"
    def process_graph(self, q):
        #print(q.text())
        #Action "Impacto"
        if (q.text()=="Impacto"):
            #Se agrega el icono de seleccion a la action en el MenuBar
            self.selectImp.setIcon(QIcon("check.png"))
            self.selectAce.setIcon(QIcon(""))
            self.selectAng.setIcon(QIcon(""))
            self.selectGir.setIcon(QIcon(""))
            self.selectAll.setIcon(QIcon(""))

            #Se borran los widgets contenidos en el GroupBox de seleccion de datos
            while self.vbox.count() > 0:
                print(self.vbox.count())
                item = self.vbox.takeAt(0).widget()
                if not(item.text() == "Eje horizontal" or item.text() == "Eje vertical"):
                    item.setChecked(False)
                self.vbox.removeWidget(item)
                item.setParent(None)


            #Se borran los widgets contenidos en el GroupBox que muestra datos
            while self.vbox4.count() > 0:
                item = self.vbox4.takeAt(0).widget()
                self.vbox4.removeWidget(item)
                item.setParent(None)
            
        if (q.text()==u"Acelerómetro"):
            #Se agrega el icono de seleccion a la action en el MenuBar
            self.selectImp.setIcon(QIcon(""))
            self.selectAce.setIcon(QIcon("check.png"))
            self.selectAng.setIcon(QIcon(""))
            self.selectGir.setIcon(QIcon(""))
            self.selectAll.setIcon(QIcon(""))

            #Se borran los widgets contenidos en el GroupBox de seleccion de datos
            while self.vbox.count() > 0:
                print(self.vbox.count())
                item = self.vbox.takeAt(0).widget()
                if not(item.text() == "Eje horizontal" or item.text() == "Eje vertical"):
                    item.setChecked(False)
                self.vbox.removeWidget(item)
                item.setParent(None)

            #Se borran los widgets contenidos en el GroupBox que muestra datos
            while self.vbox4.count() > 0:
                item = self.vbox4.takeAt(0).widget()
                self.vbox4.removeWidget(item)
                item.setParent(None)
                

            #Se agregan items de seleccion de datos
            i = 0
            self.vbox.addWidget(self.labelX,i,0)
            i+=1
            self.vbox.addWidget(self.rbT,i,0)
            i+=1
            self.vbox.addWidget(self.rbM,i,0)
            i+=1
            self.vbox.addWidget(self.rbAcx,i,0)
            i+=1
            self.vbox.addWidget(self.rbAcy,i,0)
            i+=1
            self.vbox.addWidget(self.rbAcz,i,0)
            i+=1
            self.vbox.addWidget(self.labelY,i,0)
            i+=1
            self.vbox.addWidget(self.chxAcx,i,0)
            i+=1
            self.vbox.addWidget(self.chxAcy,i,0)
            i+=1
            self.vbox.addWidget(self.chxAcz,i,0)
            
            self.rbM.setChecked(True)

            #Se agregan items de muestra de datos
            self.vbox4.addWidget(self.labelE, 0, 0)
            self.vbox4.addWidget(self.labelV, 1, 0)
            self.vbox4.addWidget(self.labelVmed, 2, 0)
            self.vbox4.addWidget(self.labelVmax, 3, 0)
            self.vbox4.addWidget(self.labelVmin, 4, 0)

            self.vbox4.addWidget(self.tAcx, 0, 1)
            self.vbox4.addWidget(self.tAcy, 0, 2)
            self.vbox4.addWidget(self.tAcz, 0, 3)

            self.vbox4.addWidget(self.vAcx, 1, 1)
            self.vbox4.addWidget(self.vAcy, 1, 2)
            self.vbox4.addWidget(self.vAcz, 1, 3)
            self.vbox4.addWidget(self.medAcx, 2, 1)
            self.vbox4.addWidget(self.medAcy, 2, 2)
            self.vbox4.addWidget(self.medAcz, 2, 3)
            self.vbox4.addWidget(self.maxAcx, 3, 1)
            self.vbox4.addWidget(self.maxAcy, 3, 2)
            self.vbox4.addWidget(self.maxAcz, 3, 3)
            self.vbox4.addWidget(self.minAcx, 4, 1)
            self.vbox4.addWidget(self.minAcy, 4, 2)
            self.vbox4.addWidget(self.minAcz, 4, 3)

            #Se colocan layouts en los GroupBox correspondientes
            self.Box.setLayout(self.vbox)
            self.Box4.setLayout(self.vbox4)
            
        if (q.text()=="Giroscopio"):
            #Se agrega el icono de seleccion a la action en el MenuBar
            self.selectImp.setIcon(QIcon(""))
            self.selectAce.setIcon(QIcon(""))
            self.selectAng.setIcon(QIcon(""))
            self.selectGir.setIcon(QIcon("check.png"))
            self.selectAll.setIcon(QIcon(""))

            #Se borran los widgets contenidos en el GroupBox de seleccion de datos
            while self.vbox.count() > 0:
                print(self.vbox.count())
                item = self.vbox.takeAt(0).widget()
                if not(item.text() == "Eje horizontal" or item.text() == "Eje vertical"):
                    item.setChecked(False)
                self.vbox.removeWidget(item)
                item.setParent(None)

            #Se borran los widgets contenidos en el GroupBox que muestra los datos
            while self.vbox4.count() > 0:
                item = self.vbox4.takeAt(0).widget()
                self.vbox4.removeWidget(item)
                item.setParent(None)

            #Se agregan los widgets de seleccion de datos
            i = 0
            self.vbox.addWidget(self.labelX,i,0)
            i+=1
            self.vbox.addWidget(self.rbT,i,0)
            i+=1
            self.vbox.addWidget(self.rbM,i,0)
            i+=1
            self.vbox.addWidget(self.rbGx,i,0)
            i+=1
            self.vbox.addWidget(self.rbGy,i,0)
            i+=1
            self.vbox.addWidget(self.rbGz,i,0)
            i+=1
            self.vbox.addWidget(self.labelY,i,0)
            i+=1
            self.vbox.addWidget(self.chxGx,i,0)
            i+=1
            self.vbox.addWidget(self.chxGy,i,0)
            i+=1
            self.vbox.addWidget(self.chxGz,i,0)
            
            self.rbM.setChecked(True)

            #Se agregan los widgets de muestra de datos
            self.vbox4.addWidget(self.labelE, 0, 0)
            self.vbox4.addWidget(self.labelV, 1, 0)
            self.vbox4.addWidget(self.labelVmed, 2, 0)
            self.vbox4.addWidget(self.labelVmax, 3, 0)
            self.vbox4.addWidget(self.labelVmin, 4, 0)

            self.vbox4.addWidget(self.tGx, 0, 1)
            self.vbox4.addWidget(self.tGy, 0, 2)
            self.vbox4.addWidget(self.tGz, 0, 3)

            self.vbox4.addWidget(self.vGx, 1, 1)
            self.vbox4.addWidget(self.vGy, 1, 2)
            self.vbox4.addWidget(self.vGz, 1, 3)
            self.vbox4.addWidget(self.medGx, 2, 1)
            self.vbox4.addWidget(self.medGy, 2, 2)
            self.vbox4.addWidget(self.medGz, 2, 3)
            self.vbox4.addWidget(self.maxGx, 3, 1)
            self.vbox4.addWidget(self.maxGy, 3, 2)
            self.vbox4.addWidget(self.maxGz, 3, 3)
            self.vbox4.addWidget(self.minGx, 4, 1)
            self.vbox4.addWidget(self.minGy, 4, 2)
            self.vbox4.addWidget(self.minGz, 4, 3)

            #Se colocan layouts en los GroupBox correspondientes
            self.Box.setLayout(self.vbox)
            self.Box4.setLayout(self.vbox4)
            
        if (q.text()==u"Ángulos"):
            #Se agrega el icono de seleccion a la action en el MenuBar
            self.selectImp.setIcon(QIcon(""))
            self.selectAce.setIcon(QIcon(""))
            self.selectAng.setIcon(QIcon("check.png"))
            self.selectGir.setIcon(QIcon(""))
            self.selectAll.setIcon(QIcon(""))

            #Se borran los widgets contenidos en el GroupBox de seleccion de datos
            while self.vbox.count() > 0:
                print(self.vbox.count())
                item = self.vbox.takeAt(0).widget()
                if not(item.text() == "Eje horizontal" or item.text() == "Eje vertical"):
                    item.setChecked(False)
                self.vbox.removeWidget(item)
                item.setParent(None)

            #Se borran los widgets contenidos en el GroupBox que muestra los datos
            while self.vbox4.count() > 0:
                item = self.vbox4.takeAt(0).widget()
                self.vbox4.removeWidget(item)
                item.setParent(None)

            #Se agregan widgets de selección de datos
            i = 0
            self.vbox.addWidget(self.labelX,i,0)
            i+=1
            self.vbox.addWidget(self.rbT,i,0)
            i+=1
            self.vbox.addWidget(self.rbM,i,0)
            i+=1
            self.vbox.addWidget(self.rbAx,i,0)
            i+=1
            self.vbox.addWidget(self.rbAy,i,0)
            i+=1
            self.vbox.addWidget(self.rbAz,i,0)
            i+=1
            self.vbox.addWidget(self.labelY,i,0)
            i+=1
            self.vbox.addWidget(self.chxAx,i,0)
            i+=1
            self.vbox.addWidget(self.chxAy,i,0)
            i+=1
            self.vbox.addWidget(self.chxAz,i,0)
            
            self.rbM.setChecked(True)

            #Se agregan widgets de meustra de datos
            self.vbox4.addWidget(self.labelE, 0, 0)
            self.vbox4.addWidget(self.labelV, 1, 0)
            self.vbox4.addWidget(self.labelVmed, 2, 0)
            self.vbox4.addWidget(self.labelVmax, 3, 0)
            self.vbox4.addWidget(self.labelVmin, 4, 0)

            self.vbox4.addWidget(self.tAx, 0, 1)
            self.vbox4.addWidget(self.tAy, 0, 2)
            self.vbox4.addWidget(self.tAz, 0, 3)

            self.vbox4.addWidget(self.vAx, 1, 1)
            self.vbox4.addWidget(self.vAy, 1, 2)
            self.vbox4.addWidget(self.vAz, 1, 3)
            self.vbox4.addWidget(self.medAx, 2, 1)
            self.vbox4.addWidget(self.medAy, 2, 2)
            self.vbox4.addWidget(self.medAz, 2, 3)
            self.vbox4.addWidget(self.maxAx, 3, 1)
            self.vbox4.addWidget(self.maxAy, 3, 2)
            self.vbox4.addWidget(self.maxAz, 3, 3)
            self.vbox4.addWidget(self.minAx, 4, 1)
            self.vbox4.addWidget(self.minAy, 4, 2)
            self.vbox4.addWidget(self.minAz, 4, 3)
            
            #Se agregan layouts a GroupBox
            self.Box.setLayout(self.vbox)
            self.Box4.setLayout(self.vbox4)
            
        if (q.text()=="Todos"):
            #Se agrega el icono de seleccion a la action en el MenuBar
            self.selectImp.setIcon(QIcon(""))
            self.selectAce.setIcon(QIcon(""))
            self.selectAng.setIcon(QIcon(""))
            self.selectGir.setIcon(QIcon(""))
            self.selectAll.setIcon(QIcon("check.png"))

            #Se borran los widgets contenidos en el GroupBox de seleccion de datos
            while self.vbox.count() > 0:
                print(self.vbox.count())
                item = self.vbox.takeAt(0).widget()
                if not(item.text() == "Eje horizontal" or item.text() == "Eje vertical"):
                    item.setChecked(False)
                self.vbox.removeWidget(item)
                item.setParent(None)

            #Se borran los widgets contenidos en el GroupBox que muestra datos
            while self.vbox4.count() > 0:
                item = self.vbox4.takeAt(0).widget()
                self.vbox4.removeWidget(item)
                item.setParent(None)

            #Se agregan widgets de selección de datos
            i=0
            self.vbox.addWidget(self.labelX,i,0)
            i+=1
            self.vbox.addWidget(self.rbT,i,0)
            i+=1
            self.vbox.addWidget(self.rbM,i,0)
            i+=1
            self.vbox.addWidget(self.labelY,i,0)
            i+=1
            self.vbox.addWidget(self.chxAx,i,0)
            i+=1
            self.vbox.addWidget(self.chxAy,i,0)
            i+=1
            self.vbox.addWidget(self.chxAz,i,0)
            i+=1
            self.vbox.addWidget(self.chxAcx,i,0)
            i+=1
            self.vbox.addWidget(self.chxAcy,i,0)
            i+=1
            self.vbox.addWidget(self.chxAcz,i,0)
            i+=1
            self.vbox.addWidget(self.chxGx,i,0)
            i+=1
            self.vbox.addWidget(self.chxGy,i,0)
            i+=1
            self.vbox.addWidget(self.chxGz,i,0)
            i+=1
            self.vbox.addWidget(self.chxI,i,0)
            
            self.rbM.setChecked(True)

            #Se agrega layout a GroupBox
            self.Box.setLayout(self.vbox)

    ###################################   Datos mostrados  #####################################################
            
    def actualizarV(self, ValAct, ValMed, ValMax, ValMin):
        self.vAx.setText(str(ValAct[0]))
        self.vAy.setText(str(ValAct[1]))
        self.vAz.setText(str(ValAct[2]))
        self.vGx.setText(str(ValAct[3]))
        self.vGy.setText(str(ValAct[4]))
        self.vGz.setText(str(ValAct[5]))
        self.vAcx.setText(str(ValAct[6]))
        self.vAcy.setText(str(ValAct[7]))
        self.vAcz.setText(str(ValAct[8]))
        self.medAx.setText(str(round(ValMed[0],4)))
        self.medAy.setText(str(round(ValMed[1],4)))
        self.medAz.setText(str(round(ValMed[2],4)))
        self.medGx.setText(str(round(ValMed[3],4)))
        self.medGy.setText(str(round(ValMed[4],4)))
        self.medGz.setText(str(round(ValMed[5],4)))
        self.medAcx.setText(str(round(ValMed[6],4)))
        self.medAcy.setText(str(round(ValMed[7],4)))
        self.medAcz.setText(str(round(ValMed[8],4)))
        self.maxAx.setText(str(ValMax[0]))
        self.maxAy.setText(str(ValMax[1]))
        self.maxAz.setText(str(ValMax[2]))
        self.maxGx.setText(str(ValMax[3]))
        self.maxGy.setText(str(ValMax[4]))
        self.maxGz.setText(str(ValMax[5]))
        self.maxAcx.setText(str(ValMax[6]))
        self.maxAcy.setText(str(ValMax[7]))
        self.maxAcz.setText(str(ValMax[8]))
        self.minAx.setText(str(ValMin[0]))
        self.minAy.setText(str(ValMin[1]))
        self.minAz.setText(str(ValMin[2]))
        self.minGx.setText(str(ValMin[3]))
        self.minGy.setText(str(ValMin[4]))
        self.minGz.setText(str(ValMin[5]))
        self.minAcx.setText(str(ValMin[6]))
        self.minAcy.setText(str(ValMin[7]))
        self.minAcz.setText(str(ValMin[8]))


    ###########################   WIDGETS SELECCIÓN DE DATOS  ############################################
    #Radio Button datos de tiempo (eje horizontal)
    @QtCore.pyqtSlot()
    def on_rbT(self):
        if self.rbT.isChecked():
            print("Tiempo seleccionado", self.stateN)
            self.stateN = 4
            self.graph[0] = 0

    #Radio Button muestras (eje horizontal)    
    @QtCore.pyqtSlot()
    def on_rbM(self):
        if self.rbM.isChecked():
            print("Muestras seleccionadas", self.stateN)
            self.stateN = 0
            self.graph[0] = 0

    #Radio Button Ángulo x (eje horizontal)    
    @QtCore.pyqtSlot()
    def on_rbAx(self):
        if self.rbAx.isChecked():
            print("Ax seleccionado", self.stateN)
            self.stateN = 1
            self.graph[0] = 1

    #Radio Button Ángulo y (eje horizontal)    
    @QtCore.pyqtSlot()    
    def on_rbAy(self):
        if self.rbAy.isChecked():
            print("Ay seleccionadas", self.stateN)
            self.stateN = 2
            self.graph[0] = 1

    #Radio Button Ángulo z (eje horizontal)    
    @QtCore.pyqtSlot()
    def on_rbAz(self):
        if self.rbAz.isChecked():
            print("Az seleccionado", self.stateN)
            self.stateN = 3
            self.graph[0] = 1

    #Radio Button Aceleración x (eje horizontal)    
    @QtCore.pyqtSlot()    
    def on_rbAcx(self):
        if self.rbAcx.isChecked():
            print("Acx seleccionadas", self.stateN)
            self.stateN = 1
            self.graph[0] = 1

    #Radio Button Aceleración y (eje horizontal)    
    @QtCore.pyqtSlot()
    def on_rbAcy(self):
        if self.rbAcy.isChecked():
            print("Acy seleccionado", self.stateN)
            self.stateN = 2
            self.graph[0] = 1

    #Radio Button Aceleración z (eje horizontal)    
    @QtCore.pyqtSlot()    
    def on_rbAcz(self):
        if self.rbAcz.isChecked():
            print("Acz seleccionadas", self.stateN)
            self.stateN = 3
            self.graph[0] = 1

    #Radio Button Grisocopio x (eje horizontal)    
    @QtCore.pyqtSlot()
    def on_rbGx(self):
        if self.rbGx.isChecked():
            print("Gx seleccionado", self.stateN)
            self.stateN = 1
            self.graph[0] = 1

    #Radio Button Giroscopio y (eje horizontal)    
    @QtCore.pyqtSlot()    
    def on_rbGy(self):
        if self.rbGy.isChecked():
            print("Gy seleccionadas", self.stateN)
            self.stateN = 2
            self.graph[0] = 1

    #Radio Button Giroscopio z (eje horizontal)    
    @QtCore.pyqtSlot()    
    def on_rbGz(self):
        if self.rbGz.isChecked():
            print("Gz seleccionadas", self.stateN)
            self.stateN = 3
            self.graph[0] = 1

    ##########################   WIDGETS MANIPULACIÓN GRÁFICA  ###########################################
    #Zoom para el eje vertical
    @QtCore.pyqtSlot()    
    def on_valueChangedy(self):
        value = 300-int(self.zoomySlider.value())+0.1
        self.textZy.setText(str(value-0.1))
        center = int(self.centerySlider.value())
        print(value)
        self.graph[1] = value
        self.graph[2] = center
        
    #Valor de centrado eje vertical
    @QtCore.pyqtSlot()    
    def on_valueChangedcy(self):
        value = 300-int(self.zoomySlider.value())+0.1
        center = int(self.centerySlider.value())
        self.textCy.setText(str(center))
        print("centrado y ",center)
        self.graph[1] = value
        self.graph[2] = center

    #Zoom para el eje horizontal        
    @QtCore.pyqtSlot()    
    def on_valueChangedx(self):
        print(self.zoomxSlider.value())
        value = 300-int(self.zoomxSlider.value())
        self.textZx.setText(str(value-0.1))
        center = int(self.centerxSlider.value())
        self.graph[3] = value
        self.graph[4] = center

    #Valor de centrado eje horizontal
    @QtCore.pyqtSlot()    
    def on_valueChangedcx(self):
        value = 300-int(self.zoomxSlider.value())+0.1
        center = int(self.centerxSlider.value())
        self.textCx.setText(str(center))
        print("centrado x ",center)
        self.graph[3] = value
        self.graph[4] = center

################################   WIDGET INICIAL (SERVER)  ##################################################
class Dialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.label1 = QtWidgets.QLabel(u"Dirección")
        self.label2 = QtWidgets.QLabel("Usuario")
        self.textBox1 = QtWidgets.QLineEdit('192.168.126.180', self)
        self.textBox2 = QtWidgets.QLineEdit('Usuario', self)
        self.buttonOk = QtWidgets.QPushButton('Ok', self)
        self.buttonOk.clicked.connect(self.accept)
        self.buttonCancel = QtWidgets.QPushButton('Cancel', self)
        self.buttonCancel.clicked.connect(self.reject)
        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.label1, 0, 0, 1, 2)
        layout.addWidget(self.label2, 1, 0, 1, 2)
        layout.addWidget(self.textBox1, 0, 1, 1, 2)
        layout.addWidget(self.textBox2, 1, 1, 1, 2)
        layout.addWidget(self.buttonOk, 2, 0)
        layout.addWidget(self.buttonCancel, 2, 1)

################################   WIDGET ANUNCIO (SERVER)  ##################################################
class DialogAnuncio(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.label = QtWidgets.QLabel(u"Actualmente hay un servidor activo ¿Desea cambiarlo?")
        self.buttonOk = QtWidgets.QPushButton('Ok', self)
        self.buttonOk.clicked.connect(self.accept)
        self.buttonCancel = QtWidgets.QPushButton('Cancel', self)
        self.buttonCancel.clicked.connect(self.reject)
        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.label, 0, 0, 1, 2, QtCore.Qt.AlignCenter)
        layout.addWidget(self.buttonOk, 1, 0)
        layout.addWidget(self.buttonCancel, 1, 1)

