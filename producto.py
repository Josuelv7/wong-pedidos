"""
producto.py
Define la clase Producto del catalogo Wong.

La subcategoria permite la busqueda recursiva en jerarquia.
El stock se distribuye por sede: cada producto tiene un diccionario
sede -> cantidad disponible.
"""


class Producto:
    def __init__(self, codigo, nombre, categoria, subcategoria, precio,
                 stock_por_sede, rotacion):
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.subcategoria = subcategoria
        self.precio = precio
        self.stock_por_sede = stock_por_sede  # dict {sede_id: cantidad}
        self.rotacion = rotacion  # unidades vendidas por semana (total)

    def stock_total(self):
        """Devuelve la suma de stock en todas las sedes."""
        return sum(self.stock_por_sede.values())

    def stock_en_sede(self, sede):
        """Devuelve el stock disponible en una sede especifica."""
        return self.stock_por_sede.get(sede, 0)

    def hay_stock_en(self, sede, cantidad=1):
        """Indica si hay al menos 'cantidad' unidades en la sede."""
        return self.stock_en_sede(sede) >= cantidad

    def descontar_stock(self, sede, cantidad=1):
        """
        Descuenta unidades del stock de una sede.
        Devuelve True si se pudo descontar, False si no habia suficiente.
        """
        if self.hay_stock_en(sede, cantidad):
            self.stock_por_sede[sede] -= cantidad
            return True
        return False

    def __str__(self):
        return (f"[{self.codigo}] {self.nombre} | {self.categoria}/{self.subcategoria} | "
                f"S/ {self.precio:.2f} | Stock total: {self.stock_total()} | "
                f"Rotacion: {self.rotacion}")
