import serial
import numpy as np
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import joblib
import time
import pyttsx3
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Predicción de Palabras")
        self.setGeometry(100, 100, 400, 300)
        
        # Cargar el modelo ya entrenado
        self.model = load_model('model.h5')

        # Inicializar el objeto Serial para leer los datos del Arduino
        self.ser = serial.Serial('COM3', 9600)

        # Inicializar el objeto MinMaxScaler para escalar los datos en tiempo real
        self.scaler = joblib.load('scaler.save')

        # Definir el número de características y clases
        self.num_features = 18
        self.class_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G','H','I','L','M','N','O']

        # Inicializar la etiqueta de la predicción actual
        self.current_prediction = QLabel("Esperando predicciones...")

        # Inicializar la etiqueta de la palabra actual
        self.labelx = QLabel("Palabra: ")
        self.current_word = QLabel("puto")

        # Inicializar el botón de reiniciar la palabra
        self.reset_button = QPushButton("Reiniciar")
        self.reset_button.clicked.connect(self.reset_word)

        self.play_button = QPushButton("Hablar")
        self.play_button.clicked.connect(self.play)

        self.start_button = QPushButton("Iniciar")
        self.start_button.clicked.connect(self.predict)

        # Crear el layout vertical y agregar todos los elementos
        vbox = QVBoxLayout()
        vbox.addWidget(self.current_prediction)
        vbox.addWidget(self.current_word)
        vbox.addWidget(self.labelx)

        hbox = QHBoxLayout()
        hbox.addWidget(self.reset_button)
        hbox.addWidget(self.start_button)
        hbox.addWidget(self.play_button)
        hbox.addStretch(1)
        vbox.addLayout(hbox)

        # Crear el widget principal y establecer el layout
        main_widget = QWidget()
        main_widget.setLayout(vbox)

        # Establecer el widget principal como el widget central de la ventana
        self.setCentralWidget(main_widget)

    def reset_word(self):
        self.current_word.setText("")

    def update_word(self, prediction):
        most_common = max(set(prediction), key = prediction.count)
        print(most_common)
        # Agregar la palabra actual a la etiqueta de la palabra
        self.current_word.setText(f"{self.current_word.text()} {most_common}")
        # Reiniciar el contador de predicciones

    def predict(self):
        total = []
        for i in range(10):
            # Leer una línea de datos del Arduino
            line = self.ser.readline().decode().strip()

            # Convertir la línea de texto a un arreglo de números
            data = np.array([float(x) for x in line.split(',')])

            # Escalar los datos
            scaled_data = self.scaler.transform(data.reshape(1, -1))

            # Realizar la predicción con el modelo
            prediction = self.model.predict(scaled_data)

            # Convertir la salida a una clase utilizando argmax
            class_idx = np.argmax(prediction)

            # Obtener la etiqueta de la clase predicha
            class_label = self.class_labels[class_idx]

            # Actualizar la etiqueta de la predicción actual
            #print(class_label)
            total.append(class_label)
            #self.current_prediction.setText(f"Predicción: {class_label}")
            if(i==9):
                self.update_word(total)
                total.clear()
    def play(self):
        # Inicializar el motor de texto a voz
        engine = pyttsx3.init()

        # Definir el mensaje que se desea reproducir
        message = self.current_word.text()

        # Establecer la velocidad de reproducción
        engine.setProperty('rate', 150)

        # Reproducir el mensaje
        engine.say(message)
        engine.runAndWait()
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

