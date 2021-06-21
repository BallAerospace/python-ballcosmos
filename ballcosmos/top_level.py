#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
top_level.py
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

USERPATH = None


def define_user_path(start_dir=os.getcwd()):
    global USERPATH
    """Searches for the file userpath.txt to define the USERPATH constant

    @param start_dir [String] Path to start the search for userpath.txt. The
      search will continue by moving up directories until the root directory is
      reached.
    """
    current_dir = os.path.abspath(start_dir)
    while True:
        if os.path.isfile("/".join([current_dir, "userpath.txt"])):
            USERPATH = current_dir
            break
        else:
            old_current_dir = current_dir
            current_dir = os.path.abspath("/".join([current_dir, ".."]))
            if old_current_dir == current_dir:
                # Hit the root dir - give up
                break


#############################################################################
# This code is executed in place when this file is imported

# First attempt try from the location of the executable ($0)
# Note this method will fail when a intermediary executable is used like rcov
define_user_path(os.path.dirname(sys.argv[0]))
if USERPATH is None:
    # Second attempt try from location of the current working directory
    define_user_path(os.getcwd())
    if USERPATH is None:
        # Last chance - Check environment
        try:
            USERPATH = os.environ["COSMOS_USERPATH"]
        except Exception:
            USERPATH = os.path.abspath("/".join([os.path.dirname(sys.argv[0]), ".."]))
