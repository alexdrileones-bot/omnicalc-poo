import unittest
from modelos import ConversionDatos, ConversionTemperatura, CalculoSubredIP
from servicios import CalculadoraServicio


class TestOmniCalc(unittest.TestCase):
    def setUp(self):
        self.servicio = CalculadoraServicio()

    def test_conversion_datos_binaria(self):
        op = ConversionDatos("GB", "MB")
        res = self.servicio.procesar(op, "2")
        self.assertEqual(res, "2,048 MB")

    def test_conversion_datos_negativa_lanza_error(self):
        op = ConversionDatos("MB", "KB")
        with self.assertRaises(ValueError):
            self.servicio.procesar(op, "-50")

    def test_conversion_temperatura_valida(self):
        op = ConversionTemperatura("Celsius", "Fahrenheit")
        res = self.servicio.procesar(op, "100")
        self.assertEqual(res, "212.00 °F")

    def test_temperatura_bajo_cero_absoluto(self):
        op = ConversionTemperatura("Celsius", "Kelvin")
        with self.assertRaises(ValueError):
            self.servicio.procesar(op, "-300")

    def test_calculo_subred_ipv4(self):
        op = CalculoSubredIP()
        res = self.servicio.procesar(op, "192.168.1.50/24")
        self.assertIn("Red: 192.168.1.0", res)
        self.assertIn("Hosts útiles: 254", res)

    def test_historial_lifo_deshacer(self):
        self.servicio.procesar(ConversionDatos("KB", "Bytes"), "1")
        self.servicio.procesar(ConversionTemperatura("Celsius", "Kelvin"), "0")
        self.assertEqual(len(self.servicio.obtener_historial()), 2)
        self.servicio.deshacer_ultimo()
        self.assertEqual(len(self.servicio.obtener_historial()), 1)


if __name__ == "__main__":
    unittest.main()