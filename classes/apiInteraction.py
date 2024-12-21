import re
import json
import requests
import pandas as pd

from abc import ABC, abstractmethod

class API(ABC):
    @abstractmethod
    def getParticipants(self):
        pass

class euroBettingAPI(API):
    """
    This class is used to interact with the Euro Betting API. It is used to get the participants of the Euro Betting game. 
    Need 2 google sheet links, one with the people and countries they bet for, another for the countries and their scores.
    """
    def __init__(self, results: str, bets: str) -> None:
        pattern = r'https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)(/edit#gid=(\d+)|/edit.*)?'
        replacement = lambda m: f'https://docs.google.com/spreadsheets/d/{m.group(1)}/export?' + (f'gid={m.group(3)}&' if m.group(3) else '') + 'format=csv'

        # Replace using regex
        self.results = re.sub(pattern, replacement, results)
        self.bets = re.sub(pattern, replacement, bets)

    def resultsDF(self):
        return pd.read_csv(self.results)
    
    def resultsDict(self):
        return self.resultsDF().set_index('Country')['Score'].to_dict()
    
    def betsDF(self):
        return pd.read_csv(self.bets)
    
    def getParticipants(self) -> dict:
        """Returns a dictionary with the id of the participants as keys for all participants
        """

        multipliers = [1,0.8,0.6,0.4,0.2]
        scores = self.resultsDict()

        results = {}
        for i,row in self.betsDF().iterrows():
            score = int(scores[row['1']]*multipliers[0] + scores[row['2']]*multipliers[1] + scores[row['3']]*multipliers[2] + scores[row['4']]*multipliers[3] + scores[row['5']]*multipliers[4])
            results[i] = {'player_alias': row['Name'], 'player_score': score}

        return results

class googleSheetsAPI(API):
    """
    A class to interact with Google Sheets API and retrieve data in CSV format.
    Attributes:
        url (str): The URL of the Google Sheets document.
        target_column (str): The name of the column containing the target data.
        name_column (str): The name of the column containing the participant names.
    Methods:
        dataFrame():
            Reads the Google Sheets data and returns it as a pandas DataFrame.
        getParticipants() -> dict:
            Returns a dictionary with the participant IDs as keys and their aliases and scores as values.
    """
    def __init__(self, url: str, name_column: str, target_column: str) -> None:
        """
        Initializes the instance with the provided URL, target column, and name column.
        Args:
            url (str): The URL of the Google Sheets document.
            target_column (str): The name of the target column in the spreadsheet.
            name_column (str): The name of the name column in the spreadsheet.
        Attributes:
            target_column (str): Stores the name of the target column.
            name_column (str): Stores the name of the name column.
            url (str): The modified URL for CSV export from the Google Sheets document.
        """
        # Saving variables
        self.target_column = target_column
        self.name_column = name_column

        # Regular expression to match and capture the necessary part of the URL
        pattern = r'https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)(/edit#gid=(\d+)|/edit.*)?'

        # Replace function to construct the new URL for CSV export
        # If gid is present in the URL, it includes it in the export URL, otherwise, it's omitted
        replacement = lambda m: f'https://docs.google.com/spreadsheets/d/{m.group(1)}/export?' + (f'gid={m.group(3)}&' if m.group(3) else '') + 'format=csv'

        # Replace using regex
        self.url = re.sub(pattern, replacement, url)

    def dataFrame(self):
        """
        Reads a CSV file from the specified URL and returns it as a pandas DataFrame.
        Returns:
            pd.DataFrame: A DataFrame containing the data from the CSV file.
        """
        return pd.read_csv(self.url)
    
    def getParticipants(self) -> dict:
        """Returns a dictionary with the id of the participants as keys for all participants
        """
        results = {}
        for i,row in self.dataFrame().iterrows():
            results[i] = {'player_alias': row[self.name_column], 'player_score': row[self.target_column]}

        return results

class ScienceDayAPI(API):
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