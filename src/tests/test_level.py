import unittest
from pygame.math import Vector2
from model import Level

class TestLevel(unittest.TestCase):
    def setUp(self):
        self.level = Level("Test Level")

    def test_cellWidth(self):
        self.assertEqual(self.level.cellWidth, 64)

    def test_cellHeight(self):
        self.assertEqual(self.level.cellHeight, 64)

    def test_str(self):
        expected_str = self.level.name+" "+str(self.level.ground)+" "+str(self.level.walls)+" "+str(self.level.units)+" "+str(self.level.cellSize)+" "+str(self.level.gameOver)
        self.assertEqual(str(self.level), expected_str)

if __name__ == '__main__':
    unittest.main()