"""
pedido.py
Define la clase Pedido. Cada pedido tiene:
  - Datos del cliente y la entrega
  - Canal de origen (APP, WEB, PRESENCIAL) para descuento diferenciado
  - SLA configurable: hora_limite = hora_confirmacion + sla_horas
  - Modalidad: DELIVERY o RETIRO_EN_TIENDA segun el distrito
  - Sede asignada para preparar el pedido
  - Datos del repartidor cuando aplica
  - Codigo de seguridad para validar la entrega
  - Historial de estados como lista enlazada
"""

from datetime import datetime, timedelta
import random


def generar_codigo_seguridad():
    """Genera un codigo de 4 digitos para validar la entrega."""
    return f"{random.randint(0, 9999):04d}"


class Pedido:
    def __init__(self, codigo, cliente_dni, distrito, canal, modalidad,
                 sla_horas, monto, productos,
                 descripcion="", hora_confirmacion=None,
                 sede_asignada="", recargo_envio=0.0):
        self.codigo = codigo
        self.cliente_dni = cliente_dni
        self.distrito = distrito
        self.canal = canal  # "APP", "WEB", "PRESENCIAL"
        self.modalidad = modalidad  # "DELIVERY", "RETIRO_EN_TIENDA"
        self.sla_horas = sla_horas
        self.monto = monto
        self.productos = productos  # lista de codigos de producto
        self.descripcion = descripcion
        self.hora_confirmacion = hora_confirmacion or datetime.now()
        self.sede_asignada = sede_asignada
        self.recargo_envio = recargo_envio

        # Generados automaticamente
        self.codigo_seguridad = generar_codigo_seguridad()
        self.repartidor_dni = None
        self.repartidor_nombre = None
        self.hora_entregado = None

        # Historial (se asigna como ListaEnlazada desde main)
        self.historial = None
        self.estado_actual = "PENDIENTE"

    @property
    def hora_limite(self):
        """Hora limite calculada como confirmacion + SLA."""
        return self.hora_confirmacion + timedelta(hours=self.sla_horas)

    @property
    def hora_limite_str(self):
        """Hora limite como string HH:MM para mostrar."""
        return self.hora_limite.strftime("%H:%M")

    def asignar_repartidor(self, dni, nombre):
        """Asigna un repartidor al pedido."""
        self.repartidor_dni = dni
        self.repartidor_nombre = nombre

    def marcar_entregado(self, fecha_entrega=None):
        """Registra la hora real de entrega."""
        self.hora_entregado = fecha_entrega or datetime.now()
        self.estado_actual = "ENTREGADO"

    def cumplio_sla(self):
        """
        Devuelve True si el pedido se entrego dentro del SLA pactado.
        Si aun no esta entregado, devuelve None.
        """
        if self.hora_entregado is None:
            return None
        return self.hora_entregado <= self.hora_limite

    def monto_total(self):
        """Monto + recargo de envio."""
        return self.monto + self.recargo_envio

    def __str__(self):
        return (f"[{self.codigo}] DNI {self.cliente_dni} | "
                f"{self.distrito} | {self.modalidad} | Canal: {self.canal} | "
                f"SLA: {self.sla_horas}h (limite {self.hora_limite_str}) | "
                f"S/ {self.monto_total():.2f} | Estado: {self.estado_actual}")
