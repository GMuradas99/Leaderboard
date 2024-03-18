import pygame

from random import choice

class Row:
    def __init__(self, score, name, screen, width, height, offsetX, offsetY, y, color):
        self.width = width
        self.height = height
        self.score = score
        self.name = name
        self.screen = screen
        self.offsetX = offsetX
        self.offsetY = offsetY
        self.y = y
        self.color = color

        self.newY = -1
        self.speed = 0
        self.moving = False

        self.separation = 5
        self.font = pygame.font.Font('fonts/Montserrat-ExtraBold.ttf', self.height-int(self.height*0.25))

    def move(self, newY, frames):
        self.moving = True
        self.newY = newY
        # Floating operation, because this will not work for lower resolutions (3 days debbuging this line)
        floatSpeed = (self.newY-self.y)/frames
        self.speed = int(floatSpeed)
        if 1 > floatSpeed > 0:
            self.speed = 1
        if -1 < floatSpeed < 0:
            self.speed = -1

    def drawRow(self, color = None):
        if self.moving:
            self.y += self.speed
            if (self.speed > 0 and self.y >= self.newY) or (self.speed < 0 and self.y <= self.newY):
                self.y = self.newY
                self.moving = False
                self.speed = 0

        if color is None:
            color = self.color

        pygame.draw.rect(self.screen, color, pygame.Rect((self.offsetX, self.offsetY+self.y, self.width, self.height-self.separation)), border_radius=8)
        # Writing name
        self.screen.blit(self.font.render(str(self.name), True, (255,255,255)), (self.offsetX + 15, self.offsetY+self.y))
        # Writing score
        self.screen.blit(self.font.render(str(self.score), True, (255,255,255)), (self.offsetX + self.width - 100, self.offsetY+self.y))

class Leaderboard:
    def __init__(self, screen, width, height, offsetX, offsetY, numOfRows):
        self.screen = screen
        self.width = width
        self.height = height
        self.offsetX = offsetX
        self.offsetY = offsetY    
        self.numOfRows = numOfRows

        self.framesAnimation = 30
        self.visibleRows = []
        self.rows = []
        self.rowHeight = height//(numOfRows)
        self.lastAdded = None
    
    def __repr__(self):  
        return str(self.score)

    def addRow(self, score, name, color = None):
        """Add a new row to the leaderboard"""
        # color = (randint(0,255), randint(0,255), randint(0,255))
        if color is None:
            color = (186, 154, 218)
        row = Row(score, name, self.screen, self.width, self.rowHeight, self.offsetX, self.offsetY, self.height, color)
        self.rows.append(row)
        self.lastAdded = row

    def drawLeaderBoard(self):
        """Draw the leaderboard on the screen"""
        for i,row in enumerate(self.visibleRows):
            if i == 0:
                row.drawRow(color=(215,180,0))
            elif i == 1:
                row.drawRow(color=(192,192,192))
            elif i == 2:
                row.drawRow(color=(205,127,50))
            else:
                row.drawRow()
        
        # if self.lastAdded is not None:
        #     # Drawing last participant
        #     pygame.draw.rect(self.screen, (255,255,255), 
        #                      pygame.Rect((self.offsetX, self.offsetY+(self.numOfRows+1)*self.rowHeight, self.width, self.rowHeight-5)), 
        #                      border_radius=8)
        #     self.screen.blit(self.lastAdded.font.render(str("Last participant: "+self.lastAdded.name), 
        #                                                 False, 
        #                                                 (0,0,0)), 
        #                                                 (self.offsetX + 5, self.offsetY+(self.numOfRows+1)*self.rowHeight))
        #     self.screen.blit(self.lastAdded.font.render(str("Score: "+str(self.lastAdded.score)),
        #                                                 True, 
        #                                                 (0,0,0)), 
        #                                                 (self.offsetX + self.width - 150, self.offsetY+(self.numOfRows+1)*self.rowHeight))


    def orderRows(self):  
        sortedRows = sorted(self.rows, key = lambda x: x.score, reverse=True)
        self.visibleRows = sortedRows[:self.numOfRows].copy()

        for i,row in enumerate(self.visibleRows):
            row.move(i*self.rowHeight, self.framesAnimation)
    
    def addParticipantsFromAPI(self, participants):
        for participant in participants:

            score = participants[participant]['player_score'] * 100

            time =  participants[participant]['player_time']
            if time < 500000:
                time += time
                time = 1000000 - time
                time = time // 10000
                score += time

            self.addRow(score, participants[participant]['player_alias'])

    def removeParticipants(self, remove):
        for participant in remove:
            filteredRows = [row for row in self.rows if row.name != participant]
            self.rows = filteredRows

    def updateRow(self, name, score, increment=True):
        for row in self.rows:
            if row.name == name:
                if increment:
                    row.score += score
                else:
                    row.score = score
