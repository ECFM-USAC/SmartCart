import paho.mqtt.client as mqtt
from PyQt5 import QtCore
import sys
import time

class MqttClient(QtCore.QObject):
    #################################################################
    # Variables y señales
    Disconnected = 0
    Connecting = 1
    Connected = 2

    MQTT_3_1 = mqtt.MQTTv31
    MQTT_3_1_1 = mqtt.MQTTv311

    connected = QtCore.pyqtSignal()
    disconnected = QtCore.pyqtSignal()

    stateChanged = QtCore.pyqtSignal(int)
    hostnameChanged = QtCore.pyqtSignal(str)
    portChanged = QtCore.pyqtSignal(int)
    keepAliveChanged = QtCore.pyqtSignal(int)
    cleanSessionChanged = QtCore.pyqtSignal(bool)
    protocolVersionChanged = QtCore.pyqtSignal(int)

    messageSignal = QtCore.pyqtSignal(list)


    #################################################################
    # Inicio
    def __init__(self, parent=None):
        super(MqttClient, self).__init__(parent)

        self.m_hostname = ""
        self.m_port = 1883
        self.m_keepAlive = 60
        self.m_cleanSession = True
        self.m_protocolVersion = MqttClient.MQTT_3_1

        self.mensaje = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.count = 0

        self.m_state = MqttClient.Disconnected

        self.m_client = mqtt.Client(clean_session=self.m_cleanSession,
                                    protocol=self.protocolVersion)

        self.m_client.on_connect = self.on_connect
        self.m_client.on_message = self.on_message
        self.m_client.on_disconnect = self.on_disconnect

    @QtCore.pyqtProperty(int, notify=stateChanged)
    def state(self):
        return self.m_state

    @state.setter
    def state(self, state):
        if self.m_state == state: return
        self.m_state = state
        self.stateChanged.emit(state)

    @QtCore.pyqtProperty(str, notify=hostnameChanged)
    def hostname(self):
        return self.m_hostname

    @hostname.setter
    def hostname(self, hostname):
        if self.m_hostname == hostname: return
        self.m_hostname = hostname
        self.hostnameChanged.emit(hostname)

    @QtCore.pyqtProperty(int, notify=portChanged)
    def port(self):
        return self.m_port

    @port.setter
    def port(self, port):
        if self.m_port == port: return
        self.m_port = port
        self.portChanged.emit(port)

    @QtCore.pyqtProperty(int, notify=keepAliveChanged)
    def keepAlive(self):
        return self.m_keepAlive

    @keepAlive.setter
    def keepAlive(self, keepAlive):
        if self.m_keepAlive == keepAlive: return
        self.m_keepAlive = keepAlive
        self.keepAliveChanged.emit(keepAlive)

    @QtCore.pyqtProperty(bool, notify=cleanSessionChanged)
    def cleanSession(self):
        return self.m_cleanSession

    @cleanSession.setter
    def cleanSession(self, cleanSession):
        if self.m_cleanSession == cleanSession: return
        self.m_cleanSession = cleanSession
        self.cleanSessionChanged.emit(cleanSession)

    @QtCore.pyqtProperty(int, notify=protocolVersionChanged)
    def protocolVersion(self):
        return self.m_protocolVersion

    @protocolVersion.setter
    def protocolVersion(self, protocolVersion):
        if self.m_protocolVersion == protocolVersion: return
        if protocolVersion in (MqttClient.MQTT_3_1, MQTT_3_1_1):
            self.m_protocolVersion = protocolVersion
            self.protocolVersionChanged.emit(protocolVersion)

    #################################################################
    # Acciones
    @QtCore.pyqtSlot()
    def connectToHost(self):
        if self.m_hostname:
            self.m_client.connect(self.m_hostname,
                                  port=self.port,
                                  keepalive=self.keepAlive)

            self.state = MqttClient.Connecting
            self.m_client.loop_start()

    @QtCore.pyqtSlot()
    def disconnectFromHost(self):
        self.m_client.disconnect()

    def subscribe(self, path):
        if self.state == MqttClient.Connected:
            self.m_client.subscribe(path)

    #################################################################
    # callbacks
    def on_message(self, mqttc, obj, msg):
        mstr = msg.payload.decode("ascii")
        if (str(msg.topic) == "anx"):
             self.mensaje[0] = float(mstr)
             self.count+=1
        if (str(msg.topic) == "any"):
             self.mensaje[1] = float(mstr)
             self.count+=1
        if (str(msg.topic) == "anz"):
             self.mensaje[2] = float(mstr)
             self.count+=1
        if (str(msg.topic) == "acx"):
             self.mensaje[3] = float(mstr)
             self.count+=1
        if (str(msg.topic) == "acy"):
             self.mensaje[4] = float(mstr)
             self.count+=1
        if (str(msg.topic) == "acz"):
             self.mensaje[5] = float(mstr)
             self.count+=1
        if (str(msg.topic) == "gx"):
             self.mensaje[6] = float(mstr)
             self.count+=1
        if (str(msg.topic) == "gy"):
             self.mensaje[7] = float(mstr)
             self.count+=1
        if (str(msg.topic) == "gz"):
             self.mensaje[8] = float(mstr)
             self.count+=1
        if (str(msg.topic) == "vueltas"):
             self.mensaje[9] = float(mstr)
             self.count+=1
        if (str(msg.topic) == "pulsos"):
             self.mensaje[10] = float(mstr)
             self.count+=1
        if (str(msg.topic) == "peso"):
             self.mensaje[11] = float(mstr)
             self.count+=1
        if (str(msg.topic) == "tiempo"):
             self.mensaje[12] = float(mstr)
             self.count+=1
             
        if self.count == 13:
            self.count = 0
            self.messageSignal.emit(self.mensaje)

    def on_connect(self, *args):
        self.state = MqttClient.Connected
        print("conectado")
        self.connected.emit()

    def on_disconnect(self, *args):
        self.state = MqttClient.Disconnected
        self.disconnected.emit()
