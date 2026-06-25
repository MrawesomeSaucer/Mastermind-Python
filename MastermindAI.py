
import random
import time
from typing import *
from .constants import GameResult

'''
AI/algorithm explaination

First Step:
There will be a dictionary containing all the possible guess as key, and there possible positions as value. 
These guesses are tried in order and so as their possible positions.

Example:
dictionary: {red:[1, 2, 3, 4, 5, 6], green: [1, 2, 3, 4, 5, 6], purple:[1, 2, 3, 4, 5, 6], blue:[1, 2, 3, 4, 5, 6], white:[1, 2, 3, 4, 5, 6], black:[1, 2, 3, 4, 5, 6]}

red is first, is the dictionary, so is its first possible position, which is one, so red is placed in index 1
green is second, index 1 is already taken, so the next possible position is 2. green will be placed on index 2

From there each possible guess will be place until the move is complete

If the sequence lenght is 4, the current move will be: red green purple blue

Second Step:
Based on each output, possible guesses and possible positions of each guess is modified.
A black output means that the guess is not present in the sequence if there is only one of them tried; 
if 2 or more is tried it could only mean that this possibe move cannot be in this position.
this index is removed from the guess' possible positions

A white output means that the guess is not in the correct spot but in the sequence.
This tried spot is removed from the guess' possible positions


A red return means the guess correct, which means that the spot can be locked in and no longer needed to be tried; a list will stroe the confirmed guesses.
The correct spot will also be removed from other guesses' possible positions as other guesss no longer need to be tried there.
If allow duplicates is off, this guess also can be completely removed from the dictionary.

Example:
from the first step, the input is red green purple blue

lets say the output is red white white black

red is correct so lock in the possition, and also remove this index from other guesses to prevent them from trying this spot. 
modification from this guess: remove index 1 from all the guesses. if allow_duplicates is off, remove it from the dictionary

green and purple are in the sequence but in the wrong spot
modification from these guesses: remove index 2 from green and index 3 from purple

blue results a black, since there is only one of them we remove it from the dictionary completely as it is not in the sequence
modification from this guess: remove blue from the dictionary

modified dictionary: {green: [3, 4, 5, 6], purple:[2, 4, 5, 6], white:[2, 3, 4, 5, 6], black:[2, 3, 4, 5, 6]}

Step Three:
base on the new modifed dictionary, make a new move

red goes first as it is locked into the position
green goes to third as it is the first index
purple goes second
white goes 4th

Second complete guess: red purple green white

Reminder:
This ai only work in this modified version of mastermind, which each output correspond to a input. In real mastermind, output only show amount of red, black, or white this output result in.
Another version of AI can be made for regular version of mastermind by creating a list of all the possible guesses and deducting them from the output.
'''

