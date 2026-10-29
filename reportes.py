"""
reportes.py
Cuatro reportes con busqueda integrada:
  1. Pedidos pendientes por zona de despacho
  2. Productos del catalogo filtrados por categoria
  3. Clientes Wong Prime activos
  4. Cumplimiento de SLA por repartidor
"""

from ordenamiento import (
    ordenar_pedidos_burbuja,
    ordenar_productos_seleccion,
    ordenar_clientes_insercion,
)


def reporte_pedidos_por_zona(pedidos, distrito_buscado):
    """
    Reporte 1.
    Filtra los pedidos por distrito y los devuelve ordenados por hora limite.
    Si distrito_buscado es 'TODAS', devuelve todos los pedidos.
    """
    filtrados = []
    for p in pedidos:
        if distrito_buscado == "TODAS" or p.distrito.upper() == distrito_buscado.upper():
            filtrados.append(p)

    filtrados = ordenar_pedidos_burbuja(filtrados)
    return filtrados


def reporte_productos_por_categoria(productos, categoria_buscada):
    """
    Reporte 2.
    Filtra productos por categoria y los devuelve ordenados por rotacion descendente.
    """
    filtrados = []
    for p in productos:
        if categoria_buscada == "TODAS" or p.categoria.upper() == categoria_buscada.upper():
            filtrados.append(p)

    filtrados = ordenar_productos_seleccion(filtrados)
    return filtrados


def reporte_clientes_prime(clientes):
    """
    Reporte 3.
    Devuelve solo los clientes Wong Prime ordenados por monto total descendente.
    """
    prime = [c for c in clientes if c.es_prime]
    prime = ordenar_clientes_insercion(prime)
    return prime


def reporte_sla_por_repartidor(pedidos):
    """
    Reporte 4.
    Calcula el cumplimiento de SLA por cada repartidor.
    Considera solo pedidos ENTREGADOS con repartidor asignado.

    Devuelve una lista de diccionarios con:
      - repartidor (nombre)
      - total_entregados
      - a_tiempo
      - tarde
      - porcentaje_cumplimiento
    """
    # Agrupar pedidos entregados por repartidor
    por_repartidor = {}
    for p in pedidos:
        if p.estado_actual != "ENTREGADO" or p.repartidor_dni is None:
            continue
        clave = (p.repartidor_dni, p.repartidor_nombre)
        if clave not in por_repartidor:
            por_repartidor[clave] = {"a_tiempo": 0, "tarde": 0, "pedidos": []}
        if p.cumplio_sla():
            por_repartidor[clave]["a_tiempo"] += 1
        else:
            por_repartidor[clave]["tarde"] += 1
        por_repartidor[clave]["pedidos"].append(p.codigo)

    # Armar resultado
    resultado = []
    for (dni, nombre), datos in por_repartidor.items():
        total = datos["a_tiempo"] + datos["tarde"]
        porcentaje = (datos["a_tiempo"] / total * 100) if total > 0 else 0
        resultado.append({
            "repartidor_dni": dni,
            "repartidor_nombre": nombre,
            "total_entregados": total,
            "a_tiempo": datos["a_tiempo"],
            "tarde": datos["tarde"],
            "porcentaje_cumplimiento": round(porcentaje, 1),
            "pedidos": datos["pedidos"],
        })

    # Ordenar por porcentaje de cumplimiento descendente
    resultado.sort(key=lambda r: r["porcentaje_cumplimiento"], reverse=True)
    return resultado
