import serial
import numpy as np
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import joblib
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
        self.current_word = QLabel("")

        # Inicializar el botón de reiniciar la palabra
        self.reset_button = QPushButton("Reiniciar")
        self.reset_button.clicked.connect(self.reset_word)

        self.start_button = QPushButton("Iniciar")
        self.start_button.clicked.connect(self.predict)

        # Crear el layout vertical y agregar todos los elementos
        vbox = QVBoxLayout()
        vbox.addWidget(self.current_prediction)
        vbox.addWidget(self.current_word)
        hbox = QHBoxLayout()
        hbox.addWidget(self.reset_button)
        hbox.addWidget(self.start_button)
        hbox.addStretch(1)
        vbox.addLayout(hbox)

        # Crear el widget principal y establecer el layout
        main_widget = QWidget()
        main_widget.setLayout(vbox)

        # Establecer el widget principal como el widget central de la ventana
        self.setCentralWidget(main_widget)

        # Inicializar el contador de predicciones
        self.prediction_count = 0

    def reset_word(self):
        self.current_word.setText("")
        self.prediction_count = 0

    def update_word(self, prediction):
        self.prediction_count += 1
        if self.prediction_count >= 50:
            # Encontrar la clase más común en las últimas 50 predicciones
            predictions = np.array(self.current_word.text().split())
            most_common = np.argmax(np.bincount(predictions))
            word = self.class_labels[most_common]
            # Agregar la palabra actual a la etiqueta de la palabra
            self.current_word.setText(f"{self.current_word.text()} {word}")
            # Reiniciar el contador de predicciones
            self.prediction_count = 0

    def predict(self):
        i = 0
        while True:
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
            print(class_label)
            #self.current_prediction.setText(f"Predicción: {class_label}")
            

            # Actualizar la palabra actual si es necesario
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

