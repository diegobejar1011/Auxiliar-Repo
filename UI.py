from tkinter import ttk, Canvas, Scrollbar
from load_data import LoadData
from Training import Coach

class UI:
    def __init__(self, root):
        self.root = root
        self.root.title("Panel de Entrenamiento de Datos")
        self.root.geometry("1000x800")
        self.root.minsize(1000, 600)

        # Crear y configurar el estilo directamente aquí
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TLabel', padding=6)
        self.style.configure('TButton', padding=6, relief='raised', borderwidth=2, font=('Segoe UI', 9, 'bold'))
        self.style.map('TButton', foreground=[('active', '#fff')], background=[('active', '#4CAF50')])
        self.style.configure('TEntry', padding=5, borderwidth=2)

        self.data = None  

        self._create_interface()

    def _create_interface(self):
        # Crear un canvas y un scrollbar para la ventana
        canvas = Canvas(self.root)
        scroll_y = Scrollbar(self.root, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll_y.set)

        # Ubicar el canvas en la ventana principal
        canvas.grid(row=0, column=0, sticky="nsew")

        # Colocar el scrollbar a la derecha
        scroll_y.grid(row=0, column=1, sticky="ns")

        # Crear el frame principal dentro del canvas
        frame_principal = ttk.Frame(canvas, padding=20)
        canvas.create_window((0, 0), window=frame_principal, anchor="nw")

        # Configurar el tamaño del canvas para adaptarse al contenido
        frame_principal.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Crear los frames de carga y entrenamiento
        self.frame_carga = LoadData(frame_principal, self)
        self.frame_entrenamiento = Coach(frame_principal, self)

        # Configurar el grid de la ventana para que el canvas se expanda correctamente
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

