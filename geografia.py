"""
geografia.py
Logica geografica de despacho para el canal digital de Wong.

Cada distrito puede tener o no una tienda Wong asociada:
  - Si tiene tienda: el cliente puede elegir entre RETIRO o DELIVERY
  - Si no tiene tienda: solo DELIVERY con recargo adicional

Las sedes representan las 21 tiendas fisicas de Wong a nivel nacional.
"""

# Mapeo distrito -> codigo de sede Wong (basado en tiendas reales)
DISTRITOS_CON_TIENDA = {
    "Miraflores":   "WONG-OVAL",
    "San Isidro":   "WONG-CAMINO",
    "Surco":        "WONG-CHACARILLA",
    "La Molina":    "WONG-MOLINA",
    "San Borja":    "WONG-SANBORJA",
    "Lince":        "WONG-RISSO",
    "Surquillo":    "WONG-DASSO",
    "Trujillo":     "WONG-TRUJILLO",
}

# Sedes con cobertura de delivery a distritos sin tienda
# (mapeo distrito sin tienda -> sede mas cercana que lo atiende)
COBERTURA_DELIVERY = {
    "Rimac":              "WONG-RISSO",
    "Comas":              "WONG-RISSO",
    "San Juan de Lurigancho": "WONG-RISSO",
    "Los Olivos":         "WONG-RISSO",
    "Villa El Salvador":  "WONG-CHACARILLA",
    "Villa Maria":        "WONG-CHACARILLA",
    "Chorrillos":         "WONG-CHACARILLA",
    "Ate":                "WONG-MOLINA",
    "Santa Anita":        "WONG-MOLINA",
    "Magdalena":          "WONG-OVAL",
    "San Miguel":         "WONG-OVAL",
    "Pueblo Libre":       "WONG-OVAL",
    "Jesus Maria":        "WONG-RISSO",
    "Brena":              "WONG-RISSO",
    "Callao":             "WONG-OVAL",
    "Bellavista":         "WONG-OVAL",
}

# Recargo adicional cuando el distrito no tiene tienda Wong
RECARGO_SIN_TIENDA = 8.50  # soles


def tiene_tienda(distrito):
    """Devuelve True si el distrito cuenta con tienda Wong."""
    return distrito in DISTRITOS_CON_TIENDA


def tienda_de_distrito(distrito):
    """Devuelve la sede que esta ubicada en el distrito o None."""
    return DISTRITOS_CON_TIENDA.get(distrito)


def sede_asignada(distrito):
    """
    Devuelve la sede que atendera el pedido segun el distrito de entrega.
    - Si el distrito tiene tienda: esa misma sede
    - Si no tiene tienda: la sede mas cercana segun cobertura
    - Si no hay cobertura registrada: devuelve None
    """
    if distrito in DISTRITOS_CON_TIENDA:
        return DISTRITOS_CON_TIENDA[distrito]
    if distrito in COBERTURA_DELIVERY:
        return COBERTURA_DELIVERY[distrito]
    return None


def modalidades_permitidas(distrito):
    """Devuelve la lista de modalidades disponibles para el distrito."""
    if tiene_tienda(distrito):
        return ["DELIVERY", "RETIRO_EN_TIENDA"]
    return ["DELIVERY"]


def calcular_recargo(distrito, modalidad):
    """Calcula el recargo de envio segun distrito y modalidad."""
    if modalidad == "RETIRO_EN_TIENDA":
        return 0.0
    if not tiene_tienda(distrito):
        return RECARGO_SIN_TIENDA
    return 0.0


def listar_distritos():
    """Devuelve la lista completa de distritos cubiertos."""
    todos = list(DISTRITOS_CON_TIENDA.keys()) + list(COBERTURA_DELIVERY.keys())
    return sorted(set(todos))
