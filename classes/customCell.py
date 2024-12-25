import re
import math
import pygame
import pandas as pd
from abc import ABC, abstractmethod

class customCell(ABC):
    @abstractmethod
    def drawCell(self, screen, x, y, width, height, updateApi):
        pass

class helloWorldCustomCell(customCell):
    def __init__(self, font_path):
        self.font_path = font_path

    def drawCell(self, screen, x, y, width, height, _):
        pygame.draw.rect(screen, (255,255,255), 
                             pygame.Rect((x, y, width, height)), 
                             border_radius=8)
        font = pygame.font.Font(self.font_path, height-int(height*0.25))
        screen.blit(font.render("Hello World", 
                                False, 
                                (0,0,0)), 
                                (x+width*0.05, y))
        
class lastNumbers(customCell):
    def __init__(self, url: str, font_path: str, numOfNumbers=3):
        pattern = r'https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)(/edit#gid=(\d+)|/edit.*)?'
        replacement = lambda m: f'https://docs.google.com/spreadsheets/d/{m.group(1)}/export?' + (f'gid={m.group(3)}&' if m.group(3) else '') + 'format=csv'
        self.url = re.sub(pattern, replacement, url)
        self.numOfNumbers = numOfNumbers
        self.lastNumbers = [math.nan] * numOfNumbers
        self.font_path = font_path
        self.updateLastNumbers()

    def getDF(self):
        return pd.read_csv(self.url)

    def updateLastNumbers(self):
        df = self.getDF()
        lastRound = df[df.columns.tolist()[-1]]
        lastRound = lastRound.dropna()
        if len(lastRound) == 0:
            return
        if len(lastRound) < self.numOfNumbers:
            self.lastNumbers = list(lastRound)
            self.lastNumbers.reverse()
        else:
            self.lastNumbers = list(lastRound[-self.numOfNumbers:])
            self.lastNumbers.reverse()

    def drawCell(self, screen, x, y, width, height, updateApi):
        if updateApi:
            self.updateLastNumbers()
        
        # Drawing cell
        pygame.draw.rect(screen, (255,255,255), 
                             pygame.Rect((x, y, width, height)), 
                             border_radius=0)
        
        # Drawing Text
        font = pygame.font.Font(self.font_path, height-int(height*0.25))
        fontSmall = pygame.font.Font(self.font_path, height-int(height*0.5))
        text_ultimos_numeros = font.render(str("ULTIMOS NUMEROS"), True, (0, 0, 0))
        screen.blit(text_ultimos_numeros, 
                                (width+20-text_ultimos_numeros.get_width(), y))
        
        # Drawing numbers
        if len(self.lastNumbers) == 0 or math.isnan(self.lastNumbers[0]):
            return
        number_separation = 100
        for i, number in enumerate(self.lastNumbers):
            if i == 0:
                screen.blit(font.render(str(int(number)), 
                                    True, 
                                    (0,0,0)), 
                                    (x+i*number_separation, y))
            else:
                screen.blit(fontSmall.render(str(int(number)), 
                                    True, 
                                    (30,30,30)), 
                                    (x+i*number_separation, y+height*0.25))