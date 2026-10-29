"""
recursivos.py
Tres metodos recursivos aplicados al negocio Wong:
  1. Calculo de puntos Bonus acumulados a partir del historial de compras
  2. Busqueda recursiva de productos en una subcategoria (incluyendo sus hijas)
  3. Calculo escalonado del descuento Wong Prime por tramos
"""


def calcular_puntos_bonus(historial_compras, indice=0):
    """
    Metodo recursivo #1.
    Devuelve los puntos Bonus acumulados:
    Cada S/ 10 de compra equivale a 1 punto Bonus.
    Se procesa el historial uno por uno de forma recursiva.

    Caso base: cuando indice llega al final de la lista, devuelve 0.
    Caso recursivo: puntos del monto actual + puntos del resto.
    """
    # Caso base
    if indice >= len(historial_compras):
        return 0
    # Caso recursivo
    puntos_actual = int(historial_compras[indice] // 10)
    return puntos_actual + calcular_puntos_bonus(historial_compras, indice + 1)


def buscar_en_subcategorias(productos, categoria_buscada, arbol_categorias):
    """
    Metodo recursivo #2.
    Devuelve todos los productos que pertenecen a una categoria
    o a cualquiera de sus subcategorias (recorrido recursivo del arbol).

    arbol_categorias es un dict donde la clave es la categoria
    y el valor es una lista de subcategorias hijas. Una categoria
    con lista vacia es una hoja (las hojas son las que tienen productos).

    Ejemplo:
      arbol = {
          "Bebidas": ["Gaseosas", "Aguas", "Jugos"],
          "Gaseosas": [],   # hoja
          ...
      }
    """
    hijas = arbol_categorias.get(categoria_buscada, [])

    # Caso base: categoria hoja - se buscan productos cuya subcategoria coincida
    if len(hijas) == 0:
        encontrados = []
        for p in productos:
            if p.subcategoria == categoria_buscada:
                encontrados.append(p)
        return encontrados

    # Caso recursivo: bajamos a cada hija y unimos los resultados
    encontrados = []
    for hija in hijas:
        encontrados.extend(buscar_en_subcategorias(productos, hija, arbol_categorias))
    return encontrados


def calcular_descuento_prime(monto, canal="PRESENCIAL", niveles=None, indice=0):
    """
    Metodo recursivo #3.
    Calcula el descuento Wong Prime de forma escalonada por tramos,
    con un bonus adicional segun el canal de compra (practica comercial real).

    Reglas de descuento por tramo:
      - Hasta S/ 100        : 5% de descuento
      - De S/ 100 a S/ 300  : 8% de descuento sobre el exceso
      - De S/ 300 a S/ 500  : 12% de descuento sobre el exceso
      - Mayor a S/ 500      : 15% de descuento sobre el exceso

    Bonus por canal de compra (se suma al porcentaje de cada tramo):
      - APP        : +2 puntos porcentuales
      - WEB        : +1 punto porcentual
      - PRESENCIAL : +0 (precio regular)

    Caso base: cuando ya no hay mas tramos por aplicar.
    Caso recursivo: se calcula el descuento del tramo actual
    y se llama recursivamente con el saldo restante.
    """
    if niveles is None:
        niveles = [
            (100, 0.05),
            (200, 0.08),  # tramo de 100 a 300 (200 de ancho)
            (200, 0.12),  # tramo de 300 a 500 (200 de ancho)
            (float("inf"), 0.15)
        ]

    # Bonus por canal
    bonus_por_canal = {"APP": 0.02, "WEB": 0.01, "PRESENCIAL": 0.0}
    bonus = bonus_por_canal.get(canal.upper(), 0.0)

    # Caso base: si ya no queda monto o ya pasamos todos los tramos
    if monto <= 0 or indice >= len(niveles):
        return 0

    tope_tramo, porcentaje = niveles[indice]
    porcentaje_final = porcentaje + bonus

    # Se calcula el descuento de este tramo
    monto_aplicable = min(monto, tope_tramo)
    descuento_actual = monto_aplicable * porcentaje_final

    # Llamada recursiva con el monto restante en el siguiente tramo
    return descuento_actual + calcular_descuento_prime(
        monto - monto_aplicable, canal, niveles, indice + 1
    )
