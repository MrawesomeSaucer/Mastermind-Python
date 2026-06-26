import random
from typing import *
from pathlib import Path
from .MastermindAI import AI
from .constants import GameOptionMapping, GameConstants, GameResult

class GameLogic():
    '''
    A class to hold the logics of the game
    '''
    def __init__(self):
        self.ai = AI()

    def get_project_root(self):
        current_file = Path(__file__).resolve()
        for parent in current_file.parents:
            print(parent)
            if (parent / '__init__.py').exists():
                return parent
        
        raise FileNotFoundError('pyproject.toml not found')

    def parse_int_input(self, player_input: str) -> bool:
        '''
        check if the input is convertable to interger

        :param player_input: the user input to check

        :return:
            True: if the input is convertable
            False: if otherwise
        '''
        try:
            int(player_input)
            return True
        except ValueError:
            return False

    def make_preset_pool(self, colors: List[str], rep_char: str) -> List[str]:
        '''
        make a preset pool with a character

        :param colors: the list of color to apply to the char
        :param rep_char: the representative character of the pool

        :return:
            the created pool
        '''
        pool = []
        for color in colors:
            item = color + rep_char
            pool.append(item)
        return pool
    
    def is_item_duplicate_sequence(self, item: str, sequence: List[str], allow_duplicates: bool) -> bool:
        '''
        check if the item is an duplicate in the sequence

        :param item: the item to be checked
        :param sequence: the currently inputed sequence
        :param allow_duplicates: if allow duplicates is on duplicates are allowed in the sequence

        :return:
            True: if the item is an duplicate
            False: if otherwise
        '''
        if item in sequence and allow_duplicates is False:
            return True
        
        return False
    
    def name_validation(self, inputed_name) -> bool:
        if not inputed_name:
            return False
        
        return True

    def pool_input_logic(self, player_input: List[str], colors: Dict[str, str], all_characters: List[str]) -> tuple:
        '''
        Convert pool making input from abstract names into actual color code, and characters
        Includes wild card logic

        :param player_input: Inputed value, which is a list in this func
        :param colors: dict of all the color code with name of color as key and color code as value
        :param all_characters: list of all the characters

        :return: 
            converted colors and characters
        '''
        # create variables
        col_input, char_input = player_input
        col = char = None

        # check the first item of list, the color
        if col_input.lower() == GameOptionMapping.WILD_CARD_OPTION:
            # all returns all of the color code
            col = list(colors.values())
        # if it is not 'all', check if the inputed value match with any color
        elif col_input in colors:
            # return color code of inputed color
            col = [colors[col_input]]
        else:
            pass
        
        # check the second item of list, the character
        if char_input.lower() == GameOptionMapping.WILD_CARD_OPTION:
            # all returns all the character
            char = all_characters
        elif char_input in all_characters:
            char = [char_input]
        else:
            pass
        
        # return the color and the character
        return col, char
    
    def generate_sequence(self, allow_duplicates: bool, pool: List[str], sequence_length: int) -> List[str]:
        '''
        generate a sequence randomly from the pool

        :param allow_duplicates: duplicates are allowed if True, they are not allowed if otherwise
        :param pool: the pool to make the sequence from
        :param sequence_length: the length of the sequence

        :return:
            the sequence generated
        '''
        if allow_duplicates:
            # use random.choices to allow dupicates to be selected
            return random.choices(pool, k=sequence_length)
        # use sample to avoid duplicates
        return random.sample(pool, k=sequence_length)
    
    def in_game_check_input(self, player_input: List[str], sequence: List[str]) -> List[str]:
        '''
        compare inputed and the sequence to give feed back
        abstrace string are returned, these are converted by ui when printing. Example 'correct' converts to red

        :param player_input: the inputed items
        :param sequence: the sequence created

        :return:
            the result of each input
        '''
        # creates an output variable
        output = [' ' for _ in sequence]

        # creates a copy of input and output
        remaining_input = player_input[:]
        remaining_sequence = sequence[:]

        # first iteration checks for exact matches
        for index, input in enumerate(player_input):
            if input == sequence[index]:
                # add result to output variable
                output[index] = GameResult.CORRECT
                # remove the match after
                remaining_input[index] = None
                remaining_sequence[index] = None
        
        # second iteration checks for wrong and partial match, using the reamaing inputs
        for index, input in enumerate(remaining_input):
            if input is None:
                # skip exact matches
                continue
            elif input in remaining_sequence:
                output[index] = GameResult.PARTIAL
            else:
                output[index] = GameResult.WRONG

        return output
    
    def check_win(self, output: List[str], attempts_left: int) -> Optional[str]:
        '''
        check the output and attempts left for a result

        :param output: the output of the current guess
        :param attempts_left: amount of attmepts left

        :return:
            None: No win or lost condition is met
            str: result based all the condtions
        '''
        # winning is check first 
        if all(o == GameResult.CORRECT for o in output):
            # return 'win' if all the output is correct
            return GameResult.WINNER_CODEBREAKER
        if attempts_left <= 0:
            # return 'lost' if no attempts is left
            return GameResult.WINNER_MASTERMIND
        # return None if non of the condition is met
        return None
    
    def create_item_logic(self, col: List[str], char: List[str]) -> List[str]:
        '''
        combines the converted colors and characters and return a list of all the combined items

        :param col: the convereted color codes
        :param char: the converted characters

        :return:
            all the combined items
        '''
        # creates a items variable to add combined item and return
        items = []

        # loop every color and character
        for c in col:
            for ch in char:
                # item is the combination of the color and the character
                item = c + ch
                # add item to the list
                items.append(item)

        # return list when done
        return items
    
    def calculate_sequence_length_max(self, all_characters: int, all_colors: int) -> int:
        '''
        calculate all the unique item avaliable

        :param all_characters: the amount of all the characters
        :param all_colors: the amount of all the colors

        :return:
            amount of all the item avaliable
        '''
        # any color can be applied to any character
        return all_characters * all_colors
    
        '''Input validation'''
    def option_input_validation(self, player_input: str, options: List[str]) -> bool:
        '''
        check if the inputed value is the list of valid inputs

        :param player_input: Inputed string
        :param options: the list of valid inputs

        :return:
            True: if input is in included
            False: if otherwise
        '''
        if player_input in options:
            return True              
        return False
    
    def int_input_validation(self, value, int_min: int = 0, int_max: Optional[int] = None) -> bool:
        '''
        check if the value if an interger and if it is in the range

        :param value: the value to convert and check
        :param int_min: the minimum of the range
        :param int_max: the maximum of the range

        :return:
            True: if value is an int and it is in range
            False: if otherwise
        '''
        # check if int is in range, int max is optional
        if int_max is not None:
            return int_min <= value <= int_max
        else:
            return int_min <= value
        
    def index_input_validation(self, value: int, t_list: List, off_by_one: bool = False) -> bool:
        '''
        check if the value can be a index that is in range in a list

        :param value: the value to convert and check
        :param t_list: the list to try the value on
        :param off_by_one: the switch to minus the value by one

        :return:
            True: if value is convertable and in range
            False: if otherwise
        '''
        try:
            # off by one is useful for the user because python list is 0 index
            if off_by_one:
                value -= 1

            # try to see if index in in range in a list
            t_list[value]

            # return true if all the test passed
            return True
        
        # index not in range returns false
        except IndexError:
            return False
    
    def is_quit(self, player_input: str) -> bool:
        '''
        Check if the input is "q"

        :param player_input: Inputed value

        :return:
            True: if input is 'q'
            False: if otherwise
        '''
        return isinstance(player_input, str) and player_input == GameOptionMapping.QUIT_OPTION
    
    def name_validation(self, player_input: str) -> bool:
        '''
        validate the inputed name

        :param player_input: the inputed name

        :return:
            True: if the name is valide
            False: if otherwise
        '''
        # the name cannot be longer than 50 characters and cannot be empty
        if not player_input or len(player_input) > GameConstants.NAME_LENGTH_MAX:
            return False
        return True
    
    def get_difficulty_level_score(self, sequence_length: int, pool_length: int, allow_duplicates: bool, attempts: int) -> int:
        '''
        calculate the difficulty level score, harder the game the higher the score, vice versa

        :param sequence_length: the length of sequence
        :param pool_length: the length of the pool
        :param allow_duplicates: the status of allow_duplicates
        :param attempts: the number of attempts

        :return:
            the final score
        '''
        # sequence length and pool length is multiplied be modifier
        sequence_length_score = sequence_length * GameConstants.SEQUENCE_LENGTH_SCORE_MODIFIER

        pool_length_score = pool_length * GameConstants.POOL_LENGTH_SCORE_MODIFIER

        subtotal_score = sequence_length_score + pool_length_score

        # allow_duplicates add extra score
        if allow_duplicates:
            subtotal_score *= GameConstants.ALLOW_DUPLICATES_SCORE_MODIFIER
        # if attempts is less the half of the length of pool, increase score
        if attempts <= pool_length / 2:
            subtotal_score *= GameConstants.LESS_ATTEMPT_MODIFER
        # if attempts is more than 50% higher than the pool length, decrease score
        if attempts >= pool_length * 1.5:
            subtotal_score *= GameConstants.MORE_ATTEMPT_MODIFER
        # if sequence_length is less than half of the pool length, increase
        if sequence_length <= pool_length / 2:
            subtotal_score *= GameConstants.LESS_SEQUENCE_LENGTH_MODIFIER
        # if sequence_length is the same as pool length, decrease
        if sequence_length == pool_length:
            subtotal_score *= GameConstants.SAME_SEQUENCE_LENGTH_MODIFIER
        # if sequence_length 50% higher than the pool length, increase
        if sequence_length > pool_length * 1.5:
            subtotal_score *= GameConstants.MORE_SEQUENCE_LENGTH_MODIFIER

        # round the score
        final_score = round(subtotal_score)

        return final_score
    
    def ai_get_amount_of_moves(self, sequence_length: int, pool: List[str], allow_duplicates: bool, sequence: List[str]) -> int:
        '''
        get amount of moves that ai uses to solve the sequence for reference

        :param sequence_length: length of sequence to pass into make_move
        :param pool: the pool to pass into make move
        :param allow_duplicates: the status of allow_duplicates to pass into make move
        :param sequence: the sequence to pass into check input

        :return:
            the amount of moves ai used
        '''
        nmoves = 0
        result = None
        # initiate the ai
        self.ai.AI_initiate(pool, sequence_length)
        while result is None:
            move = self.ai.make_move(sequence_length, pool, allow_duplicates)

            nmoves += 1

            output = self.in_game_check_input(move, sequence)

            result = self.check_win(output, 1)

            if not result:
                # modify if no result yet
                self.ai.AI_modify_p_moves(allow_duplicates, move, output)
                
        return nmoves
    
    def get_result_score(self, moves_used: int, sequence_length: int, pool: List[str], allow_duplicates: bool, sequence: List[str], winner: str) -> int:
        '''
        get a score base on amount to moves code breaker used and ai used

        :param moves_used: amount to moves the code breaker used
        :param sequence_length: sequence length to pass to ai_get_amount_of_moves
        :param pool: the pool to pass to ai_get_amount_of_moves
        :param allow_duplicates: the status of allow_duplicates to pass to ai_get_amount_of_moves
        :param sequence: the sequence to pass to ai_get_amount_of_moves
        :param winner: the winner of the game

        :return:
            the calculated score
        '''
        score = 0
        ai_moves_used = self.ai_get_amount_of_moves(sequence_length, pool, allow_duplicates, sequence)

        if moves_used <= ai_moves_used and winner == GameResult.WINNER_CODEBREAKER:
            # if used less than what ai used, add onto the score
            score += GameConstants.WIN_AND_LESS_THAN_AI
            move_difference = ai_moves_used - moves_used
            score *= move_difference + 1

        return score

    def get_score(self, moves_used: int, sequence_length: int, pool: List[str], pool_length: int, allow_duplicates: bool, sequence: List[str], result: str, attempts: int) -> int:
        '''
        get a score base on the difficulty of the game and beating the ai
        

        :param moves_used: amount of moves the codebreaker used
        :param sequence_length: the length of the sequence
        :param pool: the current pool
        :param pool_length: the length of the pool
        :param allow_duplicates: the status of allow_duplicates
        :param sequence: the current sequence
        :param result: the result of the game
        :param attempts: the number of attempts

        :return:
            the final score
        '''
        # get difficulty and result score
        result_score = self.get_result_score(moves_used, sequence_length, pool, allow_duplicates, sequence, result)
        difficulty_score = self.get_difficulty_level_score(sequence_length, pool_length, allow_duplicates, attempts)

        final_score = result_score + difficulty_score

        if result != GameResult.WINNER_CODEBREAKER:
            return 0
        
        return final_score