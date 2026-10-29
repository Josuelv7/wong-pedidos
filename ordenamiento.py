"""
ordenamiento.py
Tres metodos de ordenamiento implementados manualmente:
  - Burbuja: aplicado a pedidos por hora limite (calculada con SLA)
  - Seleccion: aplicado a productos por rotacion (descendente)
  - Insercion: aplicado a clientes por monto total de compras (descendente)
"""


def ordenar_pedidos_burbuja(pedidos):
    """
    Ordenamiento burbuja: ordena pedidos por hora_limite ascendente.
    La hora_limite es una propiedad calculada (hora_confirmacion + sla_horas).
    Devuelve una nueva lista (no modifica la original).
    Complejidad: O(n^2)
    """
    arr = pedidos.copy()
    n = len(arr)
    for i in range(n):
        intercambio = False
        for j in range(0, n - i - 1):
            if arr[j].hora_limite > arr[j + 1].hora_limite:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                intercambio = True
        if not intercambio:
            break
    return arr


def ordenar_productos_seleccion(productos):
    """
    Ordenamiento por seleccion: ordena productos por rotacion descendente.
    Devuelve una nueva lista.
    Complejidad: O(n^2)
    """
    arr = productos.copy()
    n = len(arr)
    for i in range(n):
        indice_max = i
        for j in range(i + 1, n):
            if arr[j].rotacion > arr[indice_max].rotacion:
                indice_max = j
        if indice_max != i:
            arr[i], arr[indice_max] = arr[indice_max], arr[i]
    return arr


def ordenar_clientes_insercion(clientes):
    """
    Ordenamiento por insercion: ordena clientes por monto total descendente.
    Devuelve una nueva lista.
    Complejidad: O(n^2) en el peor caso, O(n) si ya esta casi ordenado.
    """
    arr = clientes.copy()
    for i in range(1, len(arr)):
        actual = arr[i]
        j = i - 1
        while j >= 0 and arr[j].monto_total() < actual.monto_total():
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = actual
    return arr
