from abc import ABC, abstractmethod
from datetime import datetime
import ipaddress


class OperacionConversion(ABC):
    """Clase base abstracta que define el contrato polimórfico de cualquier conversión."""

    def __init__(self, nombre: str, unidad_origen: str, unidad_destino: str):
        self._nombre = nombre
        self._unidad_origen = unidad_origen
        self._unidad_destino = unidad_destino

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def unidad_origen(self) -> str:
        return self._unidad_origen

    @property
    def unidad_destino(self) -> str:
        return self._unidad_destino

    @abstractmethod
    def ejecutar(self, dato: str) -> str:
        """Ejecuta el cálculo o conversión y devuelve el resultado formateado."""
        pass


class ConversionDatos(OperacionConversion):
    """Convierte unidades de almacenamiento digital en base binaria (1024)."""

    __FACTORES_A_BITS = {
        "Bits": 1,
        "Bytes": 8,
        "KB": 8 * 1024,
        "MB": 8 * (1024 ** 2),
        "GB": 8 * (1024 ** 3),
        "TB": 8 * (1024 ** 4),
    }

    def __init__(self, unidad_origen: str, unidad_destino: str):
        if unidad_origen not in self.__FACTORES_A_BITS or unidad_destino not in self.__FACTORES_A_BITS:
            raise ValueError("Unidad de almacenamiento no soportada.")
        super().__init__("Almacenamiento Digital", unidad_origen, unidad_destino)

    def ejecutar(self, dato: str) -> str:
        try:
            valor = float(dato)
        except ValueError:
            raise ValueError("Debe ingresar un valor numérico válido.")

        if valor < 0:
            raise ValueError("El tamaño de datos no puede ser negativo.")

        en_bits = valor * self.__FACTORES_A_BITS[self._unidad_origen]
        resultado = en_bits / self.__FACTORES_A_BITS[self._unidad_destino]
        return f"{resultado:,.6g} {self._unidad_destino}"


class ConversionTemperatura(OperacionConversion):
    """Convierte escalas térmicas validando el límite físico del cero absoluto."""

    __UNIDADES_VALIDAS = ("Celsius", "Fahrenheit", "Kelvin")

    def __init__(self, unidad_origen: str, unidad_destino: str):
        if unidad_origen not in self.__UNIDADES_VALIDAS or unidad_destino not in self.__UNIDADES_VALIDAS:
            raise ValueError("Escala de temperatura no soportada.")
        super().__init__("Temperatura", unidad_origen, unidad_destino)

    def ejecutar(self, dato: str) -> str:
        try:
            valor = float(dato)
        except ValueError:
            raise ValueError("Debe ingresar una temperatura numérica.")

        # Convertir primero a Celsius y validar cero absoluto (-273.15 °C)
        if self._unidad_origen == "Celsius":
            celsius = valor
        elif self._unidad_origen == "Fahrenheit":
            celsius = (valor - 32) * 5 / 9
        else:
            celsius = valor - 273.15

        if celsius < -273.15 - 1e-9:
            raise ValueError("Temperatura inválida: no puede ser inferior al cero absoluto (-273.15 °C).")

        if self._unidad_destino == "Celsius":
            final = celsius
        elif self._unidad_destino == "Fahrenheit":
            final = (celsius * 9 / 5) + 32
        else:
            final = celsius + 273.15

        simbolo = {"Celsius": "°C", "Fahrenheit": "°F", "Kelvin": "K"}[self._unidad_destino]
        return f"{final:.2f} {simbolo}"


class CalculoSubredIP(OperacionConversion):
    """Calcula parámetros de red IPv4 a partir de una dirección en formato CIDR."""

    def __init__(self):
        super().__init__("Análisis de Subred IPv4", "IPv4/CIDR", "Parámetros de Red")

    def ejecutar(self, dato: str) -> str:
        texto = dato.strip()
        if not texto or "/" not in texto:
            raise ValueError("Ingrese una IP con máscara CIDR (ejemplo: 192.168.1.10/24).")
        try:
            red = ipaddress.IPv4Network(texto, strict=False)
        except ValueError:
            raise ValueError("Dirección IPv4 o prefijo de red inválido.")

        hosts_utiles = max(red.num_addresses - 2, 0) if red.prefixlen < 31 else red.num_addresses
        return (
            f"Red: {red.network_address} | Máscara: {red.netmask} | "
            f"Broadcast: {red.broadcast_address} | Hosts útiles: {hosts_utiles}"
        )


class RegistroOperacion:
    """Representa un elemento inmutable dentro del historial de operaciones."""

    def __init__(self, categoria: str, entrada: str, salida: str):
        self.__hora = datetime.now().strftime("%H:%M:%S")
        self.__categoria = categoria
        self.__entrada = entrada
        self.__salida = salida

    @property
    def resumen(self) -> str:
        return f"[{self.__hora}] {self.__categoria}: {self.__entrada}  →  {self.__salida}"