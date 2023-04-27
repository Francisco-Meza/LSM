import numpy as np
import tensorflow as tf
import serial

# crea la lista de etiquetas de señales de lengua de señas mexicanas
etiquetas = ['A', 'B', 'C', 'D', 'E', 'F', 'G','H','I','L','M','N','O']

# carga la red neuronal previamente entrenada
model = tf.keras.models.load_model('model.h5')

# establece la conexión con el puerto serial
ser = serial.Serial('COM9', 9600) # ajusta el puerto y la velocidad según corresponda

# función para leer los valores del sensor y realizar una predicción
def hacer_prediccion():
    # lee los valores del sensor separados por comas
    datos = ser.readline().decode('utf-8').strip().split(',')
    
    # convierte los valores a números y promedia por sensor
    promedios = np.mean(np.array(list(map(float, datos))).reshape(18, -1), axis=1)
    
    # realiza la predicción y devuelve la etiqueta correspondiente
    prediccion = etiquetas[np.argmax(model.predict(np.array(promedios).reshape(1, -1)))]
    return prediccion

# bucle principal para leer continuamente los valores del sensor y hacer predicciones
while True:
    etiqueta_predicha = hacer_prediccion()
    print('Etiqueta predicha:', etiqueta_predicha)
