import serial as ser
import tkinter as tk
from tkinter import ttk, PhotoImage
#Funcion para actualizar imagenes
def update_image(event):
    seleccion = listBox.get()
    image = PhotoImage(file=f"utilidades/{seleccion}.png")
    label.configure(image=image)
    label.image = image
# Función para actualizar los datos en la interfaz gráfica
def actualizar_datos():
    i =0
    valor1.set(10+i)
    i = i+10
    # Programar la función para que se ejecute cada cierto tiempo
    root.after(1000, actualizar_datos)

# Crear la ventana principal
root = tk.Tk()
root.title("SMAIN")
root.geometry("400x300")

# Crear un widget de etiqueta
image = PhotoImage(file="utilidades/a.png")
label = tk.Label(root, image=image)
label.pack()
#Combobox
listBox = ttk.Combobox(
    state="readonly",
    values= [
    "A",
    "B",
    "C",
    "D",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "Ñ",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z"]
)
listBox.set("Default")
listBox.pack()
listBox.bind("<<ComboboxSelected>>", update_image)

# Crear un botón
button = tk.Button(root, text="Cerrar", command=root.quit)
button.pack()

# Creación de las barras de progreso
valor1 = tk.DoubleVar()
barra1 = ttk.Progressbar(root, variable=valor1, maximum=100)
barra1.pack()

valor2 = tk.DoubleVar()
barra2 = ttk.Progressbar(root, variable=valor2, maximum=100)
barra2.pack()

valor3 = tk.DoubleVar()
barra3 = ttk.Progressbar(root, variable=valor3, maximum=1023)
barra3.pack()

# Ejecución de la función para actualizar los datos
actualizar_datos()

# Mostrar la ventana principal
root.mainloop()
