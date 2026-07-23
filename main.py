# ============================================================
# Fase 4 - Programacion
# Sistema Integral de Gestion de Clientes, Servicios y Reservas
# Empresa: Software FJ
# Autor: WILMAR FUENTES
# Grupo: 1
# Curso: Programacion - UNAD
# ============================================================

from abc import ABC, abstractmethod
from datetime import datetime
import logging


# ============================================================
# CONFIGURACION DEL ARCHIVO DE LOGS
# ============================================================

logging.basicConfig(
    filename="eventos.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


# ============================================================
# EXCEPCIONES PERSONALIZADAS
# ============================================================

class ErrorSistema(Exception):
    """Excepcion general del sistema."""
    pass


class ErrorCliente(ErrorSistema):
    """Excepcion para errores relacionados con clientes."""
    pass


class ErrorServicio(ErrorSistema):
    """Excepcion para errores relacionados con servicios."""
    pass


class ErrorReserva(ErrorSistema):
    """Excepcion para errores relacionados con reservas."""
    pass


# ============================================================
# CLASE ABSTRACTA GENERAL
# ============================================================

class EntidadSistema(ABC):
    """Clase abstracta general para las entidades del sistema."""

    def __init__(self, codigo):
        if not codigo:
            raise ErrorSistema("El codigo de la entidad no puede estar vacio.")
        self._codigo = codigo

    @property
    def codigo(self):
        return self._codigo

    @abstractmethod
    def mostrar_info(self):
        pass


# ============================================================
# CLASE CLIENTE
# ============================================================

class Cliente(EntidadSistema):
    """Clase que representa un cliente del sistema."""

    def __init__(self, codigo, nombre, documento, correo):
        super().__init__(codigo)
        self.__nombre = None
        self.__documento = None
        self.__correo = None

        self.nombre = nombre
        self.documento = documento
        self.correo = correo

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or len(valor.strip()) < 3:
            raise ErrorCliente("El nombre del cliente debe tener minimo 3 caracteres.")
        self.__nombre = valor.strip()

    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        if not str(valor).isdigit() or len(str(valor)) < 6:
            raise ErrorCliente("El documento debe ser numerico y tener minimo 6 digitos.")
        self.__documento = str(valor)

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if "@" not in valor or "." not in valor:
            raise ErrorCliente("El correo electronico no tiene un formato valido.")
        self.__correo = valor.strip()

    def mostrar_info(self):
        return f"Cliente: {self.__nombre} | Documento: {self.__documento} | Correo: {self.__correo}"


# ============================================================
# CLASE ABSTRACTA SERVICIO
# ============================================================

class Servicio(EntidadSistema):
    """Clase abstracta para representar un servicio de Software FJ."""

    def __init__(self, codigo, nombre, precio_base, disponible=True):
        super().__init__(codigo)

        if not nombre or len(nombre.strip()) < 3:
            raise ErrorServicio("El nombre del servicio debe tener minimo 3 caracteres.")

        if precio_base <= 0:
            raise ErrorServicio("El precio base del servicio debe ser mayor que cero.")

        self._nombre = nombre.strip()
        self._precio_base = precio_base
        self._disponible = disponible

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, estado):
        self._disponible = estado

    @abstractmethod
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        pass

    @abstractmethod
    def validar_parametros(self, duracion):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass

    def mostrar_info(self):
        estado = "Disponible" if self._disponible else "No disponible"
        return f"Servicio: {self._nombre} | Precio base: ${self._precio_base} | Estado: {estado}"


# ============================================================
# SERVICIOS ESPECIALIZADOS
# ============================================================

class ReservaSala(Servicio):
    """Servicio para reserva de salas."""

    def __init__(self, codigo, nombre, precio_base, capacidad, disponible=True):
        super().__init__(codigo, nombre, precio_base, disponible)
        if capacidad <= 0:
            raise ErrorServicio("La capacidad de la sala debe ser mayor que cero.")
        self.capacidad = capacidad

    def validar_parametros(self, duracion):
        if duracion <= 0:
            raise ErrorServicio("La duracion de la reserva de sala debe ser mayor que cero.")
        if duracion > 8:
            raise ErrorServicio("La sala no se puede reservar por mas de 8 horas.")

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self.validar_parametros(duracion)
        subtotal = self._precio_base * duracion
        subtotal -= subtotal * descuento
        total = subtotal + (subtotal * impuesto)
        return total

    def describir_servicio(self):
        return f"Reserva de sala con capacidad para {self.capacidad} personas."


