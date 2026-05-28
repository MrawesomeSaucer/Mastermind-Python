from typing import *

class GameAttributes():
    '''
    A class to hold and manage all of the game's settings, settings that stay the same during the playing of the game
    '''
    def __init__(self):
        # settings
        self.game_mode = None
        self.codebreaker = None
        self.codebreaker_name = None
        self.mastermind = None
        self.allow_duplicates = None
        self.sequence = None
        self.sequence_length = None
        self.attempts = None
        self.pool = None

        self.settings = ['game_mode', 
                         'mastermind', 
                         'codebreaker',
                         'codebreaker_name',
                         'allow_duplicates', 
                         'sequence', 
                         'sequence_length', 
                         'attempts', 
                         'pool'
                        ]
    
    def clear_settings(self, for_replay: bool =False) -> None:
        '''
        Clear settings

        :param for_replay: stauts of this clear setting, if it is for replay again, only clear seuqnece

        :return:
            None
        '''
        for setting in self.settings:
            if for_replay is True and setting != 'sequence':
                continue

            setattr(self, setting, None)

        return
    

class GameState():
    '''class to hold states of the game, states that changes'''
    def __init__(self):
        self.moves_used = 0
        self.attempts_left = None
        self.winner = None
        self.player_inputs = []
        self.outputs = []

    def apply_state(self, inputed: List[str], output: List[str], attempts_left_decr: int=1, moves_used_incr: int=1) -> None:
        '''
        apply the states after each input

        :param inputed: the inputed items to be stored
        :param output: the output to be stored
        :param attempts_left_decr: how much to decrese attempts_left
        :param moves_used_incr: how much to increase moves_used

        :return:
            None
        '''
        self.attempts_left -= attempts_left_decr
        self.moves_used += moves_used_incr
        # store inputs and outputs to be displayed
        self.player_inputs.append(inputed)
        self.outputs.append(output)
        return

    def clear_state(self) -> None:
        '''
        Clear all the states

        :return:
            None
        '''
        self.winner = None
        self.moves_used = 0
        self.player_inputs.clear()
        self.outputs.clear()
        return