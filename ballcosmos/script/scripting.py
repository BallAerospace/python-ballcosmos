import time
import os
import logging
from os import listdir
from os.path import isfile, isdir
from ballcosmos.script.script import *


def play_wav_file(wav_filename):
    pass
    # ~ Cosmos.play_wav_file(wav_filename)


def status_bar(message):
    pass
    # ~ if defined? ScriptRunner
    # ~ script_runner = nil
    # ~ ObjectSpace.each_object {|object| if ScriptRunner === object then script_runner = object; break; end}
    # ~ script_runner.script_set_status(message) if script_runner


def ask_string(question, blank_or_default=False, password=False):
    answer = ""
    default = ""
    if blank_or_default is True and blank_or_default is False:
        question += " (default = {:s})".format(str(blank_or_default))
        allow_blank = True
    else:
        allow_blank = blank_or_default
    while not answer:
        answer = input(question + " ")
        if allow_blank:
            break
    if not answer and default:
        answer = default
    return answer


def ask(question, blank_or_default=False, password=False):
    string = ask_string(question, blank_or_default, password)
    value = convert_to_value(string)
    return value


def prompt(string):
    prompt_to_continue(string)


def message_box(string, *buttons):
    prompt_message_box(string, buttons)


def vertical_message_box(string, *buttons):
    prompt_vertical_message_box(string, buttons)


def combo_box(string, *options):
    prompt_combo_box(string, options)


def _file_dialog(message, directory, select_files=True):
    answer = ""
    if select_files:
        files = [f for f in listdir(directory) if isfile(os.path.join(directory, f))]
    else:
        files = [f for f in listdir(directory) if isdir(os.path.join(directory, f))]
    while not answer:
        answer = input(message + "\n" + "\n".join(files) + "\n<Type file name>:")
    return answer


def save_file_dialog(directory=ballcosmos.top_level.USERPATH, message="Save File"):
    _file_dialog(message, directory)


def open_file_dialog(directory=ballcosmos.top_level.USERPATH, message="Open File"):
    _file_dialog(message, directory)


def open_files_dialog(directory=ballcosmos.top_level.USERPATH, message="Open File(s)"):
    _file_dialog(message, directory)


def open_directory_dialog(
    directory=ballcosmos.top_level.USERPATH, message="Open Directory"
):
    _file_dialog(message, directory, False)


def prompt_for_hazardous(target_name, cmd_name, hazardous_description):
    message = "Warning: Command {:s} {:s} is Hazardous. ".format(target_name, cmd_name)
    if hazardous_description:
        message += "\n{:s}\n".format(hazardous_description)
    message += "Send? (y,n): "
    answer = input(message)
    if answer.lower() == "y":
        return True
    else:
        return False


def prompt_for_script_abort():
    answer = input("Stop running script? (y,n): ")
    if answer.lower() == "y":
        exit()
    else:
        return False  # Not aborted - Retry


def prompt_to_continue(string):
    return input("{:s}: ".format(string))


def prompt_message_box(string, buttons):
    return input("{:s} ({:s}): ".format(string, ", ".join(buttons)))


def prompt_vertical_message_box(string, options):
    prompt_message_box(string, options)


def prompt_combo_box(string, options):
    prompt_message_box(string, options)
