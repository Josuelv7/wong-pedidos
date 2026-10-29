"""
datos_iniciales.py
Carga datos de prueba para demostrar el funcionamiento del sistema.
Incluye:
  - Clientes con membresia Prime y puntos Bonus
  - Productos con stock distribuido por sede (8 sedes Wong)
  - Arbol de categorias
  - Repartidores
  - Pedidos iniciales (algunos pendientes, algunos entregados para reporte SLA)
"""

from datetime import datetime, timedelta

from cliente import Cliente
from producto import Producto
from pedido import Pedido
from lista_enlazada import ListaEnlazada
from geografia import sede_asignada, calcular_recargo, tiene_tienda


# Sedes Wong de referencia (las 8 con tienda + cobertura de delivery)
SEDES = [
    "WONG-OVAL", "WONG-CAMINO", "WONG-CHACARILLA",
    "WONG-MOLINA", "WONG-SANBORJA", "WONG-RISSO",
    "WONG-DASSO", "WONG-TRUJILLO"
]


# Repartidores asignables a los pedidos
REPARTIDORES = [
    ("72839456", "Carlos Mendez Quispe"),
    ("45128973", "Maria Picker Suarez"),
    ("38927461", "Luis Quispe Vargas"),
    ("65129834", "Sandra Torres Lopez"),
    ("88123945", "Roberto Diaz Silva"),
]


def cargar_clientes():
    clientes = [
        Cliente("70123456", "Ana Rojas Quispe", es_prime=True, puntos_bonus=120),
        Cliente("45678912", "Carlos Mendoza Diaz", es_prime=False, puntos_bonus=30),
        Cliente("87654321", "Lucia Fernandez Soto", es_prime=True, puntos_bonus=210),
        Cliente("12345678", "Pedro Castillo Rios", es_prime=False, puntos_bonus=15),
        Cliente("99887766", "Maria Garcia Lopez", es_prime=True, puntos_bonus=340),
        Cliente("55443322", "Jose Vargas Pinto", es_prime=False, puntos_bonus=8),
    ]
    clientes[0].historial_compras = [85.50, 120.00, 220.30, 95.00]
    clientes[1].historial_compras = [45.00, 78.50, 32.00]
    clientes[2].historial_compras = [150.00, 280.00, 420.50, 195.00, 88.00]
    clientes[3].historial_compras = [25.50, 18.00]
    clientes[4].historial_compras = [320.00, 450.00, 580.00, 290.00]
    clientes[5].historial_compras = [38.00, 22.50]
    return clientes


def _stock(p_oval, p_camino, p_chacarilla, p_molina, p_sanborja, p_risso, p_dasso, p_trujillo):
    """Helper: arma el dict de stock por sede en orden."""
    return {
        "WONG-OVAL": p_oval, "WONG-CAMINO": p_camino, "WONG-CHACARILLA": p_chacarilla,
        "WONG-MOLINA": p_molina, "WONG-SANBORJA": p_sanborja, "WONG-RISSO": p_risso,
        "WONG-DASSO": p_dasso, "WONG-TRUJILLO": p_trujillo,
    }


