from modelos import OperacionConversion, RegistroOperacion


class CalculadoraServicio:
    """Orquesta la ejecución polimórfica de operaciones y administra el historial."""

    __MAX_HISTORIAL = 15

    def __init__(self):
        self.__historial: list[RegistroOperacion] = []

    def procesar(self, operacion: OperacionConversion, dato_entrada: str) -> str:
        """Aplica cualquier subclase de OperacionConversion mediante polimorfismo."""
        resultado = operacion.ejecutar(dato_entrada)
        entrada_formateada = f"{dato_entrada.strip()} ({operacion.unidad_origen})"
        registro = RegistroOperacion(operacion.nombre, entrada_formateada, resultado)

        if len(self.__historial) >= self.__MAX_HISTORIAL:
            self.__historial.pop(0)
        self.__historial.append(registro)
        return resultado

    def obtener_historial(self) -> list[str]:
        """Devuelve el historial ordenado del más reciente al más antiguo."""
        return [item.resumen for item in reversed(self.__historial)]

    def deshacer_ultimo(self) -> bool:
        """Elimina el último cálculo de la pila (LIFO)."""
        if not self.__historial:
            return False
        self.__historial.pop()
        return True

    def limpiar_historial(self) -> None:
        self.__historial.clear()