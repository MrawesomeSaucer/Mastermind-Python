import string
from typing import *
from .constants import GameResult, GameOptionMapping

COLORS_MAP = {
    "black": "\033[38;5;242m",
    "red": "\033[38;5;9m",
    "green": "\033[38;5;10m",
    "yellow": "\033[38;5;11m",
    "blue": "\033[38;5;12m",
    "magenta": "\033[38;5;13m",
    "cyan": "\033[38;5;14m",
    "white": "\033[38;5;250m",
}

COLOR_RESET = '\033[0m'
AVAILABLE_CHARACTERS = list(string.ascii_letters+string.digits+string.punctuation)
EXIT_MESSAGE = '\nThank you for playing mastermind'
INPUT_PROMPT = '> '

SEPERATOR = '\n---------------------------------------------\n'
GAME_DESCRIPTION = (
            '\nGame desciption'
            f'{SEPERATOR}'
            'Mastermind is a classic code breaking that involves logic, deduction, and strategy.\n\n'

            'Objective'
            f'{SEPERATOR}'
            'One player, or the game itself creates a secret code, and the other player tries to guess it in as few attempts as possible.\n'
            'The code breaker wins by successfullly guessing code based on attempts and feed backs. The code maker wins by creating a code that the code breaker cannot break.\n\n'

            'Gameplay'
            f'{SEPERATOR}'
            'The code breaker makes a guess by inputing a sequence of color or item.\n'
            'Feed back is given based on the code eaker\'s guess.\n'
            'Red means the color or item is in the correct spot.\n'
            'White means the color or item is in the sequence but the wrong spot.\n'
            'Black means that the color or item is not in the sequence.\n'
            'Code breaker keeps guessing until the correct sequence is guessed or number of attempts runs out.\n'
            'This is a modified version of mastermind. In a real game of mastermind, feed back does not correspond to the input, but here it does.\n'
            'This is to allow longer sequence and longer pool and faster game play!\n\n'

            'Customizing'
            f'{SEPERATOR}'
            'Now that you know the basics of the mastermind game. You should know about how to start a game of mastermind in this program.\n'
            'Before you start the game, you will have the chance to customize your game of mastermind.\n'
            'There are 3 modes for you to choose from: easy, hard, and custom.\n'
            'Think of easy and hard mode like presets, most of the customization is already setted up for you.\n'
            'The only customization you can have in easy and hard mode are allow dupicates, mastermind and codebreaker.\n'
            'Allow duplicates allow you to have repeating item in your sequence which can increase the difficulty.\n'
            'The mastermind (code maker) can be a human or the computer will make the sequence for you, same goes for codebreaker.\n\n'

            'Custom mode on the other hand allow you to customize all aspects of the game.\n'
            'Including the two customization above in easy and hard mode, you can customize length of sequence, amount of attempts, and customize your pool (pool of item or color to make sequence and select from).\n'
            'The items of the pool is also no longer limited to colors. It can be number, letters and even punctuations. In total, there are 658 unique items to make pool from.\n'
            'So you can expand your imagination, you can have a biggest and longest mastermind game ever.\n'
            'Notice that if you have a sequence too long it might mess up the formatting of the playboard base on your monitor size\n\n'

            'Leaderboard & Scoring'
            f'{SEPERATOR}'
            'If you are a codebreaker, you can enter a name to be saved on the leaderboard. After each game, a score will be given based on the difficulty of the game and your performance.\n'
            'The score will be save on the leaderboard under your name. And no worries, only higher scores will be saved.\n'
            'You can compete with your friends to see who can have the highest score!\n\n'

            'Navigating'
            f'{SEPERATOR}'
            'You need to navigate the program using keyboard inputs. The avaliable options of inputs will be listed when asked for input. Just type the letter or option you want and press enter to register it.\n'
            'Remeber that at any point of program and any input chance you can input "q" to exit the program. \n\n'

            'AI'
            f'{SEPERATOR}'
            'This program includes a simple and stright forward codebreaker AI.\n'
            'You can try it with a very large sequence as this program allows, which can be quite fun watching it.\n'
        )

LINE_LIMIT = 25

ERROR_MAP = {
    1:'Invalid input option detected',
    2:'Please input a positive interger within range',
    3:'Please input an index within range'
}

