import pygame
from model import GameState
from pygame.math import Vector2
from .layer import Layer, ArrayLayer, UnitsLayer, BulletsLayer, ExplosionsLayer
from controller import MoveCommand, TargetCommand, ShootCommand, MoveBulletCommand, DeleteDestroyedCommand,Command,GameController


class UserInterface():
    
    def __init__(self):
        pygame.init()

        # Game state
        self.gameState = GameState.getInstance()

        # Rendering properties
        self.cellSize = Vector2(64,64)

        # Window
        windowSize = self.gameState.worldSize.elementwise() * self.cellSize
        self.window = pygame.display.set_mode((int(windowSize.x),int(windowSize.y)))
        pygame.display.set_caption("Tower Defense")
        pygame.display.set_icon(pygame.image.load("../assets/icon.png"))

        # Layers
        self.layers = [
            ArrayLayer(self.cellSize,"../assets/ground.png",self.gameState,self.gameState.ground,0),
            ArrayLayer(self.cellSize,"../assets/walls.png",self.gameState,self.gameState.walls),
            UnitsLayer(self.cellSize,"../assets/units.png",self.gameState,self.gameState.units),
            BulletsLayer(self.cellSize,"../assets/explosions.png",self.gameState,self.gameState.bullets),
            ExplosionsLayer(self.cellSize,"../assets/explosions.png")
        ]
        
        # All layers listen to game state events
        for layer in self.layers:
            self.gameState.addObserver(layer)

        self.controller = GameController()

        # Loop properties
        self.clock = pygame.time.Clock()

    @property
    def cellWidth(self):
        return int(self.cellSize.x)

    @property
    def cellHeight(self):
        return int(self.cellSize.y)

   
        
    def render(self):
        for layer in self.layers:
            layer.render(self.window)

        pygame.display.update()    
        
    def run(self):
        while self.gameState.running:
            self.controller.processInput(self.cellWidth,self.cellHeight)
            self.controller.update()
            self.render()
            self.clock.tick(60)
    