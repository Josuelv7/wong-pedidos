"""
tabla_hash.py
Tabla hash con manejo de colisiones por encadenamiento.
Se usa para indexar pedidos por su codigo y permitir
busqueda en tiempo constante promedio O(1).
"""


class TablaHash:
    def __init__(self, tamano=29):
        # 29 es un numero primo, ayuda a distribuir mejor las claves
        self.tamano = tamano
        self.tabla = [[] for _ in range(tamano)]
        self.total = 0

    def _funcion_hash(self, clave):
        """Funcion hash simple: suma de codigos ASCII modulo tamano."""
        clave_str = str(clave)
        suma = 0
        for caracter in clave_str:
            suma += ord(caracter)
        return suma % self.tamano

    def insertar(self, clave, valor):
        indice = self._funcion_hash(clave)
        # Si la clave ya existe, se actualiza
        for i, (k, v) in enumerate(self.tabla[indice]):
            if k == clave:
                self.tabla[indice][i] = (clave, valor)
                return
        self.tabla[indice].append((clave, valor))
        self.total += 1

    def buscar(self, clave):
        indice = self._funcion_hash(clave)
        for k, v in self.tabla[indice]:
            if k == clave:
                return v
        return None

    def eliminar(self, clave):
        indice = self._funcion_hash(clave)
        for i, (k, v) in enumerate(self.tabla[indice]):
            if k == clave:
                self.tabla[indice].pop(i)
                self.total -= 1
                return True
        return False

    def listar_todos(self):
        """Devuelve todos los valores almacenados."""
        resultado = []
        for cubeta in self.tabla:
            for k, v in cubeta:
                resultado.append(v)
        return resultado

    def estadisticas(self):
        """Devuelve estadisticas de la tabla (util para reportes)."""
        ocupadas = sum(1 for c in self.tabla if len(c) > 0)
        colisiones = sum(len(c) - 1 for c in self.tabla if len(c) > 1)
        return {
            "total_elementos": self.total,
            "cubetas_ocupadas": ocupadas,
            "total_cubetas": self.tamano,
            "colisiones": colisiones
        }