REP_CHAR = 'o'

class UI():
    '''
    A class to handle all the printing, and asking for inputs
    '''
    def __init__(self):
        # color name as key and color code as value
        self.colors = COLORS_MAP

        # color needs to be reset after applied
        self.color_reset = COLOR_RESET

        # confirm messeges are green and error messages are red
        self.confirm_message_color = self.colors['green']
        self.error_message_color = self.colors['red']

        self.output_color_map = {
            GameResult.CORRECT:self.colors['red'],
            GameResult.PARTIAL:self.colors['white'],
            GameResult.WRONG:self.colors['black']
        }

        self.avaliable_characters = AVAILABLE_CHARACTERS

        self.rep_char = REP_CHAR

        self.exit_message = EXIT_MESSAGE

    '''Misc'''
    def raise_error(self, error_message: Optional[str] = None, error_type: Optional[int] = None) -> None:
        '''
        print error messages in red

        :param error_message: message to display

        :return:
            None
        '''
        if error_type is not None:
            print(self.error_message_color + ERROR_MAP[error_type] + self.color_reset)
            return

        print(self.error_message_color + error_message + self.color_reset)

    def confirm(self, confirm_message: str) -> None:
        '''
        print messages in green color

        :param confirm_message: the message to be display

        :return:
            None
        '''
        print(self.confirm_message_color + confirm_message + self.color_reset)
        return
    
    def clear_terminal(self) -> None:
        '''
        clear the screen / terminal

        :return:
            None
        '''
        # \033[H move cursor to the top
        # \033[J clear screen
        # \033[3J clear scroll back buffer
        print("\033[H\033[J\033[3J", end="")
        return
    
    def print_pool_avaliable(self) -> None:
        '''
        print the avaliable colors and characters to make pool from

        :return:
            None
        '''
        print()
        print('Avaliable charactes')
        print('Digits: ' + ' '.join(string.digits))
        print('Letters: ' + ' '.join(string.ascii_letters))
        print('Other: ' + ' '.join(string.punctuation))
        print()
        print('Avaliable colors')
        for color in list(self.colors):
            print(f'{self.colors[color]}{color}{self.color_reset}', end=' ')
        return

    def print_wild_card_exp(self) -> None:
        '''
        print the explanation for the wild card logic

        :return:
            None
        '''
        print()
        print('\"all\" can be used to input all characters or colors')
        print('Example usage:')
        print('input: all 1 \noutput: 1 in all the colors avaliable ')
        print()
        print('input: red all \noutput: all avaliable characters in red')
        print()
        print('input: all all \noutput: all the avaliable chatacters in all the avaliable colors, in total 658 unique chatacters')
        return

    def print_pool(self, pool: List[str], with_index: bool) -> None:
        '''
        print the current pool with indexes to the item

        :param pool: list containing all the item in the pool

        :return:
            None
        '''
        print('Pool: ')
        for index, item in enumerate(pool):
            # every 25 item switch line
            if index % LINE_LIMIT == 0 and index != 0:
                print('\n')
            print(f'{index + 1}: ' if with_index else ' ', end='')
            print(f'{item}{self.color_reset}', end=' ')
        print()
        return

    def get_input(self) -> str:
        '''
        ask player for a input

        :return:
            the striped and lowered input
        '''
        return input(INPUT_PROMPT)
    
    def print_status(self, target: str, status: bool) -> None:
        '''
        print the status of allow duplicates

        :param status: the status of allow duplicates
        
        :return:
            None
        '''
        status_map = {
            True:'on',
            False:'off'
        }

        print(f'{target}: {status_map[status]}')
        return
    
    def get_space_in_between(self, longest_length: int) -> str:
        '''
        return a long string of spaces with a length of longest_length

        :param longest_length: the number of spaces in between

        :return:
            the string of spaces
        '''
        return ' '.join('' for _ in range(longest_length))
    
    def print_leaderboard(self, leaderboard: List[Dict[str, Any]]) -> None:
        '''
        prints the current leader board

        :return:
            None
        '''
        if leaderboard == []:
            return
        print()
        print('place' + '\t' + 'name' + self.get_space_in_between(max(len(record['name']) for record in leaderboard) - len('name')) + '\t' + 'score')
        # place, name, and score seperate by a tab
        for placement, record in enumerate(leaderboard):
            # max len - self len keep formatting correct with different name lengths
            print(f'{placement + 1}' + '\t' + record["name"] + self.get_space_in_between(max(len(record['name']) for record in leaderboard) - len(record['name'])) + '\t' + f'{record["score"]}')
        print()

        return

    '''Start'''
    def print_game_descrption(self) -> None:
        '''
        print the game description

        :return:
            None
        '''
        print(GAME_DESCRIPTION)
        self.confirm('Input any key to continue... ')
        return
    
    def start_game_caption(self) -> None:
        '''
        print the start caption to welcome player

        :return:
            None
        '''
        print(f'Welcome to mastermind, input {GameOptionMapping.QUIT_OPTION} at any time to quit the program')
        return
    
    def start_game_inputing_caption(self) -> None:
        '''
        print the inputing caption to ask player to start game

        :return:
            None
        '''
        print()
        print(f'Input {GameOptionMapping.START_OPTION} to start game or {GameOptionMapping.DESCRIPTION_OPTION} to see game description')
        return
       
    '''Customizing'''
    # customize mode
    def single_player_customize_mode_caption(self) -> None:
        '''
        print the caption to list avaliable option to select mode

        :return:
            None
        '''
        print()
        print('Select mode')
        print(f'Input {GameOptionMapping.EASY_PRESET_OPTION} for {GameOptionMapping.EASY_PRESET} preset')
        print(f'Input {GameOptionMapping.HARD_PRESET_OPTION} for {GameOptionMapping.HARD_PRESET} preset')
        print(f'Input {GameOptionMapping.CUTSTOM_MODE_OPTION} for {GameOptionMapping.CUTSTOM_MODE} mode')
        return
    

    # customize allow duplicates
    def customize_allow_duplicates_caption(self) -> None:
        '''
        print the options to customize allow duplicates

        :return:
            None
        '''
        print()
        print(f'Allow duplicates? Input {GameOptionMapping.ALLOW_DUPLICATE_TRUE_OPTION} to turn on or {GameOptionMapping.ALLOW_DUPLICATE_FALSE_OPTION} to leave off')
        return
    
    # customize sequence length
    def customize_sequence_length_caption(self, allow_duplicates: bool) -> None:
        '''
        print the caption when customizing sequence length

        :param allow_duplicates: the status of allow duplicates to pass to print_status func

        :return:
            None
        '''
        print()
        print('Input sequence length')
        print('Sequence length has to be higher than 0 and lower than 658 unless allow duplicates is on')
        self.print_status('allow_duplicates', allow_duplicates)
        return
    
    # making pool
    def make_pool_caption(self, pool_length_min: int, sequence_length: int, allow_duplicates: bool) -> None:
        '''
        print the start caption when cusotmizng the pool

        :param pool_length_min: the minimun of pool length to display to warn the player
        :param sequence_length: the length of the sequence to warn player
        :param allow_duplicates: the status of allow duplicates to be pass to print_all_dup_status func

        :return:
            None
        '''
        print()
        print('You are going to make a custom pool of characters for you to input and make sequence from')
        print()
        self.print_pool_avaliable()
        print()
        print('Type color full name, then the character spearated by a space')
        print('Colors can be apply to any character')
        print()
        print(f'Notice that amount of item of pool has to be higher than or equal to pool length minimum: {pool_length_min} and sequence length: {sequence_length}, unless allow duplicates is on')
        self.print_status('allow_duplicates', allow_duplicates)
        print()
        print(f'Input {GameOptionMapping.END_POOL_OPTION} when you are done, ')
        print(f'Input {GameOptionMapping.POOL_SINGLE_INPUT_SHOW_AVALIABLE_OPTION} for avaliable colors and characters')
        print(f'\"all\" is the wild card, Input {GameOptionMapping.POOL_SINGLE_INPUT_WILD_CARD_EXP_OPTION} to learn about the wild card')
        print('Input existing item to delete')
        return
    
    def make_pool_inputing_caption(self, pool_len: int) -> None:
        '''
        print the caption when player is inputing the pool item

        :param pool_len: the length of pool to tell player number item they are currently inputing

        :return:
            None
        '''
        print()
        print(f'Input item {pool_len + 1}')
        return
    
    def confirm_pool_caption(self, pool: List[str]) -> None:
        '''
        print the caption when confirming the pool inputed

        :param pool: the current pool to be pass to print_pool func

        :return:
            None
        '''
        print()
        self.confirm(f'Pool validated, Input {GameOptionMapping.CLEAR_OPTION} to reset pool or any key to continue')
        self.print_pool(pool, False)
        return
    
    def handle_pool_input_dupilcate_caption(self, item: str) -> None:
        '''
        print the duplicated item when inputing pool and tell player what can be done

        :param item: the duplicated item

        :return:
            None
        '''
        print()
        print(f'{self.error_message_color}Item: {item}{self.error_message_color} already exists. Type {GameOptionMapping.CLEAR_OPTION} to delete or any key to ignore{self.color_reset}')
        return
           
    # customize sequence creator
    def customize_mastermind_caption(self) -> None:
        '''
        print the option to customize mastermind

        :return:
            None
        '''
        print()
        print(f'Input {GameOptionMapping.COMPUTER_BRAIN_OPTION} for computer mastermind')
        print(f'Input {GameOptionMapping.HUMAN_BRAIN_OPTION} to human mastermind')
        return
    
    def cutomize_codebreaker_caption(self) -> None:
        '''
        print the option to customize the codebreaker's brain

        :return:
            None
        '''
        print()
        print(f'Input {GameOptionMapping.COMPUTER_BRAIN_OPTION} for computer code breaker')
        print(f'Input {GameOptionMapping.HUMAN_BRAIN_OPTION} for human code breaker')
        return
    
    def customize_codebreaker_name_caption(self) -> None:
        '''
        print the prompt for user to enter a name for the codebreaker

        :return:
            None
        '''
        print()
        print('Input a name for your codebreaker, or input an existing name')
        return
    
    # customzie sequence
    def customize_sequence_start_caption(self, sequence_length: int, pool: List[str], allow_duplicates: bool) -> None:
        '''
        print the start caption when customizing sequence

        :param sequence_length: the length of sequence to be printed
        :param pool: the current pool to be passed to print_pool func
        :param allow_duplicates: the status of allow duplicates to pass to print_allow_duplicates_status func

        :return:
            None
        '''
        print()
        print(f'Make a custom sequnece from the pool, sequence length: {sequence_length}')
        print('Notice that you cannot input the same item unless allow duplicates is turned on')
        self.print_status('allow_duplicates', allow_duplicates)
        print()
        print(f'Input the index of avaliable item on the left')
        self.print_pool(pool, True)
        return
        
    def customize_sequence_inputing_caption(self, inputing_item_num: int) -> None:
        '''
        print the caption when playering is inputing seuqnce

        :param inputing_item_num: the number of item player is inputing

        :return:
            None
        '''
        print()
        print(f'Input item {inputing_item_num} of sequence')
        return
    
    def print_sequence(self, sequence: List[str]) -> None:
        '''
        print the current sequence

        :param seuqence: the current sequence to be printed

        :return:
            None
        '''
        print('Sequence: ' + ' '.join(f'{item}{self.color_reset}' for item in sequence))
        return
    
    def confirm_sequence_caption(self, sequence: List[str]) -> None:
        '''
        print the confirm caption when finished customizing sequence

        :param sequence: list of all the item in the sequence to be pass to print_sequence func

        :return:
            None
        '''
        print()
        self.confirm(f'Sequence created. Input {GameOptionMapping.CLEAR_OPTION} to clear the inputed sequence or any key to continue')
        self.print_sequence(sequence)
        return
    
    # customize attempts
    def customize_attempts_caption(self) -> None:
        '''
        print the caption when player is customizing attempts

        :return:
            None
        '''
        print()
        print('Input attempts amount')
        print('Attempts amount has to be higher than 0')
        return
    
    # confirm settings
    def confirm_settings_caption(self, settings: Dict[str, Any]) -> None:
        '''
        the caption when confirming all the customized settings

        :param settings: the dict of settings, their name as key and value as value

        :return:
            None
        '''
        print()
        self.confirm('Customizing complete, Input \"c\" to reset the settings or any key to continue')
        print()
        print(f'Attempts: {settings["attempts"]}, Allow duplicates: {settings["repeating_letter"]}, Sequence length: {settings["sequence_length"]}')
        self.print_pool(settings['pool'], False)
        print(f'Sequence: created, Mastermind: {settings["mastermind"]}')
        print(f'Codebreaker: {settings["codebreaker"]}, Name: {settings["codebreaker_name"]}')
        return
    
    '''Playing'''
    
    def playing_input_color_start_caption(self, pool: List[str]) -> None:
        '''
        print the start caption when playing the actual mastermind game

        :param pool: the current pool to pass to print_pool func

        :return:
            None
        '''
        print()
        print('\nInput item index to the left of the item')
        print()
        self.print_pool(pool, True)
        return
    
    def AI_pause_caption(self):
        print()
        print('AI is thinking...')
    
    def playing_inputing_color_inputing_caption(self, inputed_num: int) -> None:
        '''
        print the caption when inputing guess

        :param inputed_num: the number of item the player is currently inputing

        :return:
            None
        '''
        print()
        print(f'Input item {inputed_num}')
        return
    

    def print_current_play_board(self, board_state: Dict[str, Any]) -> None:
        '''
        print the current play board where inputed sequences and ouputs are displayed

        :param board_state: the dict of all the states needed to print the board, name as key, value as value

        :return:
            None
        '''
        print()
        print(f'{board_state["attempts_left"]} attempts left')
        print()
        # if there is a result print the sequence otherwise print '_'
        if board_state["winner"]:
            print('\t' + ' '.join(f'{s}{self.color_reset}' for s in board_state["sequence"]) + ' \t' + 'output')
        else:
            print('\t' + '_ ' * board_state['sequence_length'] + '\t' + 'output')
        print()

        # print reversed for the bottom to be the start
        for i in reversed(range(board_state["attempts"])): # attempts ..... 0
            # if there is a output and input print it otherwise leave blank
            try:
                print(f'{i + 1}\t' + ' '.join(f'{color}{self.color_reset}' for color in board_state["player_inputs"][i]) +' \t' + ' '.join(f'{self.output_color_map[o]}o{self.color_reset}' for o in board_state["outputs"][i]))
            except IndexError:
                print(f'{i + 1}')
        print()
        return
    
    def playing_print_inputed(self, inputed: List[str]) -> None:
        '''
        print the current inputed items

        :param inputed: the current list of inputed items

        :return:
            None
        '''
        print('Inputed: ' + ' '.join(f'{item}{self.color_reset}' for item in inputed))
        return
    
    def confrim_playing_inputed(self, inputed: List[str], input_type: str) -> None:
        '''
        print the caption to confirm inputed 

        :param inputed: list of inputed items to pass to print_inputed func
        :param input type: who inputed this 

        :return:
            None
        '''
        print()
        if input_type == GameOptionMapping.HUMAN:
            self.confirm('Inputing complete, input "c" to clear inputed or any key to continue')
        elif input_type == GameOptionMapping.COMPUTER:
            self.confirm('AI has decided, input enter to continue')
        self.playing_print_inputed(inputed)
        return

    '''Ending'''
    def ending_start_caption(self, winner: str, winner_name:str, score: int) -> None:
        '''
        print the ending caption

        :param winner: the winner of the game
        :param score: the score of codebreaker if he wins
        :param winner_name: the name of the codebreaker

        :return:
            None
        '''
        print()
        print(f'{winner.capitalize()}', end='')
        if winner == GameResult.WINNER_CODEBREAKER:
            print(f': {winner_name}', end='')
        print(' wins')
        if winner == GameResult.WINNER_CODEBREAKER:
            print(f'Score: {score}')
        return

    def ending_inputing_caption(self) -> None:
        '''
        print the inputing caption when ending the game

        :return:
            None
        '''
        print()
        self.confirm('Would you like to go again? ')
        print(f'Input {GameOptionMapping.QUIT_OPTION} to quit or any key to continue')
        print(f'Input {GameOptionMapping.ENDING_RECUSTOMIZE_OPTION} to re-customize the game')
        print('Input enter to replay the game with the same settings')
        return