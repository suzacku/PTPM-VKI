import unittest
from lb2.Delivery import calculate_delivery_cost


class TestDelivery(unittest.TestCase):

    def test_weight_too_small(self):
        result = calculate_delivery_cost(0.05, 100, "обычный")
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_weight_too_big(self):
        result = calculate_delivery_cost(50.1, 100, "обычный")
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_distance_too_small(self):
        result = calculate_delivery_cost(1.0, 0, "обычный")
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_distance_too_big(self):
        result = calculate_delivery_cost(1.0, 5001, "обычный")
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_bad_type(self):
        result = calculate_delivery_cost(1.0, 100, "стандартный")
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_small_package(self):
        result = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertEqual(result, (700, "2026-09-04"))

    def test_medium_weight(self):
        result = calculate_delivery_cost(10.0, 100, "обычный")
        self.assertEqual(result, (840, "2026-09-04"))

    def test_heavy_weight(self):
        result = calculate_delivery_cost(20.0, 100, "обычный")
        self.assertEqual(result, (1050, "2026-09-04"))

    def test_fragile_package(self):
        result = calculate_delivery_cost(1.0, 100, "хрупкий")
        self.assertEqual(result, (1000, "2026-09-04"))

    def test_hazardous_package(self):
        result = calculate_delivery_cost(1.0, 100, "опасный")
        self.assertEqual(result, (1700, "2026-09-04"))

    def test_weight_exactly_5kg(self):
        result = calculate_delivery_cost(5.0, 100, "обычный")
        self.assertEqual(result, (700, "2026-09-04"))


if __name__ == "__main__":
    unittest.main()