def cargar_productos():
    return [
        # codigo, nombre, categoria, subcategoria, precio, stock_por_sede, rotacion
        Producto("P001", "Arroz Costeño 5kg",     "Abarrotes", "Granos",         28.90, _stock(8,  6,  7,  5,  6,  4, 7,  7),  180),
        Producto("P002", "Aceite Primor 1L",      "Abarrotes", "Aceites",        12.50, _stock(12, 10, 11, 8,  9,  7, 11, 12), 220),
        Producto("P003", "Azucar Cartavio 1kg",   "Abarrotes", "Granos",         4.80,  _stock(15, 12, 14, 10, 11, 9, 13, 16), 310),
        Producto("P004", "Leche Gloria 1L",       "Perecibles", "Lacteos",       5.50,  _stock(18, 15, 17, 13, 14, 11, 16, 16), 450),
        Producto("P005", "Queso Laive 200g",      "Perecibles", "Lacteos",       14.90, _stock(6,  5,  5,  4,  5,  3, 6,  6),  95),
        Producto("P006", "Pan Bimbo grande",      "Perecibles", "Panaderia",     7.20,  _stock(10, 8,  8,  6,  7,  5, 8,  8),  280),
        Producto("P007", "Inca Kola 1.5L",        "Bebidas",   "Gaseosas",       8.50,  _stock(25, 22, 24, 20, 21, 18, 23, 27), 520),
        Producto("P008", "Agua San Luis 2.5L",    "Bebidas",   "Aguas",          5.00,  _stock(20, 17, 19, 15, 16, 13, 18, 32), 380),
        Producto("P009", "Jugo Frugos 1L",        "Bebidas",   "Jugos",          6.50,  _stock(12, 10, 11, 9,  10, 8, 11, 9),  160),
        Producto("P010", "Detergente Ariel 800g", "Limpieza",  "Lavanderia",     18.90, _stock(9,  8,  9,  7,  8,  6, 9,  14), 140),
        Producto("P011", "Lejia Clorox 1L",       "Limpieza",  "Desinfectantes", 7.80,  _stock(11, 10, 11, 9,  10, 8, 10, 16), 105),
        Producto("P012", "Shampoo Head 400ml",    "Cuidado Personal", "Cabello", 25.50, _stock(6,  5,  6,  4,  5,  3, 6,  10), 80),
        Producto("P013", "Pasta Colgate 100g",    "Cuidado Personal", "Higiene Bucal", 6.90, _stock(14, 12, 14, 11, 12, 10, 13, 24), 240),
        Producto("P014", "Pollo congelado 2kg",   "Congelados", "Carnes",        32.00, _stock(3,  3,  3,  3,  3,  2, 4,  4),  75),
        Producto("P015", "Helado Donofrio 1L",    "Congelados", "Postres",       19.50, _stock(5,  4,  5,  3,  4,  3, 5,  6),  130),
    ]


def cargar_arbol_categorias():
    return {
        "Abarrotes": ["Granos", "Aceites"],
        "Perecibles": ["Lacteos", "Panaderia"],
        "Bebidas": ["Gaseosas", "Aguas", "Jugos"],
        "Limpieza": ["Lavanderia", "Desinfectantes"],
        "Cuidado Personal": ["Cabello", "Higiene Bucal"],
        "Congelados": ["Carnes", "Postres"],
        "Granos": [], "Aceites": [], "Lacteos": [], "Panaderia": [],
        "Gaseosas": [], "Aguas": [], "Jugos": [],
        "Lavanderia": [], "Desinfectantes": [],
        "Cabello": [], "Higiene Bucal": [], "Carnes": [], "Postres": [],
    }


