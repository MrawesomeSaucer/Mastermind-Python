import sys
from typing import *
from .ConsoleUI import UI
from .GameLogic import GameLogic
from .GameConfig import GameAttributes, GameState
from .constants import GameConstants, GameOptionMapping, GameStages
from .MastermindAI import AI
from .LeaderboardManager import LeaderboardManager

class MastermindGame():
    '''The controller class, combines all the logic, UI, and settings to run the game'''
    def __init__(self):
        # instances
        self.ui = UI()
        self.game_attributes = GameAttributes()
        self.state = GameState()
        self.game_logic = GameLogic()
        self.codebreaker_ai = AI()
        self.leaderboard_manager = LeaderboardManager()

        # caption printed at start
        self.ui.start_game_caption()

    def exit_game(self):
        '''
        exit the game with an exit message

        :return:
            None
        '''
        sys.exit(self.ui.exit_message)

    def input_helper(self, strip=True, lower=True) -> str:
        '''
        the helper func to combine UI asking for input and logic check if user is trying to quit

        :param strip: True: returned input will be strip() False: leave as is
        :param lower: True: the returned input will be lower() False: leave as is

        :return:
            the inputed value if user didn't exit the game
        '''
        user_input = self.ui.get_input()

        if strip:
            user_input = user_input.strip()
        
        if lower:
            user_input = user_input.lower()

        # quitting is checked every where
        if self.game_logic.option_input_validation(user_input.lower(), [GameOptionMapping.QUIT_OPTION]):
            self.exit_game()
        
        return user_input

    # customization helper
    def customize_mode(self) -> str:
        '''
        the helper function to customize the mode

        :return:
            str: the selected mode if no error detected
        '''
        while True:
            # print the caption and ask for input
            self.ui.single_player_customize_mode_caption()

            user_input = self.input_helper()

            # if inputed value is not in the map's keys, it is not valid
            if not self.game_logic.option_input_validation(user_input, list(GameOptionMapping.CUSTOMIZING_MODE_MAPPING)):
                # print error and return None
                self.ui.raise_error(error_type=1)
                continue

            # if no error detected, return the mapped input
            return GameOptionMapping.CUSTOMIZING_MODE_MAPPING[user_input]

    def customize_allow_duplicates(self) -> bool:
        '''
        the helper func to customize allow duplcates

        :return:
            the desire status of allow duplicates
        '''
        
        while True:
            # print caption and ask for input
            self.ui.customize_allow_duplicates_caption()

            user_input = self.input_helper()
                
            # if input not in map's key it is invalid
            if not self.game_logic.option_input_validation(user_input, list(GameOptionMapping.CUSTOMIZING_ALLOW_DUPLICATES_MAPPING)):
                # print error
                self.ui.raise_error(error_type=1)
                continue
            
            # return the bool if no error detected
            return GameOptionMapping.CUSTOMIZING_ALLOW_DUPLICATES_MAPPING[user_input]

    def customize_sequence_length(self) -> int:
        '''
        the helper func to customize sequence length

        :return:
            the desire sequence length
        '''
        # easy and hard mode use map
        if self.game_attributes.game_mode != GameOptionMapping.CUTSTOM_MODE:
            return GameOptionMapping.SEQUENCE_LENGTH_MAPPING[self.game_attributes.game_mode]
        
        while True:
            # print caption and ask for input
            self.ui.customize_sequence_length_caption(self.game_attributes.allow_duplicates)

            user_input = self.input_helper()

            # if input is not contertable to a int
            if not self.game_logic.parse_int_input(user_input):
                self.ui.raise_error(error_type=2)
                continue
                
            # convert to int if pass parse test
            intergerlized_input = int(user_input)
            
            # check if input is in range
            sequence_length_max = self.game_logic.calculate_sequence_length_max(len(self.ui.avaliable_characters), len(list(self.ui.colors)))
            if not self.game_logic.int_input_validation(intergerlized_input, 
                                                        int_min=GameConstants.SEQUENCE_LENGTH_MIN, 
                                                        int_max=sequence_length_max if self.game_attributes.allow_duplicates is False else None):
                # print error and try again
                self.ui.raise_error(error_type=2)
                continue

            # return the converted value if no error detected
            return intergerlized_input

    def customize_pool_single_input_helper(self, user_input: str, pool: List[str]) -> Optional[List[Optional[str]]]:
        '''
        helper fucntion to handle if user input one item when customizing pool

        :param user_input: inputed value
        :param pool: the current inputed pool

        :return:
            None: input is not 'd' or pool is not validated or not a valid input
            []: empty list in returned if user clear the pool
            List[str]: original pool is returned if user confirm pool
        '''
        single_input_map = {
            GameOptionMapping.POOL_SINGLE_INPUT_SHOW_AVALIABLE_OPTION:self.ui.print_pool_avaliable,
            GameOptionMapping.POOL_SINGLE_INPUT_WILD_CARD_EXP_OPTION:self.ui.print_wild_card_exp
        } 

        # execute the function if inputed is a key to the map
        # lower input since lower is False when using helper
        if self.game_logic.option_input_validation(user_input.lower(), list(single_input_map)):
            single_input_map[user_input.lower()]()
            return None
                    
        # 'd' ends the pool making and validates the pool
        if self.game_logic.option_input_validation(user_input.lower(), [GameOptionMapping.END_POOL_OPTION]):
            # if the pool is not validated
            if not self.game_logic.int_input_validation(len(pool), 
                                                        int_min=self.game_attributes.sequence_length if self.game_attributes.allow_duplicates is False 
                                                        else GameConstants.POOL_LENGTH_MIN):
                # if allow duplicates is on the length of pool can be smaller than the length of the sequence as long as it is higer than the pool length minimum
                self.ui.raise_error(error_message='Invalid pool created, please check the length of the pool')
                return None
                            
            # confirm the pool if it is valid
            self.ui.confirm_pool_caption(pool)

            user_input = self.input_helper()

            # inputing any key other than 'c' will return the inputed pool
            if not self.game_logic.option_input_validation(user_input, [GameOptionMapping.CLEAR_OPTION]):
                return pool

            # clear the pool if inputed 'c'
            return []
        else:
            self.ui.raise_error(error_type=1)
            return None
    
    def customize_pool_add_item_helper(self, items: List[str], pool: List[str]) -> List[str]:
        '''
        helper function to add all the converted items into the pool

        :param items: the converted items
        :param pool: the current inputed pool

        :return:
            the final pool with items added
        '''
        for item in items:
            # if the item is already in pool ask player for deletion or ignore
            if item in pool:
                self.ui.handle_pool_input_dupilcate_caption(item)

                user_input = self.input_helper()

                if self.game_logic.option_input_validation(user_input, [GameOptionMapping.CLEAR_OPTION]):
                    pool.remove(item)
                    self.ui.raise_error(error_message='Duplicate deleted')
                    continue

                self.ui.raise_error(error_message='Duplicate ignored')
                continue
                
            pool.append(item)

        return pool

    def customize_pool(self) -> List[str]:
        '''
        helper func to customize and make the pool

        :return:
            the created and validated pool
        '''
        # easy and hard mode's pool is the same and not customizable
        if self.game_attributes.game_mode != GameOptionMapping.CUTSTOM_MODE:
            return self.game_logic.make_preset_pool(list(self.ui.colors.values()), self.ui.rep_char)
        
        # print caption
        self.ui.make_pool_caption(GameConstants.POOL_LENGTH_MIN, self.game_attributes.sequence_length, self.game_attributes.allow_duplicates)

        # create pool variable
        pool = []

        while True:
            # print inputing caption and ask for input
            self.ui.make_pool_inputing_caption(len(pool))

            user_input = self.input_helper(lower=False)
            
            # if user only inputed one item
            if self.game_logic.int_input_validation(len(user_input.split()), int_min=1, int_max=1):
                val = self.customize_pool_single_input_helper(user_input, pool)
                if val is None:
                    continue
                
                # update the pool if there is value
                pool = val

                # if pool is not cleared it is confirmed, return it
                if pool:
                    return pool
                
                continue
      
            # if the user input is not only one item we split it and turn it into a list
            user_input = user_input.split()

            # if it is not 2 items print error
            if len(user_input) != GameConstants.POOL_CUSTOMIZATION_NUMBER_OF_INPUT_EXPECTED:
                self.ui.raise_error(error_message='Please only input 2 items')
                continue
            
            # convert inputed items into color and characters
            col, char = self.game_logic.pool_input_logic(user_input, self.ui.colors, self.ui.avaliable_characters)

            # if conversion failed print error and ask for input again
            if not col:
                self.ui.raise_error(error_message='Invalid color inputed')
                continue
            
            if not char:
                self.ui.raise_error(error_message='Invalid character inputed')
                continue
            
            # after conversion create a list of items
            items = self.game_logic.create_item_logic(col, char)

            # add all the items into the pool variable
            pool = self.customize_pool_add_item_helper(items, pool)

            # print the modified pool after adding items
            self.ui.print_pool(pool, False)

    def customize_mastermind(self) -> str:
        '''
        helper function to customize the sequence creator

        :return:
            the mapped creator
        '''
        while True:
            # print caption and ask for input
            self.ui.customize_mastermind_caption()

            user_input = self.input_helper()

            # print error if input is not valid
            if not self.game_logic.option_input_validation(user_input, list(GameOptionMapping.CUSTOMIZING_BRAIN_MAPPING)):
                self.ui.raise_error(error_type=1)
                continue

            # return mapped value if validated
            return GameOptionMapping.CUSTOMIZING_BRAIN_MAPPING[user_input]
        
    def customize_codebreaker(self) -> str:
        '''
        helper function to customize the codebreaker's brain

        :return:
            the codebreaker's brain
        '''
        while True:
            self.ui.cutomize_codebreaker_caption()

            user_input = self.input_helper()

            # print error if input is not valid
            if not self.game_logic.option_input_validation(user_input, list(GameOptionMapping.CUSTOMIZING_BRAIN_MAPPING)):
                self.ui.raise_error(error_type=1)
                continue

            # return mapped value if validated
            return GameOptionMapping.CUSTOMIZING_BRAIN_MAPPING[user_input]
        
    def customize_codebreaker_name(self) -> str:
        '''
        helper function to customize the name of the codebreaker

        :return:
            the inputed name
        '''
        while True:
            if self.game_attributes.codebreaker == GameOptionMapping.COMPUTER:
                return GameOptionMapping.COMPUTER_CODEBREAKER_NAME

            self.ui.customize_codebreaker_name_caption()

            self.ui.print_leaderboard(self.leaderboard_manager.load())

            user_input = self.input_helper(lower=False)

            if not self.game_logic.name_validation(user_input):
                self.ui.raise_error(error_message=f'Name cannot be empty or longer than {GameConstants.NAME_LENGTH_MAX} characters')
                continue

            return user_input
         
    def customize_sequence(self) -> List[str]:
        '''
        helper function to customize the sequence

        :return:
            the created or generated sequence
        '''
        # if the creator is computer generate the sequence randomly
        if self.game_attributes.mastermind != GameOptionMapping.HUMAN:
            return self.game_logic.generate_sequence(self.game_attributes.allow_duplicates, self.game_attributes.pool, self.game_attributes.sequence_length)
        
        # print start caption to introduce
        self.ui.customize_sequence_start_caption(self.game_attributes.sequence_length, self.game_attributes.pool, self.game_attributes.allow_duplicates)

        # create a sequence variable
        sequence = []

        while True:
            # if the sequence met the validation ask for player to confirm
            if self.game_logic.int_input_validation(len(sequence), int_min=self.game_attributes.sequence_length):
                self.ui.confirm_sequence_caption(sequence)

                user_input = self.input_helper()

                # unlesss 'c' is inputed the created sequence will be returned
                if self.game_logic.option_input_validation(user_input, [GameOptionMapping.CLEAR_OPTION]):
                    # 'c' clear the current inputed sequence
                    sequence.clear()
                    continue
                
                # after sequence is created by human clear the terminal to avoid it being seen
                self.ui.clear_terminal()
                return sequence
            
            # print caption and ask for input
            self.ui.customize_sequence_inputing_caption(len(sequence) + 1) # plus one because pool items are printed with 1 index while python uses 0 index

            user_input = self.input_helper()

            if not self.game_logic.parse_int_input(user_input):
                self.ui.raise_error(error_type=2)
                continue

            intergerlized_input = int(user_input)

            # if the input is not valid print error and ask again
            if not self.game_logic.index_input_validation(intergerlized_input, self.game_attributes.pool, True):
                self.ui.raise_error(error_type=3)
                continue
            
            # convert input to item if valid
            item = self.game_attributes.pool[intergerlized_input - 1]

            # duplicates raise error if allow duplicats is off
            if self.game_logic.is_item_duplicate_sequence(item, sequence, self.game_attributes.allow_duplicates):
                self.ui.raise_error(error_message='Duplicates are only allowed if allow duplicates is on')
                continue

            # add the item to the sequence      
            sequence.append(item)

            # print the current sequence
            self.ui.print_sequence(sequence)

    def customize_attempts(self) -> int:
        '''
        helper func to customize the attempts

        :return:
            the converted attempts amount
        '''
        # easy and hard mode's attempts is setted up
        if self.game_attributes.game_mode != GameOptionMapping.CUTSTOM_MODE:
            return GameOptionMapping.MODE_ATTEMPTS_MAPPING[self.game_attributes.game_mode]
        
        while True:
            # print caption and ask for input
            self.ui.customize_attempts_caption()

            user_input = self.input_helper()

            if not self.game_logic.parse_int_input(user_input):
                self.ui.raise_error(error_type=2)
                continue

            intergerlized_input = int(user_input)

            # if the input is not valid raise error and return None
            if not self.game_logic.int_input_validation(intergerlized_input, int_min=GameConstants.ATTEMPTS_MIN):
                self.ui.raise_error(error_type=2)
                continue

            # return the converted input if valid
            return intergerlized_input

    def confirm_settings(self) -> bool:
        '''
        helper function to confirm all the settings

        :return:
            True: if the user confirm the settings
            False: if otherwise
        '''
        # all the settings with setting name as key and value as value
        # create this dict here because I don't want ui to get the entire attributes class but only the neccesary settings
        settings = {
                    'mode':self.game_attributes.game_mode,
                    'sequence_length':self.game_attributes.sequence_length,
                    'repeating_letter':self.game_attributes.allow_duplicates,
                    'pool':self.game_attributes.pool,
                    'mastermind':self.game_attributes.mastermind,
                    'codebreaker':self.game_attributes.codebreaker,
                    'codebreaker_name':self.game_attributes.codebreaker_name,
                    'attempts':self.game_attributes.attempts
                }
        
        # print caption and ask for input
        self.ui.confirm_settings_caption(settings)

        self.ui.print_leaderboard(self.leaderboard_manager.load())

        user_input = self.input_helper()

        # any input that is not 'c' will confirm the settings
        if not self.game_logic.option_input_validation(user_input, [GameOptionMapping.CLEAR_OPTION]):
            return True

        # clear all the settings and customize again if 'c' in inputed
        self.game_attributes.clear_settings()
        return False
    
    def get_board_states(self) -> dict:
        '''
        helper function to get a snap shot of the game state to print the play board

        :return:
            the game states with their name as key and value as value
        '''
        return {
            'sequence':self.game_attributes.sequence, 
            'attempts':self.game_attributes.attempts,
            'winner':self.state.winner,
            'sequence_length':self.game_attributes.sequence_length,
            'attempts_left':self.state.attempts_left,
            'player_inputs':self.state.player_inputs,
            'outputs':self.state.outputs
        }
    
    def playing_get_player_input_helper(self) -> List[str]:
        '''
        get the human inputed guess

        :return:
            the complete input
        '''
        inputed = []
        while True:
            # print caption and ask for input
            self.ui.playing_inputing_color_inputing_caption(len(inputed) + 1)

            user_input = self.input_helper()

            if not self.game_logic.parse_int_input(user_input):
                self.ui.raise_error(error_type=2)
                continue

            intergerlized_input = int(user_input)

            # if the input is not valid raise error and ask again
            if not self.game_logic.index_input_validation(intergerlized_input, self.game_attributes.pool, True):
                self.ui.raise_error(error_type=3)
                continue
            
            # add the item if it is valid
            inputed.append(self.game_attributes.pool[intergerlized_input - 1])

            # print the inputed items
            self.ui.playing_print_inputed(inputed)

            # if the input is not complete skip the rest of the code
            if not len(inputed) == self.game_attributes.sequence_length:
                continue

            return inputed
    
    def playing_get_input(self) -> List[str]:
        '''
        helper function to get the player's input when playing the mastermind game

        :return:
            the complete inputed guess by the player
        '''
        while True:
            if self.game_attributes.codebreaker == GameOptionMapping.COMPUTER:

                self.ui.AI_pause_caption()

                inputed = self.codebreaker_ai.AI_make_move(self.game_attributes.sequence_length, self.game_attributes.pool, self.game_attributes.allow_duplicates, self.game_attributes.attempts)
            
            else:
                inputed = self.playing_get_player_input_helper()
    
            # if input is complete ask player to confirm
            self.ui.confrim_playing_inputed(inputed, self.game_attributes.codebreaker)

            user_input = self.input_helper()

            if self.game_logic.option_input_validation(user_input, [GameOptionMapping.CLEAR_OPTION]) and self.game_attributes.codebreaker == GameOptionMapping.HUMAN:
                inputed.clear()
                continue

            return inputed

    def playing_initiate(self) -> None:
        '''
        initiate the ai and state before playing

        :return:
            None
        '''
        if self.game_attributes.codebreaker == GameOptionMapping.COMPUTER:
                self.codebreaker_ai.AI_initiate(self.game_attributes.pool, self.game_attributes.sequence_length)

        self.state.attempts_left = self.game_attributes.attempts

        return

    def playing_apply_state(self, inputed: List[str], outputed: List[str]) -> None:
        '''
        apply the state and update AI after each round

        :param inputed: the inputed items
        :param outputed: the output of the input

        :return:
            None
        '''
        self.state.apply_state(inputed, outputed)

        # modify AI if it is active
        if self.game_attributes.codebreaker == GameOptionMapping.COMPUTER:
            self.codebreaker_ai.AI_modify_p_moves(self.game_attributes.allow_duplicates, inputed, outputed)

        return
        
    def handle_start(self) -> int:
        '''
        function to handle the start state of the pargram

        :return:
            game state interger constant
        '''
        # print caption and ask for input
        self.ui.start_game_inputing_caption()

        user_input = self.input_helper()

        # raise error if no valid option is inputted
        if not self.game_logic.option_input_validation(user_input, GameOptionMapping.STARTING_OPTIONS):
            self.ui.raise_error(error_type=1)
            return GameStages.STARTING
        
        # 's' starts the game and 'd' prints the game ddescription
        if user_input == GameOptionMapping.START_OPTION:
            return GameStages.CUSTOMIZING
        elif user_input == GameOptionMapping.DESCRIPTION_OPTION:
            self.ui.clear_terminal()
            self.ui.print_game_descrption()
            self.input_helper()
            return GameStages.STARTING

    def handle_customization(self) -> int:
        '''
        Handle the customization state of the game.
        Combines all customization helper function and assign all the returned value to attributes

        :return:
            game state interger constant
        '''
        # the order of this map matters as the customization needs order
        customize_map = [
            ('game_mode', self.customize_mode),
            ('allow_duplicates', self.customize_allow_duplicates),
            ('sequence_length', self.customize_sequence_length),
            ('pool', self.customize_pool),
            ('mastermind', self.customize_mastermind),
            ('codebreaker', self.customize_codebreaker),
            ('codebreaker_name', self.customize_codebreaker_name),
            ('sequence', self.customize_sequence),
            ('attempts', self.customize_attempts)
        ]

        # ask for each value and assigins it
        for attr, helper in customize_map:
            if getattr(self.game_attributes, attr) is not None:
                continue

            val = helper()
            setattr(self.game_attributes, attr, val)
            
        # if all customzation is done, confirm the settings
        if self.confirm_settings():
            self.playing_initiate()
            return GameStages.PLAYING
          
        self.game_attributes.clear_settings()
        return GameStages.CUSTOMIZING
           
    def handle_playing(self) -> int:
        '''
        handle the playing state of the program

        :return:
            the game state interger constant
        '''
        # clear terminal to clear previous customization captions
        self.ui.clear_terminal()

        # print board, get input, get output using input and get result using ouput
        self.ui.print_current_play_board(self.get_board_states())

        self.ui.playing_input_color_start_caption(self.game_attributes.pool)

        inputed = self.playing_get_input()

        output = self.game_logic.in_game_check_input(inputed, self.game_attributes.sequence)

        self.playing_apply_state(inputed.copy(), output.copy())

        winner = self.game_logic.check_win(output, self.state.attempts_left)

        # if there is result will change the game state
        if winner:
            self.state.winner = winner
            return GameStages.ENDING

        return GameStages.PLAYING

    def handle_ending(self) -> int: # end caption can get more exciting
        '''
        handle the ending state of the program

        :return:
            the game state interger constant
        '''
        # reset terminal and print the final board
        self.ui.clear_terminal()

        self.ui.print_current_play_board(self.get_board_states())

        score = self.game_logic.get_score(self.state.moves_used, 
                                          self.game_attributes.sequence_length, 
                                          self.game_attributes.pool, 
                                          len(self.game_attributes.pool),
                                          self.game_attributes.allow_duplicates,
                                          self.game_attributes.sequence,
                                          self.state.winner,
                                          self.game_attributes.attempts)
        
        # ask for restart   
        self.ui.ending_start_caption(self.state.winner, self.game_attributes.codebreaker_name, score)

        self.state.clear_state()

        self.leaderboard_manager.update_leaderboard(self.game_attributes.codebreaker_name, score)

        self.ui.print_leaderboard(self.leaderboard_manager.load())

        self.ui.ending_inputing_caption()

        user_input = self.input_helper()

        if not self.game_logic.option_input_validation(user_input, list(GameOptionMapping.ENDING_RECUSTOMIZE_OPTION)):
            self.game_attributes.clear_settings(for_replay=True)
        else:
            self.game_attributes.clear_settings()
        
        return GameStages.CUSTOMIZING