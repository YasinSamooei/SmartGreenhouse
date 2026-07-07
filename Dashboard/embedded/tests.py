from django.test import TestCase

from embedded.models import SensorData


class SensorDataModelTest(TestCase):
    def test_sensor_data_can_store_expected_fields(self):
        sensor_data = SensorData.objects.create(
            temperature=25.1,
            humidity=36.1,
            soil=9.0,
            gas=49.0,
            ldr=2730.0,
            fan=False,
            pump=True,
            heater=False,
            alarm=True,
            light=False,
        )

        self.assertEqual(sensor_data.temperature, 25.1)
        self.assertEqual(sensor_data.humidity, 36.1)
        self.assertEqual(sensor_data.soil, 9.0)
        self.assertEqual(sensor_data.gas, 49.0)
        self.assertEqual(sensor_data.ldr, 2730.0)
        self.assertFalse(sensor_data.fan)
        self.assertTrue(sensor_data.pump)
        self.assertFalse(sensor_data.heater)
        self.assertTrue(sensor_data.alarm)
        self.assertFalse(sensor_data.light)
