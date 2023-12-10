# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 19:49:00 2023

@author: sport
"""

import pygame
import simpleGE
import random

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.car = Car(self)
        self.gasCan = []
        self.checkEngine = []
        for i in range(5):
            self.gasCan.append(GasCan(self))
        for i in range(2):
            self.checkEngine.append(CheckEngine(self))
        
        self.lblScore = simpleGE.Label()
        self.lblScore.text = "Score: 0"
        self.lblScore.center = (95, 50)
        self.score = 0
        
        self.lblTime = simpleGE.Label()
        self.lblTime.text = "Time Left: 30"
        self.lblTime.center = (550, 50)
        
        self.timer = simpleGE.Timer()
        self.gameOver = False

        self.sprites = [self.lblScore, self.lblTime, self.car, self.gasCan, self.checkEngine]

    def update(self):
        if not self.gameOver:
            timeLeft = 30 - self.timer.getElapsedTime()
            if timeLeft < 0:
                timeLeft = 0
                self.gameOver = True
                gameOverScene = GameOverScene(self.score)
                gameOverScene.start()
            self.lblTime.text = f"Time left: {timeLeft:.01f}"
            self.lblScore.text = f"score: {self.score}"

class Car(simpleGE.BasicSprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("Car.png")
        self.setSize(180, 140)
        self.moveSpeed = 5
        self.y = 450
        
    def checkEvents(self):
         if not self.scene.gameOver:   
            if self.scene.isKeyPressed(pygame.K_LEFT):
                self.x -= self.moveSpeed
            if self.scene.isKeyPressed(pygame.K_RIGHT):
                self.x += self.moveSpeed

class StartMenu(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.startButton = simpleGE.Button()
        self.startButton.text = 'Start'
        self.startButton.center = (300, 300)
        self.sprites = [self.startButton]
    
    def update(self):
        if self.startButton.clicked:
            self.startGame()
    
    def startGame(self):
        gameScene = Game()
        gameScene.start()

class GasCan(simpleGE.BasicSprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("JerryCan.png")
        self.setSize(75, 75)
        self.hornSound = simpleGE.Sound("Horn.mp3")
        self.reset()
    
    
    def reset(self):
        self.x = random.randint(0, 640)
        self.y = 10
        self.dy = random.randint(5, 10)
    
    def checkEvents(self):
        if not self.scene.gameOver:
            if self.collidesWith(self.scene.car):
                self.scene.score += 1
                self.hornSound.play()
                self.reset()
        
    def checkBounds(self):
        if not self.scene.gameOver:
            if self.rect.bottom > self.screen.get_height():
                self.reset()

class CheckEngine(simpleGE.BasicSprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("CheckEngine.png")
        self.setSize(75, 75)
        self.crashSound = simpleGE.Sound("CrashEffect.mp3")
        self.reset()
    
    def reset(self):
        self.x = random.randint(0, 640)
        self.y = 10
        self.dy = random.randint(5, 10)
    
    def checkEvents(self):
        if not self.scene.gameOver:
            if self.collidesWith(self.scene.car):
                self.scene.score -= 1
                self.crashSound.play()
                self.reset()
    
    def checkBounds(self):
        if not self.scene.gameOver:
            if self.rect.bottom > self.screen.get_height():
                self.reset()
                
class GameOverScene(simpleGE.Scene):
    def __init__(self, finalScore):
        super().__init__()
        self.finalScore = finalScore
        self.lblGameOver = simpleGE.Label()
        self.lblGameOver.text = "Game Over"
        self.lblGameOver.center = (300, 200)
        
        self.lblScore = simpleGE.Label()
        self.lblScore.text = f"Final Score: {finalScore}"
        self.lblScore.center = (300,230)
        
        self.sprites = [self.lblGameOver, self.lblScore]
        
    def update(self):
        if self.isKeyPressed(pygame.K_RETURN):
            self.startMenu()
        
def main():
  startButton = StartMenu()
  startButton.start()
  print("Game Over")
  
  '''
  game = Game()
  game.start()
  print('Game Over')
  '''
if __name__ == "__main__":
    main()
        
    
        
            