def cargar_pedidos_iniciales():
    """
    Carga pedidos de ejemplo. Algunos PENDIENTES y otros ENTREGADOS
    para alimentar el reporte de SLA por repartidor.
    """
    # Fecha de referencia: la jornada de hoy a las 8:00 am
    hoy = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)

    pedidos_data = [
        # (codigo, dni, distrito, canal, modalidad, sla_horas, monto, productos, desc, hora_conf, repartidor_idx, entregado_offset_h)
        ("PED0001", "70123456", "Miraflores",  "APP",  "DELIVERY",         3,  145.50, ["P001","P004","P007"], "Pedido familiar express",     hoy + timedelta(minutes=30), None, None),
        ("PED0002", "45678912", "San Isidro",  "WEB",  "DELIVERY",         6,   85.40, ["P002","P008","P011"], "Compra semanal pequeña",      hoy + timedelta(minutes=45), None, None),
        ("PED0003", "87654321", "La Molina",   "APP",  "RETIRO_EN_TIENDA", 3,  280.00, ["P014","P012","P006"], "Para reunion familiar",       hoy + timedelta(hours=1),    None, None),
        ("PED0004", "12345678", "Chorrillos",  "WEB",  "DELIVERY",         6,   48.30, ["P003","P009"],        "Pedido basico",               hoy + timedelta(hours=1, minutes=15), None, None),
        ("PED0005", "99887766", "San Borja",   "APP",  "DELIVERY",         3,  420.80, ["P014","P015","P012","P005"], "Compra premium Wong Prime", hoy + timedelta(hours=1, minutes=30), None, None),
        ("PED0006", "55443322", "Lince",       "PRESENCIAL", "RETIRO_EN_TIENDA", 24, 62.50, ["P002","P007","P011"], "Compra programada para manana", hoy + timedelta(hours=2), None, None),
        # Pedidos ENTREGADOS (de jornadas anteriores) para alimentar reporte SLA
        ("PED1001", "70123456", "Miraflores",  "APP",  "DELIVERY",         3,   95.00, ["P004","P008"],        "Compra rapida",               hoy - timedelta(days=1, hours=10), 0, 2),    # 2h: a tiempo (SLA 3h)
        ("PED1002", "99887766", "San Borja",   "APP",  "DELIVERY",         3,  195.40, ["P010","P013","P006","P009"], "Compra mensual",      hoy - timedelta(days=1, hours=8),  0, 4),    # 4h: TARDE
        ("PED1003", "87654321", "La Molina",   "WEB",  "DELIVERY",         6,  180.00, ["P001","P003","P004"], "Pedido programado",           hoy - timedelta(days=1, hours=14), 1, 5),    # 5h: a tiempo
        ("PED1004", "45678912", "Surco",       "APP",  "DELIVERY",         3,  120.00, ["P005","P006"],        "Almuerzo familiar",           hoy - timedelta(days=2, hours=6),  1, 2),    # 2h: a tiempo
        ("PED1005", "12345678", "Rimac",       "WEB",  "DELIVERY",         6,   70.00, ["P002","P007"],        "Pedido zona sin tienda",      hoy - timedelta(days=2, hours=12), 2, 7),    # 7h: TARDE
        ("PED1006", "55443322", "San Isidro",  "PRESENCIAL", "DELIVERY",   24,  55.00, ["P011","P013"],        "Pedido programado",           hoy - timedelta(days=3),            2, 20),   # 20h: a tiempo
    ]

    pedidos = []
    for (cod, dni, distrito, canal, modalidad, sla, monto, prods, desc,
         hora_conf, rep_idx, entregado_h) in pedidos_data:
        recargo = calcular_recargo(distrito, modalidad)
        sede = sede_asignada(distrito) or "WONG-OVAL"

        p = Pedido(cod, dni, distrito, canal, modalidad, sla, monto, prods,
                   descripcion=desc, hora_confirmacion=hora_conf,
                   sede_asignada=sede, recargo_envio=recargo)

        # Historial inicial
        p.historial = ListaEnlazada()
        p.historial.insertar_al_final({
            "estado": "PENDIENTE",
            "fecha": hora_conf.strftime("%Y-%m-%d %H:%M"),
            "responsable": "Sistema"
        })

        # Si tiene repartidor asignado, marcarlo y entregar segun offset
        if rep_idx is not None and entregado_h is not None:
            rep_dni, rep_nombre = REPARTIDORES[rep_idx]
            p.asignar_repartidor(rep_dni, rep_nombre)

            # Historial completo de un pedido entregado
            base = hora_conf
            for estado, offset_h, responsable in [
                ("EN PREPARACION", 0.2, "Picker Tienda"),
                ("LISTO PARA DESPACHO", 0.5, "Operaciones"),
                ("EN RUTA", 0.8, rep_nombre),
                ("ENTREGADO", entregado_h, rep_nombre),
            ]:
                fecha = base + timedelta(hours=offset_h)
                p.historial.insertar_al_final({
                    "estado": estado,
                    "fecha": fecha.strftime("%Y-%m-%d %H:%M"),
                    "responsable": responsable
                })
            p.marcar_entregado(base + timedelta(hours=entregado_h))

        pedidos.append(p)

    return pedidos
