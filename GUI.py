import serial
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer

# Puerto serial del Arduino
PORT = 'COM8'

class SensorReader(QWidget):
    def __init__(self):
        super().__init__()

        # Inicializar la conexión serial con el Arduino
        try:
            self.ser = serial.Serial(PORT, 9600)
        except serial.SerialException:
            print("Error: no se pudo conectar al Arduino")
            sys.exit()

        # Definir los widgets de la interfaz gráfica
        self.label_1 = QLabel("Valor del sensor 1:")
        self.label_2 = QLabel("Valor del sensor 2:")
        self.label_3 = QLabel("Valor del sensor 3:")
        self.label_4 = QLabel("Valor del sensor 4:")
        self.label_5 = QLabel("Valor del sensor 5:")

        self.button = QPushButton("Leer valores")
        self.button.clicked.connect(self.read_sensors)

        # Crear un temporizador para actualizar los valores cada cierto tiempo
        self.timer = QTimer()
        self.timer.setInterval(2000)  # 2 segundos
        self.timer.timeout.connect(self.read_sensors)

        # Crear un layout vertical para la ventana y agregar los widgets
        layout = QVBoxLayout()
        layout.addWidget(self.label_1)
        layout.addWidget(self.label_2)
        layout.addWidget(self.label_3)
        layout.addWidget(self.label_4)
        layout.addWidget(self.label_5)
        layout.addWidget(self.button)

        # Establecer el layout para la ventana
        self.setLayout(layout)

    def read_sensors(self):
        # Leer los valores de los sensores desde el puerto serial
        try:
            line = self.ser.readline().decode().strip()
            values = line.split(",")
            if len(values) == 5:
                sensor1, sensor2, sensor3, sensor4, sensor5 = values
                self.label_1.setText("Valor del sensor 1: {}".format(sensor1))
                self.label_2.setText("Valor del sensor 2: {}".format(sensor2))
                self.label_3.setText("Valor del sensor 3: {}".format(sensor3))
                self.label_4.setText("Valor del sensor 4: {}".format(sensor4))
                self.label_5.setText("Valor del sensor 5: {}".format(sensor5))

                ###################################################
            import csv
            # Abrir un archivo CSV para escritura
            with open('dataset/datos.csv', mode='a', newline='') as archivo_csv:
                # Crear un objeto writer para escribir en el archivo CSV
                writer = csv.writer(archivo_csv)

                # Escribir datos en el archivo CSV
                #writer.writerow(['Sensor 1', 'Sensor 2', 'Sensor 3', 'Sensor 4', 'Sensor 5'])
                writer.writerow([sensor1,sensor2,sensor3,sensor4,sensor4])

        except serial.SerialException:
            print("Error: no se pudo leer los valores de los sensores")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SensorReader()
    window.show()
    sys.exit(app.exec_())

###############################################################################
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QVBoxLayout
from PyQt5.QtGui import QPixmap

class ImageSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Image Selector')

        # Create the label that will show the image
        self.image_label = QLabel(self)
        self.image_label.setGeometry(10, 10, 280, 140)
        self.image_label.setPixmap(QPixmap('default.png'))

        # Create the list box with the image options
        self.image_list = QComboBox(self)
        self.image_list.addItem('Default', 'default.png')
        self.image_list.addItem('Image 1', 'image1.png')
        self.image_list.addItem('Image 2', 'image2.png')
        self.image_list.setGeometry(10, 160, 280, 30)
        self.image_list.activated[str].connect(self.update_image)

        # Create the layout and add the label and list box
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.image_list)
        self.setLayout(vbox)

        self.show()

    def update_image(self, image):
        self.image_label.setPixmap(QPixmap(image))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageSelector()
    sys.exit(app.exec_())

