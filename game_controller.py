from model import GameState 
import pygame
from pygame.math import Vector2
from .command import MoveCommand,TargetCommand,ShootCommand,MoveBulletCommand,DeleteDestroyedCommand
class GameController():
    
    def __init__(self):
        self.gameState = GameState.getInstance()

        # Controls
        self.playerUnit = self.gameState.units[0]
        self.commands = []
        
        

    def processInput(self,cellWidth,cellHeight):
        # Pygame events (close, keyboard and mouse click)
        moveVector = Vector2()
        mouseClicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameState.running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.gameState.running = False
                    break
                elif event.key == pygame.K_RIGHT:
                    moveVector.x = 1
                elif event.key == pygame.K_LEFT:
                    moveVector.x = -1
                elif event.key == pygame.K_DOWN:
                    moveVector.y = 1
                elif event.key == pygame.K_UP:
                    moveVector.y = -1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseClicked = True
                    
        # Keyboard controls the moves of the player's unit
        if moveVector.x != 0 or moveVector.y != 0:
            self.commands.append(
                MoveCommand(self.gameState,self.playerUnit,moveVector)
            )
                    
        # Mouse controls the target of the player's unit
        mousePos = pygame.mouse.get_pos()                    
        targetCell = Vector2()
        targetCell.x = mousePos[0] / cellWidth - 0.5
        targetCell.y = mousePos[1] / cellHeight - 0.5
        command = TargetCommand(self.gameState,self.playerUnit,targetCell)
        self.commands.append(command)

        # Shoot if left mouse was clicked
        if mouseClicked:
            self.commands.append(
                ShootCommand(self.gameState,self.playerUnit)
            )
                
        # Other units always target the player's unit and shoot if close enough
        for unit in self.gameState.units:
            if unit != self.playerUnit:
                self.commands.append(
                    TargetCommand(self.gameState,unit,self.playerUnit.position)
                )
                if unit.position.distance_to(self.playerUnit.position) <= self.gameState.bulletRange:
                    self.commands.append(
                        ShootCommand(self.gameState,unit)
                    )
                
        # Bullets automatic movement
        for bullet in self.gameState.bullets:
            self.commands.append(
                MoveBulletCommand(self.gameState,bullet)
            )
            
        # Delete any destroyed bullet
        self.commands.append(
            DeleteDestroyedCommand(self.gameState.bullets)
        )
                    
    def update(self):
        for command in self.commands:
            command.run()
        self.commands.clear()
        self.gameState.epoch += 1
