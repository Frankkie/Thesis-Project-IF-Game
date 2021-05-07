

import os


def start_log(game):
    log_file_path = f"Games\\{game.title}\\log_commands.log"
    if os.path.exists(log_file_path):
        os.remove(log_file_path)
    else:
        pass


def log_command(game, command_text):
    log_file_path = f"Games\\{game.title}\\log_commands.log"
    with open(log_file_path, "a+") as file:
        file.write(command_text)
        file.write("\n")
    file.close()
    return

