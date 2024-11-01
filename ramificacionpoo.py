import tkinter as tk
from tkinter import messagebox
from pulp import LpMaximize, LpProblem, LpVariable, LpStatus, PULP_CBC_CMD

class ProblemaProgramacionEntera:
    def __init__(self, coef_x, coef_y, restriccion_1, restriccion_2):
        self.prob = LpProblem("Ejemplo_Programacion_Entera", LpMaximize)
        self.x = LpVariable('x', lowBound=0, cat='Integer')
        self.y = LpVariable('y', lowBound=0, cat='Integer')
        self.coef_x = coef_x
        self.coef_y = coef_y
        self.restriccion_1 = restriccion_1
        self.restriccion_2 = restriccion_2

        self.definir_objetivo()
        self.definir_restricciones()
        self.resolver()

    def definir_objetivo(self):
        # Definir la función objetivo
        self.prob += self.coef_x * self.x + self.coef_y * self.y, "Función Objetivo"

    def definir_restricciones(self):
        # Definir las restricciones
        self.prob += self.x + self.y <= self.restriccion_1, "Restriccion_1"
        self.prob += self.x - self.y >= self.restriccion_2, "Restriccion_2"

    def resolver(self):
        # Resolver el problema utilizando el solucionador por defecto (CBC)
        self.prob.solve(PULP_CBC_CMD(msg=True))
        return self.obtener_resultados()

    def obtener_resultados(self):
        # Mostrar el estado de la solución
        estado = LpStatus[self.prob.status]
        resultados = {
            'estado': estado,
            'x': self.x.varValue,
            'y': self.y.varValue,
            'valor_optimo': self.prob.objective.value()
        }
        return resultados

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Programación Entera")

        # Crear campos de entrada
        tk.Label(root, text="Coeficiente de x:").grid(row=0, column=0)
        self.coef_x_entry = tk.Entry(root)
        self.coef_x_entry.grid(row=0, column=1)

        tk.Label(root, text="Coeficiente de y:").grid(row=1, column=0)
        self.coef_y_entry = tk.Entry(root)
        self.coef_y_entry.grid(row=1, column=1)

        tk.Label(root, text="Restricción 1:").grid(row=2, column=0)
        self.restriccion_1_entry = tk.Entry(root)
        self.restriccion_1_entry.grid(row=2, column=1)

        tk.Label(root, text="Restricción 2:").grid(row=3, column=0)
        self.restriccion_2_entry = tk.Entry(root)
        self.restriccion_2_entry.grid(row=3, column=1)

        # Botón para resolver el problema
        self.solve_button = tk.Button(root, text="Resolver", command=self.resolver)
        self.solve_button.grid(row=4, columnspan=2)

    def resolver(self):
        # Obtener los valores de entrada
        try:
            coef_x = float(self.coef_x_entry.get())
            coef_y = float(self.coef_y_entry.get())
            restriccion_1 = float(self.restriccion_1_entry.get())
            restriccion_2 = float(self.restriccion_2_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos.")
            return

        # Crear el problema y resolverlo
        problema = ProblemaProgramacionEntera(coef_x, coef_y, restriccion_1, restriccion_2)
        resultados = problema.resolver()

        # Mostrar los resultados
        resultado_texto = f"Estado de la solución: {resultados['estado']}\n"
        resultado_texto += f"x = {resultados['x']}\n"
        resultado_texto += f"y = {resultados['y']}\n"
        resultado_texto += f"Valor óptimo de Z = {resultados['valor_optimo']}"

        messagebox.showinfo("Resultados", resultado_texto)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
