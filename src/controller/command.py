from pygame.math import Vector2
from model import Unit,Bullet

class Command():
    def run(self):
        raise NotImplementedError()
        
class MoveCommand(Command):
    """
    This command moves a unit in a given direction
    """
    def __init__(self,state,unit,moveVector):
        self.state = state
        self.unit = unit
        self.moveVector = moveVector
    def run(self):
        unit = self.unit
        
        # Destroyed units can't move
        if unit.status != "alive":
            return

        # Update unit orientation
        if self.moveVector.x < 0: 
            unit.orientation = 90
        elif self.moveVector.x > 0: 
            unit.orientation = -90
        if self.moveVector.y < 0: 
            unit.orientation = 0
        elif self.moveVector.y > 0: 
            unit.orientation = 180
        
        # Compute new tank position
        newPos = unit.position + self.moveVector

        # Don't allow positions outside the world
        if not self.state.isInside(newPos):
            return

        # Don't allow wall positions
        if not self.state.walls[int(newPos.y)][int(newPos.x)] is None:
            return

        # Don't allow other unit positions 
        unitIndex = self.state.findUnit(newPos)
        if not unitIndex is None:
                return

        unit.position = newPos
        
class TargetCommand(Command):
    def __init__(self,state,unit,target):
        self.state = state
        self.unit = unit
        self.target = target
    def run(self):
        self.unit.weaponTarget = self.target
        
class ShootCommand(Command):
    def __init__(self,state,unit):
        self.state = state
        self.unit = unit
    def run(self):
        if self.unit.status != "alive":
            return
        if self.state.epoch-self.unit.lastBulletEpoch < self.state.bulletDelay:
            return
        self.unit.lastBulletEpoch = self.state.epoch
        self.state.bullets.append(Bullet(self.state,self.unit))
        
class MoveBulletCommand(Command):
    def __init__(self,state,bullet):
        self.state = state
        self.bullet = bullet
    def run(self):
        direction = (self.bullet.endPosition - self.bullet.startPosition).normalize()
        newPos = self.bullet.position + self.state.bulletSpeed * direction
        newCenterPos = newPos + Vector2(0.5,0.5)
        # If the bullet goes outside the world, destroy it
        if not self.state.isInside(newPos):
            self.bullet.status = "destroyed"
            return
        # If the bullet goes towards the target cell, destroy it
        if ((direction.x >= 0 and newPos.x >= self.bullet.endPosition.x) \
        or (direction.x < 0 and newPos.x <= self.bullet.endPosition.x)) \
        and ((direction.y >= 0 and newPos.y >= self.bullet.endPosition.y) \
        or (direction.y < 0 and newPos.y <= self.bullet.endPosition.y)):
            self.bullet.status = "destroyed"
            return
        # If the bullet is outside the allowed range, destroy it
        if newPos.distance_to(self.bullet.startPosition) >= self.state.bulletRange:  
            self.bullet.status = "destroyed"
            return
        # If the bullet hits a unit, destroy the bullet and the unit 
        unit = self.state.findLiveUnit(newCenterPos)
        if not unit is None and unit != self.bullet.unit:
            self.bullet.status = "destroyed"
            unit.status = "destroyed"
            self.state.notifyUnitDestroyed(unit)
            return
        # Nothing happends, continue bullet trajectory
        self.bullet.position = newPos
        
class DeleteDestroyedCommand(Command)       :
    def __init__(self,itemList):
        self.itemList = itemList
    def run(self):
        newList = [ item for item in self.itemList if item.status == "alive" ]
        self.itemList[:] = newList