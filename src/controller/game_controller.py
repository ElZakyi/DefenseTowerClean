from model import GameState 
import pygame
from pygame.math import Vector2
from .command import MoveCommand,TargetCommand,ShootCommand,MoveBulletCommand,DeleteDestroyedCommand,LoadLevelCommand
from view import ArrayLayer,UnitsLayer,BulletsLayer,ExplosionsLayer,SoundLayer
class GameController():
    
    def __init__(self):
        self.gameState = GameState.getInstance()
        self.gameState.menu.menuItems = [
            {
                'title': 'Level 1',
                'action': lambda: self.loadLevelRequested("levels/level1.json")
            },
            {
                'title': 'Level 2',
                'action': lambda: self.loadLevelRequested("levels/level2.json")
            },
            {
                'title': 'Level 3',
                'action': lambda: self.loadLevelRequested("levels/level3.json")
            },
            {
                'title': 'Quit',
                'action': lambda: self.quitRequested()
            }
        ]  

        
        # Controls
        self.commands = []
    

    def gameWon(self):
        self.showMessage("Victory !")
 
    
    def gameLost(self):
        self.showMessage("GAME OVER")

    def loadLevelRequested(self, fileName):
        state = self.gameState
        LoadLevelCommand(state,fileName).run()
        try:
            state.currentActiveMode = 'Play'
        except Exception as ex:
            print(ex)
            self.showMessage("Level loading failed :-(")

        
    def showGameRequested(self):
        state = self.gameState
        state.currentActiveMode = 'Play'

    def showMenuRequested(self):
        state = self.gameState
        state.currentActiveMode = 'Overlay'
        
    def showMessage(self, message):
        state = self.gameState
        state.message = message
        state.currentActiveMode = 'Message'
        
    def quitRequested(self):
        self.gameState.running = False

    def updateLayers(self, layers):
        state = self.gameState
        layers[:] = [
            ArrayLayer(self.gameState.level.cellSize,"assets/ground.png",self.gameState,self.gameState.level.ground,0),
            ArrayLayer(self.gameState.level.cellSize,"assets/walls.png",self.gameState,self.gameState.level.walls),
            UnitsLayer(self.gameState.level.cellSize,"assets/units.png",self.gameState,self.gameState.level.units),
            BulletsLayer(self.gameState.level.cellSize,"assets/explosions.png",self.gameState,self.gameState.bullets),
            ExplosionsLayer(self.gameState.level.cellSize,"assets/explosions.png"),
            SoundLayer("assets/sound/170274__knova__rifle-fire-synthetic.wav","assets/sound/110115__ryansnook__small-explosion.wav")
        ]  

    def worldSizeChanged(self, cellSize,window):
        worldSize = self.gameState.worldSize.elementwise() * cellSize
        window = pygame.display.set_mode((int(worldSize.x),int(worldSize.y))) 


    def processInputMenu(self, layers,window):
        menu=self.gameState.menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quitRequested()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.showGameRequested()
                elif event.key == pygame.K_DOWN:
                    if menu.currentMenuItem < len(menu.menuItems) - 1:
                        menu.currentMenuItem += 1
                elif event.key == pygame.K_UP:
                    if menu.currentMenuItem > 0:
                        menu.currentMenuItem -= 1
                elif event.key == pygame.K_RETURN:
                    menuItem = menu.menuItems[menu.currentMenuItem]
                    try:
                        menuItem['action']()
                        self.updateLayers(layers)
                        self.worldSizeChanged(self.gameState.level.cellSize,window)
                    except Exception as ex:
                        print(ex)

    def processInputMessage(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quitRequested()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE \
                or event.key == pygame.K_SPACE \
                or event.key == pygame.K_RETURN:
                    self.showMenuRequested()
        

    def processInputLevel(self):
        # Pygame events (close, keyboard and mouse click)
        state = self.gameState
        moveVector = Vector2()
        mouseClicked = False
        tank = self.gameState.level.units[0]
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.QUIT:
                    print("quit")
                    self.quitRequested()
                    break
                elif event.key == pygame.K_ESCAPE:
                    print("escape")
                    self.showMenuRequested()
                    break
                elif event.key == pygame.K_RIGHT:
                    print("right")
                    moveVector.x = 1
                elif event.key == pygame.K_LEFT:
                    print("left")
                    moveVector.x = -1
                elif event.key == pygame.K_DOWN:
                    print("down")
                    moveVector.y = 1
                elif event.key == pygame.K_UP:
                    print("up")
                    moveVector.y = -1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("mouse")
                mouseClicked = True

        # If the game is over, all commands creations are disabled
        print("gameOver",state.level.gameOver)
        if state.level.gameOver:
            return
                    
        # Keyboard controls the moves of the player's unit
        print("moveVector",moveVector)
        if moveVector.x != 0 or moveVector.y != 0:
            self.commands.append(
                MoveCommand(state,tank,moveVector)
            )
                    
        # Mouse controls the target of the player's unit
        mousePos = pygame.mouse.get_pos()                    
        targetCell = Vector2()
        targetCell.x = mousePos[0] / state.level.cellWidth - 0.5
        targetCell.y = mousePos[1] / state.level.cellHeight - 0.5
        command = TargetCommand(state,tank,targetCell)
        self.commands.append(command)

        # Shoot if left mouse was clicked
        if mouseClicked:
            self.commands.append(
                ShootCommand(state,tank)
            )
                
        # Other units always target the player's unit and shoot if close enough
        for unit in state.level.units:
            if unit != tank:
                self.commands.append(
                    TargetCommand(state,unit,tank.position)
                )
                if unit.position.distance_to(tank.position) <= state.bulletRange:
                    self.commands.append(
                        ShootCommand(state,unit)
                    )
                
        # Bullets automatic movement
        for bullet in state.bullets:
            self.commands.append(
                MoveBulletCommand(state,bullet)
            )
            
        # Delete any destroyed bullet
        self.commands.append(
            DeleteDestroyedCommand(state.bullets)
        )
        self.update()
                    
    def update(self):
        state = self.gameState
        tank = self.gameState.level.units[0]
        for command in self.commands:
            command.run()
        self.commands.clear()
        state.epoch += 1
        
        # Check game over
        print("tank.status",tank.status)
        if tank.status != "alive":
            state.level.gameOver = True
            self.gameLost()
        else:
            oneEnemyStillLives = False
            for unit in state.level.units:
                if unit == tank:
                    continue
                if unit.status == "alive":
                    oneEnemyStillLives = True
                    break
            if not oneEnemyStillLives:
                state.level.gameOver = True
                self.gameWon()


    