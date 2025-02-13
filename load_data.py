import pandas as pd
from tkinter import ttk, filedialog

class LoadData:
    def __init__(self, parent, main_app):
        self.main_app = main_app
        frame = ttk.LabelFrame(parent, text="Carga de Datos", padding=10)
        frame.grid(row=0, column=0, sticky="ew", pady=10)

        self.btn_cargar = ttk.Button(frame, text="Cargar CSV", command=self.cargar_csv)
        self.btn_cargar.grid(row=0, column=0, sticky="w", padx=5)

        self.label_status = ttk.Label(frame, text="Seleccione un archivo CSV", foreground="grey")
        self.label_status.grid(row=0, column=1, sticky="w", padx=5)

    def cargar_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
        if file_path:
            self.main_app.data = pd.read_csv(file_path, header=None, delimiter=";")
            self.label_status.config(text="Datos cargados correctamente", foreground="green")
        else:
            self.label_status.config(text="No se seleccionó ningún archivo", foreground="red")
