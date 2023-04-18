import serial
import tkinter as tk
from tkinter import ttk, PhotoImage
def update_image(event):
    seleccion = listBox.get()
    image = PhotoImage(file=f"utilidades/{seleccion}.png")
    label.configure(image=image)
    label.image = image
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

# Mostrar la ventana principal
root.mainloop()
