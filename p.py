import tkinter as tk
from tkinter import ttk

# Crear la ventana principal
root = tk.Tk()
root.title("SMAIN")
root.geometry("400x300")

items = {
    
}

# Crear un widget de etiqueta
label = tk.Label(root, text="Hola Mundo!")
label.pack()

listBox = ttk.Combobox(
    state="readonly",
    values= ["Default",
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
# Crear un botón
button = tk.Button(root, text="Cerrar", command=root.quit)
button.pack()

# Mostrar la ventana principal
root.mainloop()
