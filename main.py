"""
main.py
Punto de entrada del Sistema de Gestion de Pedidos WongOnline.

Curso : IS207 Estructura de Datos y Algoritmos - UPC 2026-15
Grupo : Leyva, Yparraguirre, Crovetto, Aliaga
"""

from datetime import datetime

from cola_prioridad import ColaPrioridad
from tabla_hash import TablaHash
from lista_enlazada import ListaEnlazada
from pedido import Pedido
from datos_iniciales import (
    cargar_clientes, cargar_productos, cargar_arbol_categorias,
    cargar_pedidos_iniciales, REPARTIDORES, SEDES,
)
from geografia import (
    tiene_tienda, modalidades_permitidas, sede_asignada,
    calcular_recargo, listar_distritos,
)
from recursivos import (
    calcular_puntos_bonus, buscar_en_subcategorias, calcular_descuento_prime,
)
from reportes import (
    reporte_pedidos_por_zona, reporte_productos_por_categoria,
    reporte_clientes_prime, reporte_sla_por_repartidor,
)


# ============================================================
#  ESTADO GLOBAL
# ============================================================
clientes = []
productos = []
arbol_categorias = {}
cola_pedidos = ColaPrioridad()
hash_pedidos = TablaHash(tamano=29)
pedidos_todos = []  # incluye PENDIENTES y ENTREGADOS para reporte SLA


def inicializar_sistema():
    global clientes, productos, arbol_categorias, pedidos_todos

    clientes = cargar_clientes()
    productos = cargar_productos()
    arbol_categorias = cargar_arbol_categorias()

    pedidos_todos = cargar_pedidos_iniciales()
    pendientes = 0
    entregados = 0
    for p in pedidos_todos:
        # Solo los PENDIENTES van a la cola
        if p.estado_actual == "PENDIENTE":
            es_prime = buscar_cliente_es_prime(p.cliente_dni)
            cola_pedidos.insertar(p, es_prime)
            pendientes += 1
        else:
            entregados += 1
        hash_pedidos.insertar(p.codigo, p)

    print("Sistema inicializado correctamente.")
    print(f"  - Clientes cargados        : {len(clientes)}")
    print(f"  - Productos cargados       : {len(productos)} (en {len(SEDES)} sedes)")
    print(f"  - Pedidos en cola          : {pendientes}")
    print(f"  - Pedidos historicos       : {entregados} (para reporte SLA)")


def buscar_cliente_es_prime(dni):
    for c in clientes:
        if c.dni == dni:
            return c.es_prime
    return False


def buscar_cliente_por_dni(dni):
    for c in clientes:
        if c.dni == dni:
            return c
    return None


def buscar_producto_por_codigo(codigo):
    for p in productos:
        if p.codigo == codigo:
            return p
    return None


