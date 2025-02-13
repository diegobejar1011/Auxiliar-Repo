import random
import tensorflow as tf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  
import tkinter.ttk as ttk
from Model import Model
import numpy as np

class Coach:
    def __init__(self, parent, main_app):
        self.main_app = main_app
        self.frame = ttk.LabelFrame(parent, text="Entrenamiento", padding=10)
        self.frame.grid(row=1, column=0, sticky="ew", pady=10)

        self.btn_entrenar = ttk.Button(self.frame, text="Iniciar Entrenamiento", command=self.train_model)
        self.btn_entrenar.grid(row=0, column=0, sticky="w", padx=5)

        self.loss_histories = []
        self.learning_rates = []


        self.table_frame = ttk.Frame(self.frame)
        self.table_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)

        self.tree = ttk.Treeview(self.table_frame, columns=("Tasa de aprendizaje", "Pesos Iniciales", "Pesos Finales", "Error", "Iteraciones"), show="headings")
        self.tree.heading("Tasa de aprendizaje", text="Tasa de aprendizaje")
        self.tree.heading("Pesos Iniciales", text="Pesos Iniciales")
        self.tree.heading("Pesos Finales", text="Pesos Finales")
        self.tree.heading("Error", text="Error")
        self.tree.heading("Iteraciones", text="Iteraciones")

        self.tree.grid(row=0, column=0, sticky="nsew")


        self.scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)

    def normalize_data(self, X_values, y_values):
        X_min, X_max = X_values.min(), X_values.max()
        y_min, y_max = y_values.min(), y_values.max()

        X_norm = (X_values - X_min) / (X_max - X_min)
        y_norm = (y_values - y_min) / (y_max - y_min)

        return X_norm, y_norm, X_min, X_max, y_min, y_max

    def train_model(self):
        if self.main_app.data is None:
            return
        
        X_values = self.main_app.data.iloc[:, :-1].values
        y_values = self.main_app.data.iloc[:, -1].values.reshape(-1, 1)

        X_norm, y_norm, X_min, X_max, y_min, y_max = self.normalize_data(X_values, y_values)

        X_tensor = tf.convert_to_tensor(X_norm, dtype=tf.float32)
        y_tensor = tf.convert_to_tensor(y_norm, dtype=tf.float32)

        input_dim = X_tensor.shape[1]
        self.learning_rates = [random.uniform(0, 5) for _ in range(10)]

        self.loss_histories = []
        self.table_data = []  

        for lr in self.learning_rates:
            modelo = Model(input_dim, lr)
            loss_history, initial_weights, final_weights, error, epochs = modelo.train(X_tensor, y_tensor)

            
            self.table_data.append((
                f"{lr:.4f}",
                self.vector_to_str(initial_weights),
                self.vector_to_str(final_weights),
                f"{error:.6f}",
                epochs
            ))

            self.loss_histories.append(loss_history)

        print("Entrenamiento finalizado")
        self.update_table()
        self.plot_training_results()

    def vector_to_str(self, vector):
        """Convierte un vector en una cadena legible para la tabla."""
        
        if isinstance(vector, (tuple, list)) and isinstance(vector[0], np.ndarray):
            vector = vector[0].flatten()
        
        return "[" + ", ".join([f"{val:.4f}" for val in vector]) + "]"


    def update_table(self):
        """Actualiza los datos de la tabla con los resultados del entrenamiento."""
        
        for item in self.tree.get_children():
            self.tree.delete(item)

        
        for row in self.table_data:
            self.tree.insert("", "end", values=row)

    def plot_training_results(self):
        """Genera y muestra la gráfica de las pérdidas durante el entrenamiento."""
        if not self.loss_histories:
            print("No hay datos de entrenamiento para graficar.")
            return

        
        if not hasattr(self, 'graph_window'):
            self.graph_window = ttk.Frame(self.frame)
            self.graph_window.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)

        
        for widget in self.graph_window.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(6, 4))
        for i, loss_history in enumerate(self.loss_histories):
            ax.plot(loss_history, label=f"Tasa {self.learning_rates[i]:.4f}")

        ax.set_xlabel("Épocas")
        ax.set_ylabel("Pérdida")
        ax.set_title("Historial de pérdida por tasa de aprendizaje")
        ax.legend()

        
        canvas = FigureCanvasTkAgg(fig, master=self.graph_window)
        canvas.get_tk_widget().pack(expand=True, fill="both")
        canvas.draw()
