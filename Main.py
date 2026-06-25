from .constants import GameStages
from .Controller import MastermindGame

def main() -> None:
    '''
    the main function to run the whole game

    :return:
        None
    '''
    mg = MastermindGame()
    game_state = GameStages.STARTING
    while True:
        if game_state == GameStages.STARTING:
            game_state = mg.handle_start()
        elif game_state == GameStages.CUSTOMIZING:
            game_state = mg.handle_customization()
        elif game_state == GameStages.PLAYING:
            game_state = mg.handle_playing()
        elif game_state == GameStages.ENDING:
            game_state = mg.handle_ending()

if __name__ == "__main__":  
    main()