# ============================================================
#  OPCIONES
# ============================================================
def opcion_registrar_pedido():
    print("\n--- REGISTRO DE NUEVO PEDIDO ---")
    codigo = input("Codigo de pedido (ej: PED0099): ").strip().upper()
    if hash_pedidos.buscar(codigo) is not None:
        print("ERROR: ya existe un pedido con ese codigo.")
        return

    dni = input("DNI del cliente: ").strip()
    cliente = buscar_cliente_por_dni(dni)
    if cliente is None:
        print("ERROR: cliente no registrado en el sistema.")
        return

    distrito = input("Distrito de entrega: ").strip()
    if sede_asignada(distrito) is None:
        print(f"ERROR: el distrito '{distrito}' no esta dentro de la cobertura.")
        print(f"Distritos validos: {', '.join(listar_distritos()[:8])}...")
        return

    # Mostrar modalidades segun el distrito
    modalidades = modalidades_permitidas(distrito)
    print(f"\nDistrito {distrito}: ", end="")
    if tiene_tienda(distrito):
        print("tiene tienda Wong. Modalidades disponibles:")
    else:
        print("sin tienda. Solo delivery con recargo.")
    for i, m in enumerate(modalidades, 1):
        print(f"  {i}. {m}")
    try:
        opc_m = int(input("Modalidad: "))
        modalidad = modalidades[opc_m - 1]
    except (ValueError, IndexError):
        print("ERROR: modalidad invalida.")
        return

    print("\nCanal de origen:\n  1. APP\n  2. WEB\n  3. PRESENCIAL")
    try:
        opc_c = int(input("Canal: "))
        canal = ["APP", "WEB", "PRESENCIAL"][opc_c - 1]
    except (ValueError, IndexError):
        print("ERROR: canal invalido.")
        return

    print("\nTipo de SLA:\n  1. Express (3 horas)\n  2. Estandar (6 horas)\n  3. Programado (24 horas)")
    try:
        opc_s = int(input("SLA: "))
        sla_horas = [3, 6, 24][opc_s - 1]
    except (ValueError, IndexError):
        print("ERROR: SLA invalido.")
        return

    try:
        monto = float(input("Monto del pedido (S/): "))
    except ValueError:
        print("ERROR: monto invalido.")
        return

    productos_pedido = input("Codigos de productos separados por coma: ").strip().split(",")
    productos_pedido = [p.strip().upper() for p in productos_pedido]

    descripcion = input("Descripcion del pedido (opcional): ").strip()

    # Validar y asignar sede
    sede = sede_asignada(distrito)

    # Validar stock en la sede asignada
    faltantes = []
    for cp in productos_pedido:
        prod = buscar_producto_por_codigo(cp)
        if prod is None:
            print(f"ADVERTENCIA: producto {cp} no existe en el catalogo.")
        elif not prod.hay_stock_en(sede):
            faltantes.append(cp)
    if faltantes:
        print(f"ADVERTENCIA: sin stock en sede {sede} para: {', '.join(faltantes)}")
        print("(El pedido se registra igual; operaciones reasignara sede.)")

    recargo = calcular_recargo(distrito, modalidad)

    pedido = Pedido(codigo, dni, distrito, canal, modalidad, sla_horas,
                    monto, productos_pedido, descripcion=descripcion,
                    sede_asignada=sede, recargo_envio=recargo)
    pedido.historial = ListaEnlazada()
    pedido.historial.insertar_al_final({
        "estado": "PENDIENTE",
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "responsable": "Sistema"
    })

    cola_pedidos.insertar(pedido, cliente.es_prime)
    hash_pedidos.insertar(codigo, pedido)
    pedidos_todos.append(pedido)
    cliente.historial_compras.append(monto)

    print(f"\nPedido {codigo} registrado.")
    print(f"  Sede asignada    : {sede}")
    print(f"  Modalidad        : {modalidad}")
    print(f"  Recargo de envio : S/ {recargo:.2f}")
    print(f"  Codigo seguridad : {pedido.codigo_seguridad}")
    print(f"  Hora limite (SLA): {pedido.hora_limite_str}")


def opcion_listar_pendientes():
    print("\n--- PEDIDOS PENDIENTES (POR PRIORIDAD) ---")
    if cola_pedidos.esta_vacia():
        print("No hay pedidos en cola.")
        return
    for i, p in enumerate(cola_pedidos.listar_todos(), 1):
        marca = " PRIME" if buscar_cliente_es_prime(p.cliente_dni) else ""
        print(f"{i:3}. {p}{marca}")


def opcion_buscar_pedido():
    print("\n--- BUSCAR PEDIDO POR CODIGO ---")
    codigo = input("Codigo: ").strip().upper()
    pedido = hash_pedidos.buscar(codigo)
    if pedido is None:
        print("Pedido no encontrado.")
        return
    cliente = buscar_cliente_por_dni(pedido.cliente_dni)
    print(f"\n{pedido}")
    if cliente:
        print(f"  Cliente             : {cliente.nombre} ({'PRIME' if cliente.es_prime else 'Normal'})")
    print(f"  Sede asignada       : {pedido.sede_asignada}")
    print(f"  Productos           : {', '.join(pedido.productos)}")
    print(f"  Descripcion         : {pedido.descripcion or '(sin descripcion)'}")
    print(f"  Codigo de seguridad : {pedido.codigo_seguridad}")
    if pedido.repartidor_nombre:
        print(f"  Repartidor          : {pedido.repartidor_nombre} (DNI {pedido.repartidor_dni})")
    else:
        print(f"  Repartidor          : (no asignado)")


