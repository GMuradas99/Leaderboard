from classes.window import leaderboardWindow
from classes.apiInteraction import euroBettingAPI

UPDATE_DELAY = 3               # In seconds
FPS = 30                       # Frames per second
NUMBER_OF_ROWS = 10            # Number of rows in leaderboard
RESULTS = 'https://docs.google.com/spreadsheets/d/1SVcGkEek1FtdbvXDZcSPjeAuFcUZlieiy1L7joL3rDM/edit?usp=sharing'
BETS = 'https://docs.google.com/spreadsheets/d/1oOMDQ_hA4ksDpszbuaXXEFXkhANo4s_IailTPYWRsAw/edit?usp=sharing'

api = euroBettingAPI(RESULTS, BETS)

leaderboard = leaderboardWindow(NUMBER_OF_ROWS, api, offset_width=100, window_resolution=(1500,650), font_path='fonts/Montserrat-ExtraBold.ttf')

leaderboard.mainLoop(API_update_delay=UPDATE_DELAY, fps=FPS)