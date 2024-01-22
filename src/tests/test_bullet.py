import unittest
from pygame.math import Vector2
from model import Bullet, GameItem

class TestBullet(unittest.TestCase):
    def setUp(self):
        self.unit = GameItem(Vector2(0, 0), Vector2(1, 1))
        self.unit.weaponTarget = Vector2(2, 1)
        self.unit.position = Vector2(0, 0)
        self.bullet = Bullet(self.unit)

    def test_init(self):
        self.assertEqual(self.bullet.position, self.unit.position)
        self.assertEqual(self.bullet.unit, self.unit)
        self.assertEqual(self.bullet.startPosition, self.unit.position)
        self.assertEqual(self.bullet.endPosition, self.unit.weaponTarget)

if __name__ == '__main__':
    unittest.main()