def opcion_actualizar_estado():
    print("\n--- ACTUALIZAR ESTADO DEL PEDIDO ---")
    codigo = input("Codigo del pedido: ").strip().upper()
    pedido = hash_pedidos.buscar(codigo)
    if pedido is None:
        print("Pedido no encontrado.")
        return

    estados = ["EN PREPARACION", "LISTO PARA DESPACHO", "EN RUTA", "ENTREGADO", "CANCELADO"]
    print("Estados disponibles:")
    for i, e in enumerate(estados, 1):
        print(f"  {i}. {e}")
    try:
        opc = int(input("Opcion: "))
        nuevo_estado = estados[opc - 1]
    except (ValueError, IndexError):
        print("Opcion invalida.")
        return

    # Si pasa a EN RUTA y no tiene repartidor, pedir asignacion
    if nuevo_estado in ("EN RUTA", "ENTREGADO") and pedido.repartidor_dni is None:
        print("\nAsignar repartidor:")
        for i, (dni, nombre) in enumerate(REPARTIDORES, 1):
            print(f"  {i}. {nombre} (DNI {dni})")
        try:
            opc_r = int(input("Repartidor: "))
            dni_r, nombre_r = REPARTIDORES[opc_r - 1]
            pedido.asignar_repartidor(dni_r, nombre_r)
            responsable = nombre_r
        except (ValueError, IndexError):
            print("Asignacion invalida.")
            return
    else:
        responsable = pedido.repartidor_nombre or input("Responsable: ").strip() or "Sistema"

    pedido.historial.insertar_al_final({
        "estado": nuevo_estado,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "responsable": responsable
    })

    if nuevo_estado == "ENTREGADO":
        pedido.marcar_entregado()
        cumplio = pedido.cumplio_sla()
        print(f"\nEstado: ENTREGADO. SLA: {'CUMPLIDO' if cumplio else 'INCUMPLIDO'}")
    else:
        pedido.estado_actual = nuevo_estado
        print(f"\nEstado actualizado a: {nuevo_estado}")


def opcion_ver_historial():
    print("\n--- HISTORIAL DE ESTADOS DE UN PEDIDO ---")
    codigo = input("Codigo del pedido: ").strip().upper()
    pedido = hash_pedidos.buscar(codigo)
    if pedido is None:
        print("Pedido no encontrado.")
        return
    print(f"\nPedido {codigo} - historial completo:")
    for i, h in enumerate(pedido.historial.recorrer(), 1):
        print(f"  {i}. [{h['fecha']}] {h['estado']:25} - {h['responsable']}")
    print(f"\nTotal de cambios de estado: {pedido.historial.longitud()}")


def opcion_metodos_recursivos():
    print("\n--- METODOS RECURSIVOS ---")
    print("1. Calcular puntos Bonus acumulados de un cliente")
    print("2. Buscar productos en una categoria (incluyendo subcategorias)")
    print("3. Calcular descuento Wong Prime escalonado (con bonus por canal)")
    opc = input("Opcion: ").strip()

    if opc == "1":
        dni = input("DNI del cliente: ").strip()
        cliente = buscar_cliente_por_dni(dni)
        if cliente is None:
            print("Cliente no encontrado.")
            return
        puntos = calcular_puntos_bonus(cliente.historial_compras)
        print(f"\nCliente: {cliente.nombre}")
        print(f"Historial de compras: {cliente.historial_compras}")
        print(f"Puntos Bonus acumulados (calculo recursivo): {puntos}")

    elif opc == "2":
        cat = input("Categoria a buscar (ej: Bebidas): ").strip()
        encontrados = buscar_en_subcategorias(productos, cat, arbol_categorias)
        if not encontrados:
            print("No se encontraron productos en esa categoria.")
            return
        print(f"\nProductos encontrados en '{cat}' y sus subcategorias:")
        for p in encontrados:
            print(f"  {p}")
        print(f"Total: {len(encontrados)} producto(s)")

    elif opc == "3":
        try:
            monto = float(input("Monto del pedido (S/): "))
        except ValueError:
            print("Monto invalido.")
            return
        print("Canal:\n  1. APP\n  2. WEB\n  3. PRESENCIAL")
        try:
            opc_c = int(input("Canal: "))
            canal = ["APP", "WEB", "PRESENCIAL"][opc_c - 1]
        except (ValueError, IndexError):
            print("Canal invalido.")
            return
        desc = calcular_descuento_prime(monto, canal)
        print(f"\nMonto original    : S/ {monto:.2f}")
        print(f"Canal             : {canal}")
        print(f"Descuento Prime   : S/ {desc:.2f}")
        print(f"Monto a pagar     : S/ {monto - desc:.2f}")
    else:
        print("Opcion invalida.")


