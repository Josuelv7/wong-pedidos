"""
cola_prioridad.py
Cola de prioridad implementada manualmente (sin heapq) para fines academicos.

Prioridad de los pedidos:
  1. Hora limite calculada mas temprana primero (hora_confirmacion + sla_horas)
  2. Si hay empate, Wong Prime tiene prioridad sobre cliente normal

Internamente se mantiene una lista ordenada al momento de insertar.
"""


class ColaPrioridad:
    def __init__(self):
        self.items = []  # cada item es una tupla (prioridad_tupla, pedido)

    def _prioridad(self, pedido, es_prime):
        # hora_limite es un datetime calculado: confirmacion + SLA
        # Se compara directamente porque los datetime son ordenables
        # Se usa 0 para Prime y 1 para Normal asi Prime queda primero
        return (pedido.hora_limite, 0 if es_prime else 1)

    def insertar(self, pedido, es_prime):
        nueva_prio = self._prioridad(pedido, es_prime)
        # Buscar la posicion correcta para mantener orden ascendente
        posicion = 0
        while posicion < len(self.items) and self.items[posicion][0] <= nueva_prio:
            posicion += 1
        self.items.insert(posicion, (nueva_prio, pedido))

    def extraer(self):
        """Devuelve y elimina el pedido de mayor prioridad."""
        if self.esta_vacia():
            return None
        return self.items.pop(0)[1]

    def ver_frente(self):
        """Devuelve el pedido del frente sin eliminarlo."""
        if self.esta_vacia():
            return None
        return self.items[0][1]

    def esta_vacia(self):
        return len(self.items) == 0

    def tamano(self):
        return len(self.items)

    def listar_todos(self):
        """Devuelve la lista de pedidos en orden de prioridad."""
        return [item[1] for item in self.items]
