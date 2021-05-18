

import os


def start_log(game):
    log_file_path = os.path.join('Games', game.title, "log_commands.log")
    if os.path.exists(log_file_path):
        os.remove(log_file_path)
    else:
        pass


def log_command(game, command_text):
    log_file_path = os.path.join('Games', game.title, "log_commands.log")
    with open(log_file_path, "a+") as file:
        file.write(command_text)
        file.write("\n")
    file.close()
    return


def log_time(game):
    log_file_path = os.path.join('Games', game.title, "log_commands.log")
    with open(log_file_path, "a+") as file:
        file.write(str(game.game_state['game time']))
        file.write("\n")
        file.write(str(game.game_state['chapter time']))
        file.write("\n")
    file.close()
    return


def log_seed(game):
    log_file_path = os.path.join('Games', game.title, "log_seed.log")
    with open(log_file_path, "w") as file:
        file.write(str(game.seed))
    file.close()
    return

