from pygame.math import Vector2
from model import Unit

class GameState():
    _instance = None

    @staticmethod
    def getInstance():
        if GameState._instance is None:
            GameState()
        return GameState._instance

    def __init__(self):
        if GameState._instance is not None:
            raise Exception("GameState class is a singleton. Use getInstance() method to get the instance.")
        GameState._instance = self
        # Your existing __init__ code here
        self.epoch = 0
        self.worldSize = Vector2(16,10)
        self.running = True
        self.ground = [ 
            [ Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1)],
            [ Vector2(5,1), Vector2(5,1), Vector2(7,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(7,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,4), Vector2(7,2), Vector2(7,2), Vector2(7,2), Vector2(7,2), Vector2(7,2)],
            [ Vector2(5,1), Vector2(6,1), Vector2(5,1), Vector2(5,1), Vector2(6,1), Vector2(6,2), Vector2(5,1), Vector2(6,1), Vector2(6,1), Vector2(5,1), Vector2(6,2), Vector2(7,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1)],
            [ Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(7,1)],
            [ Vector2(5,1), Vector2(7,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,5), Vector2(7,2), Vector2(7,2), Vector2(7,2), Vector2(7,2), Vector2(8,5), Vector2(6,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1)],
            [ Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(7,1)],
            [ Vector2(6,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(7,1), Vector2(5,1), Vector2(6,2), Vector2(6,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1)],
            [ Vector2(5,1), Vector2(6,4), Vector2(7,2), Vector2(7,2), Vector2(7,2), Vector2(8,4), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1)],
            [ Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(7,1), Vector2(5,1), Vector2(5,1), Vector2(6,1), Vector2(5,1), Vector2(7,4), Vector2(7,2), Vector2(7,2), Vector2(7,2), Vector2(7,2), Vector2(7,2)],
            [ Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(6,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1)]
        ]
        self.walls = [
            [ None, None, None, None, None, None, None, None, None, Vector2(1,3), Vector2(1,1), Vector2(1,1), Vector2(1,1), Vector2(1,1), Vector2(1,1), Vector2(1,1)],
            [ None, None, None, None, None, None, None, None, None, Vector2(2,1), None, None, None, None, None, None],
            [ None, None, None, None, None, None, None, None, None, Vector2(2,1), None, None, Vector2(1,3), Vector2(1,1), Vector2(0,3), None],
            [ None, None, None, None, None, None, None, Vector2(1,1), Vector2(1,1), Vector2(3,3), None, None, Vector2(2,1), None, Vector2(2,1), None],
            [ None, None, None, None, None, None, None, None, None, None, None, None, Vector2(2,1), None, Vector2(2,1), None],
            [ None, None, None, None, None, None, None, Vector2(1,1), Vector2(1,1), Vector2(0,3), None, None, Vector2(2,1), None, Vector2(2,1), None],
            [ None, None, None, None, None, None, None, None, None, Vector2(2,1), None, None, Vector2(2,1), None, Vector2(2,1), None],
            [ None, None, None, None, None, None, None, None, None, Vector2(2,1), None, None, Vector2(2,3), Vector2(1,1), Vector2(3,3), None],
            [ None, None, None, None, None, None, None, None, None, Vector2(2,1), None, None, None, None, None, None],
            [ None, None, None, None, None, None, None, None, None, Vector2(2,3), Vector2(1,1), Vector2(1,1), Vector2(1,1), Vector2(1,1), Vector2(1,1), Vector2(1,1)]
        ]
        self.units = [
            Unit(self,Vector2(1,9),Vector2(1,0)),
            Unit(self,Vector2(6,3),Vector2(0,2)),
            Unit(self,Vector2(6,5),Vector2(0,2)),
            Unit(self,Vector2(13,3),Vector2(0,1)),
            Unit(self,Vector2(13,6),Vector2(0,1))
        ]
        self.bullets = [
        ]
        self.bulletSpeed = 0.1
        self.bulletRange = 4
        self.bulletDelay = 10
        
        self.observers = [
        ]
    
    @property
    def worldWidth(self):
        """
        Returns the world width as an integer
        """
        return int(self.worldSize.x)
    
    @property
    def worldHeight(self):
        """
        Returns the world height as an integer
        """
        return int(self.worldSize.y)

    def isInside(self,position):
        """
        Returns true is position is inside the world
        """
        return position.x >= 0 and position.x < self.worldWidth \
           and position.y >= 0 and position.y < self.worldHeight

    def findUnit(self,position):
        """
        Returns the index of the first unit at position, otherwise None.
        """
        for unit in self.units:
            if  int(unit.position.x) == int(position.x) \
            and int(unit.position.y) == int(position.y):
                return unit
        return None
    
    def findLiveUnit(self,position):
        """
        Returns the index of the first live unit at position, otherwise None.
        """
        unit = self.findUnit(position)
        if unit is None or unit.status != "alive":
            return None
        return unit
    
    def addObserver(self,observer):
        """
        Add a game state observer. 
        All observer is notified when something happens (see GameStateObserver class)
        """
        self.observers.append(observer)
        
    def notifyUnitDestroyed(self,unit):
        for observer in self.observers:
            observer.unitDestroyed(unit)