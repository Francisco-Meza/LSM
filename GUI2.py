import csv
import serial
import time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QPushButton, QVBoxLayout
from PyQt5 import QtCore

# Configurar puerto serial
ser = "123,123,211,23,34"#serial.Serial('COM3', 9600)
time.sleep(2)

# Inicializar variables
data = []
labels = []
counter = 0

# Definir función para guardar datos
def save_data():
    global counter
    counter = 0
    with open('training_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        for i in range(len(data)):
            writer.writerow(data[i] + [labels[i]])
            counter += 1
            if counter >= 1000:
                print('Se han recolectado 1000 datos, deteniendo la recolección...')
                btn_stop.setEnabled(False)
                btn_start.setEnabled(True)
                return
    print('Se han guardado los datos en el archivo training_data.csv')
    data.clear()
    labels.clear()

# Definir función para leer datos del puerto serial
def read_data():
    line = ser#ser.readline().decode().strip()
    values = line.split(',')
    data.append([float(value) for value in values])
    labels.append(combobox.currentText())
    label_value.setText(f'Valor seleccionado: {combobox.currentText()}')
    sensor_value.setText(f'Valores del sensor: {line}')

# Definir función para iniciar recolección de datos
def start_recording():
    global counter
    counter = 0
    btn_start.setEnabled(False)
    btn_stop.setEnabled(True)
    print('Iniciando la recolección de datos...')
    while counter < 1000:
        read_data()
        counter += 1
        QApplication.processEvents()
    save_data()

# Definir interfaz gráfica
app = QApplication([])
window = QWidget()
layout = QVBoxLayout()

# Etiquetas
title = QLabel('Recolección de datos para entrenamiento')
sensor_label = QLabel('Valores del sensor:')
label_label = QLabel('Etiqueta:')
label_value = QLabel('Valor seleccionado: ')
sensor_value = QLabel('Valores del sensor: ')

# List box de etiquetas
combobox = QComboBox()
combobox.addItems(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])

# Botones
btn_start = QPushButton('Iniciar recolección')
btn_start.clicked.connect(start_recording)
btn_stop = QPushButton('Detener recolección')
btn_stop.setEnabled(False)
btn_stop.clicked.connect(save_data)

# Añadir elementos al layout
layout.addWidget(title)
layout.addWidget(sensor_label)
layout.addWidget(sensor_value)
layout.addWidget(label_label)
layout.addWidget(combobox)
layout.addWidget(label_value)
layout.addWidget(btn_start)
layout.addWidget(btn_stop)
layout.setAlignment(QtCore.Qt.AlignTop)

# Configurar ventana principal
window.setLayout(layout)
window.setWindowTitle('Recolección de datos')
window.show()
app.exec_()
