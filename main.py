from classes.window import leaderboardWindow
from classes.apiInteraction import googleSheetsAPI


UPDATE_DELAY = 3               # In seconds
FPS = 30                       # Frames per second
NUMBER_OF_ROWS = 15            # Number of rows in leaderboard
SHEETS_URL = 'https://docs.google.com/spreadsheets/d/1fRigW0X1irnclTC_XGF-XHvwNjvDzfK5rXWikZU70s0/edit?gid=0#gid=0'

api = googleSheetsAPI(SHEETS_URL, 'Nombre', 'Total')

leaderboard = leaderboardWindow(NUMBER_OF_ROWS, api, offset_width=100, font_path='fonts/Montserrat-ExtraBold.ttf', negative_row_color=(255,0,0),
                                show_last_participant=True)

leaderboard.mainLoop(API_update_delay=UPDATE_DELAY, fps=FPS)