def opcion_reportes():
    print("\n--- REPORTES OPERATIVOS ---")
    print("1. Pedidos por zona de despacho")
    print("2. Productos por categoria")
    print("3. Clientes Wong Prime activos")
    print("4. Cumplimiento de SLA por repartidor")
    opc = input("Opcion: ").strip()

    if opc == "1":
        zona = input("Distrito (o TODAS): ").strip()
        resultado = reporte_pedidos_por_zona(cola_pedidos.listar_todos(), zona)
        if not resultado:
            print("No hay pedidos para esa zona.")
            return
        print(f"\nPedidos en '{zona}' ordenados por hora limite:")
        for p in resultado:
            print(f"  {p}")

    elif opc == "2":
        cat = input("Categoria (o TODAS): ").strip()
        resultado = reporte_productos_por_categoria(productos, cat)
        if not resultado:
            print("No hay productos en esa categoria.")
            return
        print(f"\nProductos en '{cat}' ordenados por rotacion descendente:")
        for p in resultado:
            print(f"  {p}")

    elif opc == "3":
        resultado = reporte_clientes_prime(clientes)
        if not resultado:
            print("No hay clientes Prime activos.")
            return
        print("\nClientes Wong Prime ordenados por monto total descendente:")
        for c in resultado:
            puntos = calcular_puntos_bonus(c.historial_compras)
            print(f"  {c} | Puntos (recursivo): {puntos}")

    elif opc == "4":
        resultado = reporte_sla_por_repartidor(pedidos_todos)
        if not resultado:
            print("Aun no hay pedidos entregados para evaluar SLA.")
            return
        print("\nCumplimiento de SLA por repartidor (ordenado descendente):")
        print("-" * 75)
        for r in resultado:
            print(f"  {r['repartidor_nombre']:30} | "
                  f"Entregados: {r['total_entregados']:3} | "
                  f"A tiempo: {r['a_tiempo']:3} | "
                  f"Tarde: {r['tarde']:3} | "
                  f"Cumplimiento: {r['porcentaje_cumplimiento']:5.1f}%")
        print("-" * 75)
    else:
        print("Opcion invalida.")


def opcion_estadisticas_hash():
    print("\n--- ESTADISTICAS DE LA TABLA HASH ---")
    e = hash_pedidos.estadisticas()
    print(f"Elementos almacenados : {e['total_elementos']}")
    print(f"Cubetas ocupadas      : {e['cubetas_ocupadas']} de {e['total_cubetas']}")
    print(f"Colisiones registradas: {e['colisiones']}")
    factor_carga = e['total_elementos'] / e['total_cubetas']
    print(f"Factor de carga       : {factor_carga:.2f}")


def opcion_consultar_inventario():
    print("\n--- CONSULTAR INVENTARIO POR SEDE ---")
    codigo = input("Codigo del producto: ").strip().upper()
    p = buscar_producto_por_codigo(codigo)
    if p is None:
        print("Producto no encontrado.")
        return
    print(f"\n{p.nombre} (cod {p.codigo})")
    print(f"Stock total: {p.stock_total()} unidades distribuidas en {len(p.stock_por_sede)} sedes\n")
    for sede, cantidad in p.stock_por_sede.items():
        barra = "#" * cantidad
        print(f"  {sede:18} : {cantidad:3} {barra}")


# ============================================================
#  MENU PRINCIPAL
# ============================================================
def mostrar_menu():
    print("\n" + "=" * 60)
    print("  SISTEMA DE GESTION DE PEDIDOS - WONG ONLINE")
    print("=" * 60)
    print("  1. Registrar un nuevo pedido")
    print("  2. Listar pedidos pendientes (por prioridad)")
    print("  3. Buscar pedido por codigo (tabla hash)")
    print("  4. Actualizar estado de un pedido")
    print("  5. Ver historial de estados (lista enlazada)")
    print("  6. Metodos recursivos")
    print("  7. Reportes operativos (incluye reporte SLA)")
    print("  8. Estadisticas de la tabla hash")
    print("  9. Consultar inventario por sede")
    print("  0. Salir")
    print("=" * 60)


def main():
    inicializar_sistema()
    while True:
        mostrar_menu()
        opc = input("Seleccione una opcion: ").strip()
        if opc == "1": opcion_registrar_pedido()
        elif opc == "2": opcion_listar_pendientes()
        elif opc == "3": opcion_buscar_pedido()
        elif opc == "4": opcion_actualizar_estado()
        elif opc == "5": opcion_ver_historial()
        elif opc == "6": opcion_metodos_recursivos()
        elif opc == "7": opcion_reportes()
        elif opc == "8": opcion_estadisticas_hash()
        elif opc == "9": opcion_consultar_inventario()
        elif opc == "0":
            print("\nSaliendo del sistema. Hasta luego.")
            break
        else:
            print("Opcion invalida.")


if __name__ == "__main__":
    main()
