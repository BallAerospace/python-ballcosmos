#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
scripting.py
"""

# Copyright 2021 Ball Aerospace & Technologies Corp.
# All Rights Reserved.
#
# This program is free software; you can modify and/or redistribute it
# under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; version 3 with
# attribution addendums as found in the LICENSE.txt


import os
import sys
from ballcosmos.extract import convert_to_value

PWD = os.path.dirname(os.path.abspath(__file__))


def play_wav_file(wav_filename):
    """ """
    raise NotImplementedError()


def status_bar(message):
    """ """
    raise NotImplementedError()


def ask_string(question, blank_or_default=False, password=False):
    """ """
    answer = ""
    default = ""
    if blank_or_default is not True and blank_or_default is not False:
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
    """ """
    string = ask_string(question, blank_or_default, password)
    value = convert_to_value(string)
    return value


def prompt(string):
    """ """
    prompt_to_continue(string)


def message_box(string, *buttons):
    """ """
    prompt_message_box(string, buttons)


def vertical_message_box(string, *buttons):
    """ """
    prompt_vertical_message_box(string, buttons)


def combo_box(string, *options):
    """ """
    prompt_combo_box(string, options)


def _file_dialog(message, directory, select_files=True):
    """ """
    answer = ""
    files = (
        []
        if not select_files
        else [
            f
            for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f))
        ]
    )
    prpt = "\n".join([message, "\n".join(files), "<Type file name>: "])
    while not answer:
        answer = input(prpt)
    return answer


def save_file_dialog(directory=PWD, message="Save File"):
    """ """
    _file_dialog(message, directory)


def open_file_dialog(directory=PWD, message="Open File"):
    """ """
    _file_dialog(message, directory)


def open_files_dialog(directory=PWD, message="Open File(s)"):
    """ """
    _file_dialog(message, directory)


def open_directory_dialog(directory=PWD, message="Open Directory"):
    """ """
    _file_dialog(message, directory, False)


def prompt_for_hazardous(target_name, cmd_name, hazardous_description):
    """ """
    message_list = [
        "Warning: Command {:s} {:s} is Hazardous. ".format(target_name, cmd_name)
    ]
    if hazardous_description:
        message_list.append(" >> {:s}".format(hazardous_description))
    message_list.append("Send? (y/N): ")
    answer = input("\n".join(message_list))
    try:
        return answer.lower()[0] == "y"
    except IndexError:
        return False


def prompt_for_script_abort():
    """ """
    answer = input("Stop running script? (y/N): ")
    try:
        if answer.lower()[0] == "y":
            sys.exit(66)  # execute order 66
    except IndexError:
        return False


def prompt_to_continue(string):
    """ """
    return input("{:s}: ".format(string))


def prompt_message_box(string, buttons):
    """ """
    return input("{:s} ({:s}): ".format(string, ", ".join(buttons)))


def prompt_vertical_message_box(string, options):
    """ """
    prompt_message_box(string, options)


def prompt_combo_box(string, options):
    """ """
    prompt_message_box(string, options)
