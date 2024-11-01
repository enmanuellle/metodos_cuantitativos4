import tkinter as tk
from tkinter import messagebox
from pulp import LpMaximize, LpProblem, LpVariable, LpStatus

class ProblemaMochila:
    def __init__(self, pesos, valores, capacidad):
        self.pesos = pesos
        self.valores = valores
        self.capacidad = capacidad
        self.problema_mochila = LpProblem("Problema_de_la_Mochila", LpMaximize)
        self.crear_variables()
        self.definir_objetivo()
        self.definir_restriccion()

    def crear_variables(self):
        # Definir las variables de decisión (0 o 1 para cada objeto)
        self.n = len(self.pesos)  # Número de objetos
        self.x = [LpVariable(f"x_{i+1}", cat='Binary') for i in range(self.n)]

    def definir_objetivo(self):
        # Definir la función objetivo (maximizar el valor total)
        self.problema_mochila += sum(self.valores[i] * self.x[i] for i in range(self.n)), "Valor_total"

    def definir_restriccion(self):
        # Definir la restricción de capacidad de la mochila
        self.problema_mochila += sum(self.pesos[i] * self.x[i] for i in range(self.n)) <= self.capacidad, "Capacidad_mochila"

    def resolver(self):
        # Resolver el problema
        self.problema_mochila.solve()
        return self.obtener_resultados()

    def obtener_resultados(self):
        # Mostrar el estado de la solución
        estado = LpStatus[self.problema_mochila.status]
        resultados = {
            'estado': estado,
            'objetos': [(i+1, self.x[i].varValue, self.pesos[i], self.valores[i]) for i in range(self.n)],
            'valor_total': sum(self.valores[i] * self.x[i].varValue for i in range(self.n)),
            'peso_total': sum(self.pesos[i] * self.x[i].varValue for i in range(self.n))
        }
        return resultados

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Problema de la Mochila")
        
        # Crear campos de entrada
        tk.Label(root, text="Pesos (separados por comas):").grid(row=0, column=0)
        self.pesos_entry = tk.Entry(root)
        self.pesos_entry.grid(row=0, column=1)

        tk.Label(root, text="Valores (separados por comas):").grid(row=1, column=0)
        self.valores_entry = tk.Entry(root)
        self.valores_entry.grid(row=1, column=1)

        tk.Label(root, text="Capacidad:").grid(row=2, column=0)
        self.capacidad_entry = tk.Entry(root)
        self.capacidad_entry.grid(row=2, column=1)

        # Botón para resolver el problema
        self.solve_button = tk.Button(root, text="Resolver", command=self.resolver)
        self.solve_button.grid(row=3, columnspan=2)

    def resolver(self):
        # Obtener los valores de entrada
        try:
            pesos = list(map(int, self.pesos_entry.get().split(',')))
            valores = list(map(int, self.valores_entry.get().split(',')))
            capacidad = int(self.capacidad_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos.")
            return

        # Crear el problema y resolverlo
        problema = ProblemaMochila(pesos, valores, capacidad)
        resultados = problema.resolver()

        # Mostrar los resultados
        resultado_texto = f"Estado de la solución: {resultados['estado']}\n"
        resultado_texto += "--- Objetos seleccionados ---\n"
        for objeto in resultados['objetos']:
            estado_objeto = 'Seleccionado' if objeto[1] == 1 else 'No seleccionado'
            resultado_texto += f"Objeto {objeto[0]}: {estado_objeto} (Peso: {objeto[2]}, Valor: {objeto[3]})\n"
        resultado_texto += f"\nValor total en la mochila: {resultados['valor_total']}\n"
        resultado_texto += f"Peso total en la mochila: {resultados['peso_total']}"

        messagebox.showinfo("Resultados", resultado_texto)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
