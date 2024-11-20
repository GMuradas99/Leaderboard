from classes.window import leaderboardWindow
from classes.apiInteraction import googleSheetsAPI


UPDATE_DELAY = 3               # In seconds
FPS = 30                       # Frames per second
NUMBER_OF_ROWS = 15            # Number of rows in leaderboard
SHEETS_URL = 'https://docs.google.com/spreadsheets/d/1OAF9IgNfLfqvUFTZa0rPV_2HaNa4fc7Qd3UN1jvCYHc/edit?usp=sharing'

api = googleSheetsAPI(SHEETS_URL)

leaderboard = leaderboardWindow(NUMBER_OF_ROWS, api, offset_width=100, font_path='fonts/Montserrat-ExtraBold.ttf')

leaderboard.mainLoop(API_update_delay=UPDATE_DELAY, fps=FPS)