class AlquilerEquipo(Servicio):
    """Servicio para alquiler de equipos tecnologicos."""

    def __init__(self, codigo, nombre, precio_base, tipo_equipo, disponible=True):
        super().__init__(codigo, nombre, precio_base, disponible)
        if not tipo_equipo:
            raise ErrorServicio("Debe indicar el tipo de equipo.")
        self.tipo_equipo = tipo_equipo

    def validar_parametros(self, duracion):
        if duracion <= 0:
            raise ErrorServicio("La duracion del alquiler debe ser mayor que cero.")
        if duracion > 15:
            raise ErrorServicio("El equipo no se puede alquilar por mas de 15 dias.")

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self.validar_parametros(duracion)
        subtotal = self._precio_base * duracion
        subtotal -= subtotal * descuento
        total = subtotal + (subtotal * impuesto)
        return total

    def describir_servicio(self):
        return f"Alquiler de equipo tipo {self.tipo_equipo}."


class AsesoriaEspecializada(Servicio):
    """Servicio para asesorias especializadas."""

    def __init__(self, codigo, nombre, precio_base, area, disponible=True):
        super().__init__(codigo, nombre, precio_base, disponible)
        if not area:
            raise ErrorServicio("Debe indicar el area de la asesoria.")
        self.area = area

    def validar_parametros(self, duracion):
        if duracion <= 0:
            raise ErrorServicio("La duracion de la asesoria debe ser mayor que cero.")
        if duracion > 6:
            raise ErrorServicio("La asesoria no puede durar mas de 6 horas.")

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self.validar_parametros(duracion)
        subtotal = self._precio_base * duracion
        subtotal -= subtotal * descuento
        total = subtotal + (subtotal * impuesto)
        return total

    def describir_servicio(self):
        return f"Asesoria especializada en el area de {self.area}."


# ============================================================
# CLASE RESERVA
# ============================================================

class Reserva(EntidadSistema):
    """Clase que integra un cliente con un servicio."""

    def __init__(self, codigo, cliente, servicio, duracion):
        super().__init__(codigo)

        if not isinstance(cliente, Cliente):
            raise ErrorReserva("El cliente asignado no es valido.")

        if not isinstance(servicio, Servicio):
            raise ErrorReserva("El servicio asignado no es valido.")

        if duracion <= 0:
            raise ErrorReserva("La duracion de la reserva debe ser mayor que cero.")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"
        self.fecha_creacion = datetime.now()

    def confirmar(self):
        try:
            if not self.servicio.disponible:
                raise ErrorReserva("No se puede confirmar la reserva porque el servicio no esta disponible.")

            self.servicio.validar_parametros(self.duracion)
            self.estado = "Confirmada"
            logging.info(f"Reserva confirmada: {self.codigo}")
            return "Reserva confirmada correctamente."

        except ErrorServicio as error:
            logging.error(f"Error al validar servicio en reserva {self.codigo}: {error}")
            raise ErrorReserva("No fue posible confirmar la reserva por un error en el servicio.") from error

        finally:
            logging.info(f"Finalizo el intento de confirmacion de la reserva {self.codigo}")

    def cancelar(self):
        if self.estado == "Cancelada":
            raise ErrorReserva("La reserva ya se encuentra cancelada.")
        self.estado = "Cancelada"
        logging.info(f"Reserva cancelada: {self.codigo}")
        return "Reserva cancelada correctamente."

    def procesar_pago(self, descuento=0, impuesto=0.19):
        try:
            if self.estado != "Confirmada":
                raise ErrorReserva("Solo se puede procesar el pago de una reserva confirmada.")

            total = self.servicio.calcular_costo(self.duracion, descuento, impuesto)

        except ErrorReserva as error:
            logging.error(f"Error de reserva al procesar pago {self.codigo}: {error}")
            return f"Error: {error}"

        except ErrorServicio as error:
            logging.error(f"Error de servicio al procesar pago {self.codigo}: {error}")
            return f"Error: {error}"

        else:
            logging.info(f"Pago procesado para reserva {self.codigo}. Total: {total}")
            return f"Pago procesado. Total a pagar: ${total:,.2f}"

        finally:
            logging.info(f"Finalizo el proceso de pago de la reserva {self.codigo}")

    def mostrar_info(self):
        return (
            f"Reserva: {self.codigo} | Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio._nombre} | Duracion: {self.duracion} | Estado: {self.estado}"
        )


# ============================================================
# FUNCION AUXILIAR PARA EJECUTAR OPERACIONES SIN DETENER EL SISTEMA
# ============================================================

def ejecutar_operacion(numero, descripcion, funcion):
    print("\n" + "=" * 70)
    print(f"OPERACION {numero}: {descripcion}")
    print("=" * 70)

    try:
        resultado = funcion()

    except ErrorSistema as error:
        print(f"Error controlado: {error}")
        logging.error(f"Operacion {numero} fallida: {descripcion}. Error: {error}")

    except Exception as error:
        print(f"Error inesperado controlado: {error}")
        logging.exception(f"Operacion {numero} genero un error inesperado.")

    else:
        if resultado is not None:
            print(resultado)
        logging.info(f"Operacion {numero} ejecutada correctamente: {descripcion}")

    finally:
        print("Operacion finalizada. El sistema continua funcionando.")