class AI:
    '''
    A class to hold the AI
    '''
    def __init__(self):
        self.p_moves = {}
        
        self.fixed_moves = []

    def AI_initiate(self, pool: List[str], sequence_length: int) -> None:
        '''
        Initiate the AI, use this instead of __init__ because this can also act as a reset for the AI

        :param pool: the current pool to create the list of possible guesses
        :param sequence_lenght: the sequence length to create the list of possible possitions

        :return:
            None
        '''
        self.p_moves = {}
        
        # create p_moves containing all the possible guesses and their possible positions
        for item in pool:
            # at the start the possible guess and possible positions is everything
            self.p_moves[item] = list(range(sequence_length))
        
        # fixed moves to store all the correct moves
        self.fixed_moves = [None for _ in range(sequence_length)]

        return
        
    def AI_modify_p_move_remove_correct_spot(self) -> None:
        '''
        remove the guessed correct spot's index fromm the rest of the guesses' possible positions

        :return:
            None
        '''
        for index, f_move in enumerate(self.fixed_moves):
            # remove the fixed moves index from the other p_positions
            for p_move in self.p_moves:
                p_index = self.p_moves[p_move]
                if f_move is not None and index in p_index:
                    p_index.remove(index)

        return

    def AI_modify_p_moves(self, allow_duplicates: bool, attempt_in_question: List[str], output: List[str]) -> None:
        '''
        modify the p_positions based on output

        :param allow_duplicates: a corrent output remove the guess from p_moves if allow_duplicates is off
        :param attempt_in_question: the move that resulted in the output
        :param output: the output produced by the input

        :return:
            None
        '''
        for index, o in enumerate(output):
            # the x index of return relates to the x index of attempt 
            current_move_of_attempt_in_question = attempt_in_question[index]

            if current_move_of_attempt_in_question not in self.p_moves:
                continue
            
            current_move_of_attempt_possible_index = self.p_moves[current_move_of_attempt_in_question]

            if o == GameResult.WRONG:
                # if only one input is present and it result in wrong, delete from p_moves
                if attempt_in_question.count(current_move_of_attempt_in_question) == 1:
                    del self.p_moves[current_move_of_attempt_in_question]
                    continue
                    
                # else remove the index as it only means it is not in this spot
                if index in current_move_of_attempt_possible_index:
                    current_move_of_attempt_possible_index.remove(index)
 
            elif o == GameResult.PARTIAL:
                # 'partial' means can not be in that position in future, remove that index from the possible index
                if index in current_move_of_attempt_possible_index:
                    current_move_of_attempt_possible_index.remove(index)

            elif o == GameResult.CORRECT:
                # if allow duplcates is false it means that the guess can be remove from p_moves
                if allow_duplicates is False:
                    del self.p_moves[current_move_of_attempt_in_question]

                # 'correct' will move the item to the fixed moves list 
                self.fixed_moves[index] = current_move_of_attempt_in_question

        # remove corrent indexies from the rest
        self.AI_modify_p_move_remove_correct_spot()
        return

    def AI_make_current_move_list(self, sequence_length: int) -> List[Optional[str]]:
        '''
        premake a list with all the spot to add on to and become the complete move later, add fixed moves' move on there as well

        :param sequence_length: tell how many spot to make

        :return:
            The remade list
        '''
        # [None, None, None ...]
        current_planned_move = [None for _ in range(sequence_length)]
        
        # add fixed moves if any
        for index, fixed_move in enumerate(self.fixed_moves):
            if fixed_move is not None:
                current_planned_move[index] = fixed_move

        return current_planned_move

    def AI_make_move(self, sequence_length: int, pool: List[str], allow_duplicates: bool, attempts_amount: int) -> List[str]:
        '''
        seperate the delay and the actual make move function

        :param sequence_length: pass to actual make_move func
        :param pool: pass to actual make move func
        :param allow_duplicates: pass to actual make move func

        :return:
            the complete move
        '''
        current_move_list = self.make_move(sequence_length, pool, allow_duplicates)

        # add delay to prevent AI from instantly making the move
        time.sleep(self.get_pause_time(attempts_amount))

        return current_move_list
    
    def make_move(self, sequence_length: int, pool: List[str], allow_duplicates: bool) -> List[str]:
        '''
        make the move using logical order, use fall back func to complete if None is present

        :param sequence_length: pass to AI_make_current_move_list func
        :param pool: pass to fall_back func
        :param allow_duplicates: pass to fall_back func

        :return:
            the complete move
        '''
        # make a list of place holders
        current_move_list = self.AI_make_current_move_list(sequence_length)

        # for each guess, its index is checked in order
        for p_guess in self.p_moves:
            # indexies are the value of the guess
            p_index = self.p_moves[p_guess]
            for index in p_index:
                # check the possible position, if it is taken skip it
                p_position = current_move_list[index]
                if p_position is None:
                    current_move_list[index] = p_guess
                    break
        
        # sometime None can be present in a list because of the way it is went over in the order of p_moves
        # fall back function will correct it if there is None in the move
        if None in current_move_list:
            current_move_list = self.fall_back(current_move_list, pool, allow_duplicates)

        return current_move_list

    def check_common_items(self, l1: List[Any], l2: List[Any]) -> Tuple[bool, Optional[Any]]:
        '''
        helper function for fall back, check if the two list have any items in common

        :param l1: the first list
        :param l2: the second list

        :return:
            bool: whether the two list have item in common
            Optional[Any]: None if no item is in common, else the first common item
        '''
        for l1_indedx in l1:
            for l2_index in l2:
                if l1_indedx == l2_index:
                    return True, l2_index
        
        return False, None
    
    def get_moves_not_in_current_move_list(self, current_move_list: List[Optional[str]])  -> List[Optional[str]]:
        '''
        helper func for fall back, check for guesses that is not present in the current move

        :param current_move_list: the list of moves to check
        
        :return:
            the item not in move list if there is any
        '''
        l = []
        for p_guess in self.p_moves:
            if p_guess not in current_move_list:
                l.append(p_guess)

        return l

    def get_none_index_in_current_move_list(self, current_move_list: List[Optional[str]]) -> List[int]:
        '''
        helper func for fall back, get a list of the None postions in the current move list for fall back

        :param current_move_list: the list of moves to check for None

        :return:
            the list of all the positions of None in the list
        '''
        indexies = []

        for index, item in enumerate(current_move_list):
            # add the position to the list if it is None
            if item is None:
                indexies.append(index)

        return indexies

    def fall_back_first_check(self, current_move_list: List[Optional[str]], guess_just_moved: str, allow_duplicates: bool) -> Tuple[List[Optional[str]], Optional[str]]:
        '''
        first check of fall back, check for any item in the list that can move into the None spot

        :param current_move_list: the current moves
        :param guess_just_moved: the moved that just went into None spot, to prevent moving the same item and looping
        :param allow_duplicates: status of allow_duplicates, if it is false we don't look at moves in fixed_moves

        :return:
            List[Optioanl[str]]: the modified move list
            Optional[str]: guess the just got tried, stay None if no move got moved
        '''
        none_indexies_in_current_move_list = self.get_none_index_in_current_move_list(current_move_list)
        for index, guess in enumerate(current_move_list):
            
            # skip move that is None and just moved
            if guess is None:
                continue

            if guess == guess_just_moved:
                continue
            
            # skip fixed moves if allow_duplicates is False
            if allow_duplicates is False and guess in self.fixed_moves:
                continue

            # check None avaliablity
            guess_indexies = self.p_moves[guess]
            success, success_index = self.check_common_items(guess_indexies, none_indexies_in_current_move_list)

            if not success:
                continue

            # swap spot
            current_move_list[index] = None
            current_move_list[success_index] = guess
            guess_just_moved = guess

            return current_move_list, guess_just_moved
        
        return current_move_list, guess_just_moved
    
    def fall_back_second_check(self, current_move_list: List[Optional[str]]) -> List[Optional[str]]:
        '''
        second check of fall back, check if moves not present in the list can go into spot left by moves that went to None spot

        :param current_move_list: the modified current_move_list

        :return:
            the modified current_move_list
        '''
        none_indexies_in_current_move_list = self.get_none_index_in_current_move_list(current_move_list)
        items_not_in_list = self.get_moves_not_in_current_move_list(current_move_list)
        for item in items_not_in_list:

            item_index = self.p_moves[item]

            success, success_index = self.check_common_items(item_index, none_indexies_in_current_move_list)

            if not success:
                continue

            current_move_list[success_index] = item
            return current_move_list

        return current_move_list
    
    def fall_back_add_random_item(self, current_move_list: List[Optional[str]], pool: List[str]) -> List[str]:
        '''
        last resort of fall back, add a random item if move list didn't get modified (both fall back check failed)

        :param current_move_list: the move list
        :param pool: the pool to select a random item from

        :return:
            the modified move list
        '''
        for index, item in enumerate(current_move_list):
            if item is not None:
                continue

            current_move_list[index] = random.choice(pool)

        return current_move_list

    def fall_back(self, current_move_list: List[Optional[str]], pool: List[str], allow_duplicates: bool) -> List[str]:
        '''
        fall back func to combine check 1 and check 2 and plan B

        :param current_move_list: the move list to pass on
        :param pool: the pool to pass the add_random_item
        :param allow_duplicates: the status of allow_duplicates to pass on

        :return:
            the modified move list
        '''
        guess_just_moved = None
        while None in current_move_list:
            # compare unmodified move list and modified move list
            before = current_move_list

            # check 1 and check 2
            current_move_list, guess_just_moved = self.fall_back_first_check(current_move_list, guess_just_moved, allow_duplicates)

            current_move_list = self.fall_back_second_check(current_move_list)

            # if stay the same add random item
            if current_move_list == before:
                current_move_list = self.fall_back_add_random_item(current_move_list, pool)

        return current_move_list
    
    def get_pause_time(self, attempts_amount: int) -> float:
        '''
        get AI pause time based on the # of attempts

        :param attempts_amount: use to determine pause time

        :return:
            pause time
        '''
        pause_time = 0
        if attempts_amount <= 10:
            pause_time = 2
        elif attempts_amount <= 100:
            pause_time = 0.1
        else:
            pause_time = 0

        return pause_time