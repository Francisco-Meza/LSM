import sys
import serial
import time
import numpy as np
import tensorflow as tf
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5 import QtCore

# Configurar puerto serial
ser = serial.Serial('COM9', 9600)
time.sleep(2)

# Cargar modelo
model = tf.keras.models.load_model('model.h5')

# Definir función para leer datos del puerto serial y hacer predicciones
def read_data_and_predict():
    line = ser.readline().decode().strip()
    value = float(line)
    distance_label.setText(f'Distancia: {value:.2f}')
    input_data = np.array([value])
    input_data = input_data.reshape((1, 1))
    prediction = model.predict(input_data)[0][0]
    if prediction >= 0.5:
        prediction_label.setText(f'Objeto detectado: sí ({prediction:.2f})')
    else:
        prediction_label.setText(f'Objeto detectado: no ({prediction:.2f})')
    QApplication.processEvents()

# Definir función para iniciar lectura y predicción de datos
def start_reading():
    btn_start.setEnabled(False)
    btn_stop.setEnabled(True)
    print('Iniciando lectura y predicción de datos...')
    while True:
        read_data_and_predict()

# Definir interfaz gráfica
app = QApplication([])
window = QWidget()
layout = QVBoxLayout()

# Etiquetas
title = QLabel('Detección de objetos')
distance_label = QLabel('Distancia: ')
prediction_label = QLabel('Objeto detectado: ')

# Botones
btn_start = QPushButton('Iniciar lectura')
btn_start.clicked.connect(start_reading)
btn_stop = QPushButton('Detener lectura')
btn_stop.setEnabled(False)
btn_stop.clicked.connect(lambda: sys.exit())

# Añadir elementos al layout
layout.addWidget(title)
layout.addWidget(distance_label)
layout.addWidget(prediction_label)
layout.addWidget(btn_start)
layout.addWidget(btn_stop)
layout.setAlignment(QtCore.Qt.AlignTop)

# Configurar ventana principal
window.setLayout(layout)
window.setWindowTitle('Detección de objetos')
window.show()
app.exec_()
