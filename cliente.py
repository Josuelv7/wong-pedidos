"""
cliente.py
Define la clase Cliente del canal digital de Wong.
"""


class Cliente:
    def __init__(self, dni, nombre, es_prime=False, puntos_bonus=0):
        self.dni = dni
        self.nombre = nombre
        self.es_prime = es_prime
        self.puntos_bonus = puntos_bonus
        self.historial_compras = []  # lista de montos de pedidos anteriores

    def monto_total(self):
        return sum(self.historial_compras)

    def __str__(self):
        prime = "PRIME" if self.es_prime else "NORMAL"
        return (f"{self.dni} - {self.nombre} ({prime}) | "
                f"Compras: S/ {self.monto_total():.2f} | "
                f"Puntos Bonus: {self.puntos_bonus}")
