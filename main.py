from classes.customCell import lastNumbers, helloWorldCustomCell
from classes.window import leaderboardWindow
from classes.apiInteraction import googleSheetsAPI

UPDATE_DELAY = 2                                        # In seconds
FPS = 30                                                # Frames per second
NUMBER_OF_ROWS = 15                                     # Number of rows in leaderboard
FONT_PATH = 'fonts/Montserrat-ExtraBold.ttf'            # Custom font
SHEETS_URL = 'https://docs.google.com/spreadsheets/d/1fRigW0X1irnclTC_XGF-XHvwNjvDzfK5rXWikZU70s0/edit?gid=0#gid=0'
CUSTOM_CELL_URL = 'https://docs.google.com/spreadsheets/d/1PP0G17lIbv8mHBSFhHMSUE6faz2bjUWY72izqrgMRKU/edit?usp=sharing'

api = googleSheetsAPI(SHEETS_URL, 'Nombre', 'Total')
ccLastNumbers = lastNumbers(CUSTOM_CELL_URL, FONT_PATH, numOfNumbers=8)

# leaderboard = leaderboardWindow(NUMBER_OF_ROWS, api, offset_width=100, font_path=FONT_PATH, negative_row_color=(255,0,0),
#                                 custom_cell=ccLastNumbers, window_resolution=(700,500))
leaderboard = leaderboardWindow(NUMBER_OF_ROWS, api, offset_width=100, font_path=FONT_PATH, negative_row_color=(255,0,0),
                                custom_cell=ccLastNumbers)

leaderboard.mainLoop(API_update_delay=UPDATE_DELAY, fps=FPS)