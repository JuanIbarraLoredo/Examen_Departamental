import sys
from PyQt5 import QtWidgets, uic, QtCore
import serial

class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Examen_Departamental.ui", self)  # Carga el archivo .ui

        self.txt_com.setText("COM3")
        self.arduino = None
        self.datos = []
        self.bandera = 0
        self.umbral = 500
        self.lbl_umbral.setText(f"Umbral Actual: {self.umbral}")

        # Buscar txt_umbral si existe en el .ui (por si lo agregas después)
        self.txt_umbral = self.findChild(QtWidgets.QLineEdit, "txt_umbral")

        self.segundoPlano = QtCore.QTimer()
        self.segundoPlano.timeout.connect(self.lecturas)

        self.btn_accion.clicked.connect(self.accion)
        self.btn_control.clicked.connect(self.control)

        self.dial_umbral.valueChanged.connect(self.cambiar_umbral_desde_dial)

        # NO conectamos btn_cambiar_umbral porque no existe en tu .ui

    def accion(self):
        texto = self.btn_accion.text()
        com = self.txt_com.text()

        try:
            if texto == "CONECTAR":
                self.arduino = serial.Serial(com, baudrate=9600, timeout=1)
                QtCore.QThread.msleep(1500)  # Dar tiempo a Arduino para reiniciar
                self.segundoPlano.start(100)
                self.btn_accion.setText("DESCONECTAR")
                self.txt_estado.setText("CONECTADO")
            elif texto == "DESCONECTAR":
                if self.arduino and self.arduino.isOpen():
                    self.segundoPlano.stop()
                    self.arduino.close()
                self.btn_accion.setText("RECONECTAR")
                self.txt_estado.setText("DESCONECTADO")
            elif texto == "RECONECTAR":
                if self.arduino and not self.arduino.isOpen():
                    self.arduino.open()
                    self.segundoPlano.start(100)
                    self.btn_accion.setText("DESCONECTAR")
                    self.txt_estado.setText("RECONECTADO")
        except Exception as e:
            print(f"Error en la conexión: {e}")

    def control(self):
        texto = self.btn_control.text()
        if self.arduino and self.arduino.isOpen():
            if texto == "PRENDER":
                self.btn_control.setText("APAGAR")
                self.arduino.write("1".encode())
            else:
                self.btn_control.setText("PRENDER")
                self.arduino.write("0".encode())

    def lecturas(self):
        if self.arduino and self.arduino.isOpen():
            if self.arduino.inWaiting():
                cadena = self.arduino.readline().decode().strip()
                if cadena:
                    self.datos.append(cadena)
                    if self.bandera == 0:
                        cadena_split = cadena.split("-")
                        if len(cadena_split) >= 3:
                            try:
                                valores_int = [int(v) for v in cadena_split[:-1]]
                            except Exception as e:
                                print(f"Error al convertir valores: {e}")

    def cambiar_umbral_desde_dial(self):
        self.umbral = self.dial_umbral.value()
        self.lbl_umbral.setText(f"Umbral Actual: {self.umbral}")
        if self.arduino and self.arduino.isOpen():
            comando = f"UMBRAL:{self.umbral}\n"
            self.arduino.write(comando.encode())
            self.arduino.flush()
            QtCore.QThread.msleep(100)
            print(f"Umbral enviado desde dial: {self.umbral}")

    def cambiar_umbral(self):
        if not self.txt_umbral:
            print("No se encontró el campo 'txt_umbral' en el .ui.")
            return

        try:
            nuevo_umbral = int(self.txt_umbral.text())
            self.umbral = nuevo_umbral
            self.lbl_umbral.setText(f"Umbral Actual: {self.umbral}")
            if self.arduino and self.arduino.isOpen():
                comando = f"UMBRAL:{self.umbral}\n"
                self.arduino.write(comando.encode())
                self.arduino.flush()
                QtCore.QThread.msleep(100)
            print(f"Umbral cambiado a: {self.umbral}")
        except ValueError:
            print("Por favor ingresa un número válido para el umbral.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = MyApp()
    ventana.show()
    sys.exit(app.exec_())