# ============================================================
# SIMULACION PRINCIPAL DEL SISTEMA
# ============================================================

clientes = []
servicios = []
reservas = []


def operacion_1_cliente_valido():
    cliente = Cliente("C001", "Carlos Martinez", "1020304050", "carlos@mail.com")
    clientes.append(cliente)
    return cliente.mostrar_info()


def operacion_2_cliente_invalido_nombre():
    cliente = Cliente("C002", "Lu", "102030", "lu@mail.com")
    clientes.append(cliente)
    return cliente.mostrar_info()


def operacion_3_cliente_invalido_correo():
    cliente = Cliente("C003", "Ana Gomez", "123456789", "anagomezcorreo")
    clientes.append(cliente)
    return cliente.mostrar_info()


def operacion_4_servicio_sala_valido():
    servicio = ReservaSala("S001", "Sala de reuniones", 50000, 20)
    servicios.append(servicio)
    return servicio.mostrar_info() + "\n" + servicio.describir_servicio()


def operacion_5_servicio_equipo_valido():
    servicio = AlquilerEquipo("S002", "Alquiler de portatil", 70000, "Computador portatil")
    servicios.append(servicio)
    return servicio.mostrar_info() + "\n" + servicio.describir_servicio()


def operacion_6_servicio_invalido_precio():
    servicio = AsesoriaEspecializada("S003", "Asesoria en software", -80000, "Desarrollo")
    servicios.append(servicio)
    return servicio.mostrar_info()


def operacion_7_reserva_exitosa():
    cliente = clientes[0]
    servicio = servicios[0]
    reserva = Reserva("R001", cliente, servicio, 3)
    reservas.append(reserva)
    mensaje = reserva.confirmar()
    pago = reserva.procesar_pago(descuento=0.10, impuesto=0.19)
    return reserva.mostrar_info() + "\n" + mensaje + "\n" + pago


def operacion_8_reserva_duracion_invalida():
    cliente = clientes[0]
    servicio = servicios[0]
    reserva = Reserva("R002", cliente, servicio, 12)
    reservas.append(reserva)
    return reserva.confirmar()


def operacion_9_servicio_no_disponible():
    cliente = clientes[0]
    servicio = servicios[1]
    servicio.cambiar_disponibilidad(False)
    reserva = Reserva("R003", cliente, servicio, 2)
    reservas.append(reserva)
    return reserva.confirmar()


def operacion_10_pago_sin_confirmar():
    cliente = clientes[0]
    servicio = servicios[0]
    reserva = Reserva("R004", cliente, servicio, 2)
    reservas.append(reserva)
    return reserva.procesar_pago()


def operacion_11_cancelacion_exitosa():
    reserva = reservas[0]
    mensaje = reserva.cancelar()
    return reserva.mostrar_info() + "\n" + mensaje


def operacion_12_cancelacion_repetida():
    reserva = reservas[0]
    mensaje = reserva.cancelar()
    return reserva.mostrar_info() + "\n" + mensaje


if __name__ == "__main__":
    print("SISTEMA INTEGRAL DE GESTION DE CLIENTES, SERVICIOS Y RESERVAS")
    print("Empresa: Software FJ")
    print("Inicio de simulaciones del sistema")

    logging.info("Inicio de ejecucion del sistema Software FJ")

    ejecutar_operacion(1, "Registro valido de cliente", operacion_1_cliente_valido)
    ejecutar_operacion(2, "Registro invalido de cliente por nombre corto", operacion_2_cliente_invalido_nombre)
    ejecutar_operacion(3, "Registro invalido de cliente por correo incorrecto", operacion_3_cliente_invalido_correo)
    ejecutar_operacion(4, "Creacion valida de servicio de reserva de sala", operacion_4_servicio_sala_valido)
    ejecutar_operacion(5, "Creacion valida de servicio de alquiler de equipo", operacion_5_servicio_equipo_valido)
    ejecutar_operacion(6, "Creacion invalida de servicio por precio negativo", operacion_6_servicio_invalido_precio)
    ejecutar_operacion(7, "Reserva exitosa con pago procesado", operacion_7_reserva_exitosa)
    ejecutar_operacion(8, "Reserva fallida por duracion invalida", operacion_8_reserva_duracion_invalida)
    ejecutar_operacion(9, "Reserva fallida por servicio no disponible", operacion_9_servicio_no_disponible)
    ejecutar_operacion(10, "Pago fallido por reserva sin confirmar", operacion_10_pago_sin_confirmar)
    ejecutar_operacion(11, "Cancelacion exitosa de reserva", operacion_11_cancelacion_exitosa)
    ejecutar_operacion(12, "Cancelacion repetida de reserva", operacion_12_cancelacion_repetida)

    logging.info("Fin de ejecucion del sistema Software FJ")

    print("\n" + "=" * 70)
    print("SIMULACION FINALIZADA")
    print("Revise el archivo eventos.log para ver el registro de eventos y errores.")
    print("=" * 70)
