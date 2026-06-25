import json
import os
from typing import *
from .constants import GameConstants

class LeaderboardManager:
    '''class to manage the leaderboard'''
    def __init__(self):
        self.file_path = GameConstants.LEADERBOARD_FILE_PATH
        # indent make the file more readable
        self.indent = 4

        # create a file if no file is present
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump([], file, indent=self.indent)

    def load(self) -> List[Dict[str, Any]]:
        '''
        read the json file and return the content

        :return:
            the json file content
        '''
        # 'r' open it as read mode
        with open(self.file_path, 'r') as file:
            return json.load(file)
        
    def save(self, data: List[Dict[str, Any]]) -> None:
        '''
        save the new data into the json file

        :param data: the data to save

        :return:
            None
        '''
        # 'w' open as write mode
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=self.indent)

        return
    
    def add_new_placement(self, name: str, score: int) -> None:
        '''
        add a new record dict

        :param name: the name of the record
        :param score: the score of the record

        :return:
            None
        '''
        # get the current leaderboard
        leaderboard = self.load()

        new_record = {'name':name, 'score':score}

        # add a new record
        leaderboard.append(new_record)

        # save
        self.save(leaderboard)

        return
        
    def update_score(self, name: str, score: int) -> None:
        '''
        add a new score to a existing name

        :param name: the name of the record
        :param score: the new score

        :return:
            None
        '''
        leaderboard = self.load()

        for record in leaderboard:
            record_name = record['name']
            record_score = record['score']

            if record_name != name:
                continue
            
            # if the score is lower or equal to previous score, no need to update it
            if record_score >= score:
                continue
            
            record['score'] = score

        # save
        self.save(leaderboard)

        return

    def update_placement(self) -> None:
        '''
        update the placement of each record, the bigger the score the more front the placement

        :return:
            None
        '''
        pleaderboard = self.load()

        # sort using ['score']
        pleaderboard = sorted(pleaderboard, key=lambda placement: placement['score'], reverse=True)

        # save
        self.save(pleaderboard)

        return        
    
    def update_leaderboard(self, name: str, score: int) -> None:
        '''
        update the leaderboard after a new record

        :param name: the name of the record
        :param score: the score of the record

        :return:
            None
        '''
        leaderboard = self.load()

        # if it is a new name, save as new record
        if not any(name == record['name'] for record in leaderboard):
            self.add_new_placement(name, score)
        else:
        # else just update the score
            self.update_score(name, score)

        # rearrange after updating
        self.update_placement()

        return 

    def reset_leaderboard(self) -> None:
        '''
        reset the json file, for DEBUG purposes

        :return:
            None
        '''
        with open(self.file_path, 'w') as file:
            json.dump([], file, indent=self.indent) 