import pygame

from random import choice

class Row:
    def __init__(self, score, name, screen, width, height, offsetX, offsetY, y, color, fontPath = None):
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

        # Setting font
        self.font = pygame.font.Font(fontPath, self.height-int(self.height*0.25))

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
        score_text = f"{self.score:.2f}" if isinstance(self.score, float) else str(self.score)
        self.screen.blit(self.font.render(score_text, True, (255,255,255)), (self.offsetX + self.width - 200, self.offsetY+self.y))

class Leaderboard:
    def __init__(self, screen, width, height, offsetX, offsetY, numOfRows, rowColor: tuple = (186, 154, 218), fontPath = None, 
                 reverse: bool = True, negative_row_color: tuple = None, podium_colors: list = None, custom_cell = None):
        self.screen = screen
        self.width = width
        self.height = height
        self.offsetX = offsetX
        self.offsetY = offsetY    
        self.numOfRows = numOfRows
        if custom_cell is not None: self.numOfRows -= 1
        self.reverse = reverse

        self.framesAnimation = 30
        self.visibleRows = []
        self.rows = []
        self.rowHeight = height//(numOfRows)
        self.lastAdded = None
        self.custom_cell = custom_cell

        self.rowColor = rowColor
        self.negative_row_color = negative_row_color
        self.podium_colors = podium_colors
        self.fontPath = fontPath
    
    def __repr__(self):  
        return str(self.score)

    def addRow(self, score, name):
        """Add a new row to the leaderboard"""
        row = Row(score, name, self.screen, self.width, self.rowHeight, self.offsetX, self.offsetY, self.height, self.rowColor, self.fontPath)
        self.rows.append(row)
        self.lastAdded = row

    def drawLeaderBoard(self, updateApi = False):
        """Draw the leaderboard on the screen"""
        for i,row in enumerate(self.visibleRows):
            # Default color
            row.drawRow()

            # Negative row color
            if row.score < 0 and self.negative_row_color is not None:
                row.drawRow(color=self.negative_row_color)

            # First second and third
            if self.podium_colors is not None and i < len(self.podium_colors):
                row.drawRow(color=self.podium_colors[i])                
        
        if self.custom_cell is not None:

            self.custom_cell.drawCell(self.screen, self.offsetX, self.offsetY+(self.numOfRows)*self.rowHeight, self.width, self.rowHeight-5, updateApi)

            # # Drawing last participant
            # pygame.draw.rect(self.screen, (255,255,255), 
            #                  pygame.Rect((self.offsetX, self.offsetY+(self.numOfRows+1)*self.rowHeight, self.width, self.rowHeight-5)), 
            #                  border_radius=8)
            # self.screen.blit(self.lastAdded.font.render(str("Last participant: "+self.lastAdded.name), 
            #                                             False, 
            #                                             (0,0,0)), 
            #                                             (self.offsetX + 5, self.offsetY+(self.numOfRows+1)*self.rowHeight))
            # self.screen.blit(self.lastAdded.font.render(str("Score: "+str(self.lastAdded.score)),
            #                                             True, 
            #                                             (0,0,0)), 
            #                                             (self.offsetX + self.width - 150, self.offsetY+(self.numOfRows+1)*self.rowHeight))


    def orderRows(self):  
        sortedRows = sorted(self.rows, key = lambda x: x.score, reverse = self.reverse)
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
        """
        Updates the score of a row with the given name. If the row does not exist, it adds a new row.
        Parameters:
        name (str): The name of the row to update.
        score (int): The score to update or increment.
        increment (bool): If True, increments the score by the given value. If False, sets the score to the given value. Default is True.
        Returns:
        None
        """
        updated = False
        for row in self.rows:
            if row.name == name:
                if increment:
                    row.score += score
                else:
                    row.score = score
                updated = True
        
        if not updated:
            self.addRow(score, name)
                    

