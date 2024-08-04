import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from moviepy.editor import VideoFileClip
import os
import threading

def convert_avi_to_mp4(input_file, output_file):
    video = VideoFileClip(input_file)
    video.write_videofile(output_file, codec='libx264')

def batch_convert(directory, progress_var, status_label):
    files = [f for f in os.listdir(directory) if f.endswith(".avi")]
    total_files = len(files)
    if total_files == 0:
        status_label.config(text="No se encontraron archivos AVI en el directorio.")
        return

    for i, filename in enumerate(files, start=1):
        input_path = os.path.join(directory, filename)
        output_path = os.path.splitext(input_path)[0] + ".mp4"
        convert_avi_to_mp4(input_path, output_path)
        progress_var.set((i / total_files) * 100)
        status_label.config(text=f"Convertido: {filename} a {os.path.basename(output_path)}")
        root.update_idletasks()  

    progress_var.set(100)
    status_label.config(text="Conversión completada!")

def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        status_label.config(text="Iniciando conversión...")
        progress_var.set(0)
        threading.Thread(target=batch_convert, args=(directory, progress_var, status_label)).start()

# Crear la ventana principal
root = tk.Tk()
root.title("Conversión de Videos AVI a MP4")

# Crear un marco para el contenido
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Etiqueta de instrucciones
label = tk.Label(frame, text="Selecciona un directorio para convertir archivos AVI a MP4.")
label.pack(pady=5)

# Botón para seleccionar el directorio
btn_select_directory = tk.Button(frame, text="Seleccionar Directorio", command=select_directory)
btn_select_directory.pack(pady=5)

# Etiqueta de estado
status_label = tk.Label(frame, text="", wraplength=300)
status_label.pack(pady=5)

# Barra de progreso
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(frame, length=300, orient="horizontal", mode="determinate", variable=progress_var)
progress_bar.pack(pady=5)

# Ejecutar la interfaz gráfica
root.mainloop()
