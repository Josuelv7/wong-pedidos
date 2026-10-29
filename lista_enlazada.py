"""
lista_enlazada.py
Implementacion de una lista enlazada simple.
Se usa para guardar el historial de estados de cada pedido.
Cada nodo contiene: estado, fecha-hora y responsable del cambio.
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor  # dict con estado, fecha y responsable
        self.siguiente = None


class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
        self.tamano = 0

    def insertar_al_final(self, valor):
        nuevo = Nodo(valor)
        if self.cabeza is None:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self.tamano += 1

    def recorrer(self):
        """Devuelve una lista con todos los valores en orden."""
        resultado = []
        actual = self.cabeza
        while actual is not None:
            resultado.append(actual.valor)
            actual = actual.siguiente
        return resultado

    def longitud(self):
        return self.tamano

    def ultimo(self):
        """Devuelve el valor del ultimo nodo (estado actual)."""
        if self.cabeza is None:
            return None
        actual = self.cabeza
        while actual.siguiente is not None:
            actual = actual.siguiente
        return actual.valor
