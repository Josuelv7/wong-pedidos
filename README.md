# Sistema de Gestión de Pedidos WongOnline (v2)

**Curso:** IS207 — Estructura de Datos y Algoritmos | **Ciclo:** 2026-15 | **UPC**

**Integrantes:**
- Leyva Flores, Josué Valentín
- Yparraguirre Bravo, Ismael Jesús
- Crovetto Caballero, Omar
- Aliaga Vadillo, Cheryld Fabiola

---

## Cómo ejecutar

```bash
python3 main.py
```

No requiere instalar librerías. Solo Python 3.

---

## Estructura del proyecto

| Archivo | Contenido |
|---|---|
| `main.py` | Menú principal y flujo del programa (9 opciones) |
| `pedido.py` | Clase Pedido con SLA, canal, modalidad, repartidor, código de seguridad |
| `cliente.py` | Clase Cliente con membresía Prime y puntos Bonus |
| `producto.py` | Clase Producto con stock distribuido por sede |
| `geografia.py` | Distritos con/sin tienda, asignación de sede, cálculo de recargos |
| `cola_prioridad.py` | Cola de prioridad (manual, sin heapq) |
| `tabla_hash.py` | Tabla hash con encadenamiento |
| `lista_enlazada.py` | Lista enlazada simple para historial |
| `ordenamiento.py` | Tres métodos: burbuja, selección, inserción |
| `recursivos.py` | Tres métodos recursivos (incluye bonus por canal) |
| `reportes.py` | Cuatro reportes operativos (incluye SLA por repartidor) |
| `datos_iniciales.py` | Datos de prueba (6 clientes, 15 productos × 8 sedes, 12 pedidos) |

---

## Cobertura del syllabus

### Estructuras de datos
- **Cola de prioridad** → pedidos ordenados por hora límite calculada (`hora_confirmacion + sla_horas`) + Wong Prime al desempate
- **Tabla hash** → búsqueda de pedidos por código en O(1) promedio
- **Lista enlazada** → historial de 5 estados por pedido (PENDIENTE → EN PREPARACIÓN → LISTO PARA DESPACHO → EN RUTA → ENTREGADO)
- **Arreglos** → catálogo de productos, clientes, reportes

### Tres métodos de ordenamiento
1. **Burbuja** → pedidos por hora límite (SLA)
2. **Selección** → productos por rotación descendente
3. **Inserción** → clientes por monto total descendente

### Tres métodos recursivos
1. **Cálculo de puntos Bonus** acumulados del historial de compras
2. **Búsqueda en subcategorías** recorriendo el árbol del catálogo
3. **Descuento Wong Prime escalonado** con bonus por canal (APP +2pp, WEB +1pp, PRESENCIAL +0pp)

### Cuatro reportes con búsqueda
1. Pedidos pendientes por distrito de despacho
2. Productos del catálogo filtrados por categoría
3. Clientes Wong Prime activos ordenados por monto
4. **Cumplimiento de SLA por repartidor** (mide ineficiencia vs falta de personal)

---

## Reglas de negocio implementadas

### Lógica geográfica
- **Distritos con tienda Wong** (Miraflores, San Isidro, Surco, La Molina, San Borja, Lince, Surquillo, Trujillo): el cliente elige entre **DELIVERY** o **RETIRO_EN_TIENDA**
- **Distritos sin tienda Wong** (Rímac, Comas, San Juan de Lurigancho, Chorrillos, Ate, etc.): solo **DELIVERY** con **recargo de S/ 8.50**
- El sistema **asigna automáticamente la sede** que atenderá cada pedido

### SLA configurable
- **Express:** 3 horas (típico para pedidos APP)
- **Estándar:** 6 horas
- **Programado:** 24 horas
- La hora límite se calcula automáticamente: `hora_confirmacion + sla_horas`
- Cada pedido entregado registra si **cumplió o incumplió** el SLA

### Descuento Wong Prime con bonus por canal
| Tramo | Base | APP (+2pp) | WEB (+1pp) | PRESENCIAL |
|---|---|---|---|---|
| Hasta S/ 100 | 5% | 7% | 6% | 5% |
| S/ 100-300 | 8% | 10% | 9% | 8% |
| S/ 300-500 | 12% | 14% | 13% | 12% |
| Mayor a S/ 500 | 15% | 17% | 16% | 15% |

### Datos del pedido
- Código único, cliente, distrito, canal (APP/WEB/PRESENCIAL)
- Modalidad (DELIVERY/RETIRO_EN_TIENDA)
- SLA en horas
- **Código de seguridad de 4 dígitos** para validar la entrega
- Descripción del pedido
- Datos del repartidor (DNI + nombre) cuando se asigna
- Sede asignada automáticamente

---

## Flujo de prueba sugerido para la sustentación

1. **Opción 2** → mostrar pedidos priorizados por hora límite calculada (Prime express primero)
2. **Opción 9** → consultar inventario distribuido en 8 sedes
3. **Opción 1** → registrar un pedido en Rímac (sin tienda) y mostrar que se fuerza delivery con recargo
4. **Opción 1** → registrar un pedido en Miraflores y mostrar las dos opciones
5. **Opción 3** → buscar PED0005 por hash (búsqueda inmediata)
6. **Opción 4** → asignar repartidor y actualizar a EN RUTA → ENTREGADO
7. **Opción 5** → mostrar historial enlazado completo del pedido entregado
8. **Opción 6.3** → comparar descuento Prime para los 3 canales con un mismo monto
9. **Opción 7.4** → reporte de cumplimiento SLA por repartidor (diagnóstico operativo)
10. **Opción 8** → estadísticas de la tabla hash
