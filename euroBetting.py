import pygame
import random

from time import sleep, time

from Classes.leaderboard import Leaderboard, Row
from Classes.apiInteraction import euroBettingAPI

UPDATE_DELAY = 3                       # In seconds
FPS = 30                       # Frames per second
NUMBER_OF_ROWS = 11           # Number of rows in leaderboard
RESULTS = 'https://docs.google.com/spreadsheets/d/1SVcGkEek1FtdbvXDZcSPjeAuFcUZlieiy1L7joL3rDM/edit?usp=sharing'
BETS = 'https://docs.google.com/spreadsheets/d/1oOMDQ_hA4ksDpszbuaXXEFXkhANo4s_IailTPYWRsAw/edit?usp=sharing'

# Initializing 
pygame.init()
screen = pygame.display.set_mode((1500,650))
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

screenWidth = pygame.display.Info().current_w
screenHeight = pygame.display.Info().current_h  

offsetW = 230
offsetH = 30

lead = Leaderboard(screen, screenWidth - offsetW*2, screenHeight - offsetH*2, offsetW, offsetH, NUMBER_OF_ROWS)

# Setting up API
gs = euroBettingAPI(RESULTS, BETS)

# Adding participants from API
participants = gs.getParticipants()
for participant in participants:
    lead.addRow(participants[participant]['player_score'], participants[participant]['player_alias'])

lead.orderRows()

# Main loop
run = True
startTime = time()
while run:
    #Clearing previous frame
    screen.fill((56,18,114))

    # Drawing
    lead.drawLeaderBoard()

    # Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # Key is pressed
        if event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_u:
                lead.orderRows()
            if event.key == pygame.K_a:
                randScore = random.randint(0,100)
                print('Adding',randScore)
                lead.addRow(randScore, 'temp')
                lead.orderRows()
            if event.key == pygame.K_d:
                print("Updating row")
                lead.updateRow("Gonzalo", 4)
                lead.orderRows()
            if event.key == pygame.K_f:
                for row in lead.rows:
                    print(row.score, 'old',row.y, 'new', row.newY, 'moving', row.moving, 'speed', row.speed)
                
            if event.key == pygame.K_q:
                run = False
    
    # Time check for API updates
    elapsedTime = time() - startTime
    if elapsedTime > UPDATE_DELAY:
        print('Updating')

        # Getting new data
        participantData = gs.getParticipants()

        # Updating leaderboard
        for key in list(participantData.keys()):
            lead.updateRow(participantData[key]['player_alias'], participantData[key]['player_score'], increment=False)

        startTime = time()
        lead.orderRows()

    # Updating
    pygame.display.update()

    sleep(1/FPS)

pygame.quit()