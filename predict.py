import serial
import numpy as np
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import joblib

# Cargar el modelo ya entrenado
model = load_model('model.h5')

# Inicializar el objeto Serial para leer los datos del Arduino
ser = serial.Serial('COM3',9600)

# Inicializar el objeto MinMaxScaler para escalar los datos en tiempo real
scaler = joblib.load('scaler.save')

# Definir el número de características y clases
num_features = 18
class_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G','H','I','L','M','N','O']

while True:
    # Leer una línea de datos del Arduino
    line = ser.readline().decode().strip()
    
    # Convertir la línea de texto a un arreglo de números
    data = np.array([float(x) for x in line.split(',')])
    
    # Escalar los datos
    scaled_data = scaler.transform(data.reshape(1, -1))
    
    # Realizar la predicción con el modelo
    prediction = model.predict(scaled_data)
    
    # Convertir la salida a una clase utilizando argmax
    class_idx = np.argmax(prediction)
    
    # Obtener la etiqueta de la clase predicha
    class_label = class_labels[class_idx]
    
    # Imprimir la predicción
    print(f'Predicción: {class_label}')
