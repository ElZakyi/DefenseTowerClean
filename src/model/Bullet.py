from .GameItem import GameItem

from pygame.math import Vector2

class Bullet(GameItem):
    def __init__(self,unit):
        super().__init__(unit.position,Vector2(2,1))
        self.unit = unit
        self.startPosition = unit.position
        self.endPosition = unit.weaponTarget


class FactoryBullet:
    def __init__(self):
        pass

    def create(self,unit):
        return Bullet(unit)