#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
replay.py
"""

# Copyright 2021 Ball Aerospace & Technologies Corp.
# All Rights Reserved.
#
# This program is free software; you can modify and/or redistribute it
# under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; version 3 with
# attribution addendums as found in the LICENSE.txt


import ballcosmos


def replay_select_file(filename, packet_log_reader="DEFAULT"):
    return ballcosmos.CTS.write("replay_select_file", filename, packet_log_reader)


def replay_status():
    return ballcosmos.CTS.write("replay_status")


def replay_set_playback_delay(delay):
    return ballcosmos.CTS.write("replay_set_playback_delay", delay)


def replay_play():
    return ballcosmos.CTS.write("replay_play")


def replay_reverse_play():
    return ballcosmos.CTS.write("replay_reverse_play")


def replay_stop():
    return ballcosmos.CTS.write("replay_stop")


def replay_step_forward():
    return ballcosmos.CTS.write("replay_step_forward")


def replay_step_back():
    return ballcosmos.CTS.write("replay_step_back")


def replay_move_start():
    return ballcosmos.CTS.write("replay_move_start")


def replay_move_end():
    return ballcosmos.CTS.write("replay_move_end")


def replay_move_index(index):
    return ballcosmos.CTS.write("replay_move_index", index)
