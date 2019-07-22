import unittest

from uuid import UUID

from ride import (
    GeometricSurface,
)
from .utils import generate_positions


class TestSurfaces(unittest.TestCase):

    def test_geometric_surface(self):
        positions = generate_positions(100)
        n = len(positions)
        surface = GeometricSurface(positions=positions)
        self.assertIsInstance(surface.uuid, UUID)
        self.assertEqual(n, len(surface.positions))

    def test_distance(self):
        positions = generate_positions(2)
        surface = GeometricSurface(positions=positions)

        a, b = tuple(positions)
        real_dist = ((a.lat - b.lat) ** 2 + (a.lon - b.lon) ** 2) ** 0.5

        dist = surface.distance(a, b)
        self.assertAlmostEqual(dist, real_dist)


if __name__ == '__main__':
    unittest.main()
