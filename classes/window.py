import pygame
import random

from time import sleep, time

from classes.apiInteraction import API
from classes.leaderboard import Leaderboard

class leaderboardWindow:
    def __init__(self, 
                 number_of_rows: int,
                 api: API,
                 offset_width: int = 230,
                 offset_height: int = 30,
                 window_resolution: tuple = None,
                 reverse: bool = True,
                 font_path: str = None,
                 background_color: tuple = (56,18,114),
                 row_color: tuple = (186, 154, 218),
                 negative_row_color: tuple = None,
                 podium_colors: list = [(215,180,0), (192,192,192), (205,127,50)],
                 show_last_participant: bool = False,
                 no_frame = False,
                 ) -> None:
        # Initializing 
        pygame.init()
        pygame.display.set_caption('GMO Leaderboard')
        if window_resolution is None:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            if no_frame:
                self.screen = pygame.display.set_mode(window_resolution, pygame.NOFRAME)
            else:
                self.screen = pygame.display.set_mode(window_resolution)

        # Getting screen resolution
        self.screenWidth = pygame.display.Info().current_w
        self.screenHeight = pygame.display.Info().current_h

        self.offsetW = offset_width
        self.offsetH = offset_height
        
        self.background_color = background_color

        self.lead = Leaderboard(self.screen, self.screenWidth - self.offsetW*2, self.screenHeight - self.offsetH*2, self.offsetW, self.offsetH, 
                                number_of_rows, fontPath=font_path, reverse=reverse, rowColor=row_color, negative_row_color=negative_row_color, 
                                podium_colors=podium_colors, show_last_participant=show_last_participant)

        self.api = api

        # Adding participants from API
        participants = self.api.getParticipants()
        for participant in participants:
            self.lead.addRow(participants[participant]['player_score'], participants[participant]['player_alias'])
        self.lead.orderRows()

    def mainLoop(self, API_update_delay: int = 3, fps: int = 30) -> None:
        # Main loop
        run = True
        startTime = time()
        while run:
            #Clearing previous frame
            self.screen.fill(self.background_color)

            # Drawing
            self.lead.drawLeaderBoard()

            # Event Handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                # Key is pressed
                if event.type == pygame.KEYDOWN:  
                    # Quit with q               
                    if event.key == pygame.K_q:
                        run = False
            
            # Time check for API updates
            elapsedTime = time() - startTime
            if elapsedTime > API_update_delay:

                # Getting new data
                participantData = self.api.getParticipants()

                # Updating leaderboard
                for key in list(participantData.keys()):
                    self.lead.updateRow(participantData[key]['player_alias'], participantData[key]['player_score'], increment=False)

                startTime = time()
                self.lead.orderRows()

            # Updating
            pygame.display.update()

            sleep(1/fps)

        pygame.quit()