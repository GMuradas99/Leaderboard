import re
import json
import requests
import pandas as pd

class googleSheetsAPI:
    def __init__(self, url: str) -> None:
        # Regular expression to match and capture the necessary part of the URL
        pattern = r'https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)(/edit#gid=(\d+)|/edit.*)?'

        # Replace function to construct the new URL for CSV export
        # If gid is present in the URL, it includes it in the export URL, otherwise, it's omitted
        replacement = lambda m: f'https://docs.google.com/spreadsheets/d/{m.group(1)}/export?' + (f'gid={m.group(3)}&' if m.group(3) else '') + 'format=csv'

        # Replace using regex
        self.url = re.sub(pattern, replacement, url)

    def dataFrame(self):
        return pd.read_csv(self.url)
    
    def getParticipants(self) -> dict:
        """Returns a dictionary with the id of the participants as keys for all participants
        """

        results = {}
        for i,row in self.dataFrame().iterrows():
            results[i] = {'player_alias': row['Name'], 'player_score': row['Score']}

        return results

class ScienceDayAPI:
    def __init__(self, url: str) -> None:
        self.url = url
        self.participants = self.getParticipants()

    def getParticipants(self) -> dict:
        """Returns a dictionary with the id of the participants as keys for all participants
        """
        dataApi = json.loads(requests.get(self.url).text)

        results = {}
        for instance in dataApi:
            results[instance['id']] = {'player_alias':instance['player_alias'], 'player_score':instance['player_score'], 'player_time':instance['player_time']}

        return results
    
    def getNewParticipants(self) -> dict:
        """Returns all participants that were added to the API
        """
        updatedParticipants = self.getParticipants()

        s = set(self.participants.keys())
        difference = [x for x in updatedParticipants if x not in s]

        results = {}
        for id in difference:
            results[id] = updatedParticipants[id]

        return results
    
    def updateParticipants(self) -> None:
        self.participants = self.getParticipants()