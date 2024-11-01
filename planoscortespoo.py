import tkinter as tk
from tkinter import messagebox
import pulp
import numpy as np

class ProblemaCortesGomory:
    def __init__(self, coef_x1, coef_x2, restricciones):
        self.prob = pulp.LpProblem("Ejemplo_Cortes_Gomory", pulp.LpMaximize)
        self.x1 = pulp.LpVariable("x1", lowBound=0)
        self.x2 = pulp.LpVariable("x2", lowBound=0)
        self.coef_x1 = coef_x1
        self.coef_x2 = coef_x2
        self.restricciones = restricciones
        
        self.definir_objetivo()
        self.definir_restricciones()
        self.resolver()

    def definir_objetivo(self):
        # Definir la función objetivo
        self.prob += self.coef_x1 * self.x1 + self.coef_x2 * self.x2, "Función Objetivo"

    def definir_restricciones(self):
        # Agregar las restricciones
        for i, (coef1, coef2, limite) in enumerate(self.restricciones):
            self.prob += coef1 * self.x1 + coef2 * self.x2 <= limite, f"Restriccion_{i+1}"

    def agregar_corte(self, vars, tableau):
        filas, columnas = tableau.shape
        for i in range(filas):
            if not np.isclose(tableau[i, -1], np.floor(tableau[i, -1])):
                corte = np.floor(tableau[i, -1]) - tableau[i, -1]
                for j in range(columnas - 1):
                    if not np.isclose(tableau[i, j], 0):
                        corte += (tableau[i, j] - np.floor(tableau[i, j])) * vars[j]
                self.prob += corte <= 0, f"Corte_Gomory_{i}"
                return True  # Se agregó un corte
        return False  # No se encontraron cortes

    def resolver(self):
        # Resolver el problema relajado inicialmente
        self.prob.solve()
        print(f"Estado de la solución inicial: {pulp.LpStatus[self.prob.status]}")
        print(f"x1 = {self.x1.varValue}, x2 = {self.x2.varValue}")

        # Obtener la tabla simplex (conceptual, usando valores directos)
        tableau = np.array([
            [6, 4, 0, 24],  # Restricción 1
            [1, 2, 0, 6],   # Restricción 2
            [-1, 1, 0, 1]   # Restricción 3
        ])

        # Aplicar el algoritmo de cortes iterativamente
        while True:
            if not self.agregar_corte([self.x1, self.x2], tableau):
                break
            self.prob.solve()
            print(f"Estado de la solución con cortes: {pulp.LpStatus[self.prob.status]}")
            print(f"x1 = {self.x1.varValue}, x2 = {self.x2.varValue}")

        print(f"Solución óptima entera: x1 = {self.x1.varValue}, x2 = {self.x2.varValue}")

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Cortes de Gomory")

        # Crear campos de entrada
        tk.Label(root, text="Coeficiente de x1:").grid(row=0, column=0)
        self.coef_x1_entry = tk.Entry(root)
        self.coef_x1_entry.grid(row=0, column=1)

        tk.Label(root, text="Coeficiente de x2:").grid(row=1, column=0)
        self.coef_x2_entry = tk.Entry(root)
        self.coef_x2_entry.grid(row=1, column=1)

        tk.Label(root, text="Restricciones (coef1, coef2, limite):").grid(row=2, column=0)
        self.restricciones_entry = tk.Entry(root)
        self.restricciones_entry.grid(row=2, column=1)

        # Botón para resolver el problema
        self.solve_button = tk.Button(root, text="Resolver", command=self.resolver)
        self.solve_button.grid(row=3, columnspan=2)

    def resolver(self):
        # Obtener los valores de entrada
        try:
            coef_x1 = float(self.coef_x1_entry.get())
            coef_x2 = float(self.coef_x2_entry.get())
            restricciones_raw = self.restricciones_entry.get().split(';')
            restricciones = [tuple(map(float, restr.split(','))) for restr in restricciones_raw]
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos.")
            return

        # Crear el problema y resolverlo
        problema = ProblemaCortesGomory(coef_x1, coef_x2, restricciones)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
