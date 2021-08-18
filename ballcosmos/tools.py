#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
tools.py
"""

# Copyright 2021 Ball Aerospace & Technologies Corp.
# All Rights Reserved.
#
# This program is free software; you can modify and/or redistribute it
# under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; version 3 with
# attribution addendums as found in the LICENSE.txt

import ballcosmos

###########################
# Telemetry Screen methods
###########################

# Get the organized list of available telemetry screens
def get_screen_list(config_filename=None, force_refresh=False):
    return ballcosmos.CTS.write("get_screen_list", config_filename, force_refresh)


# Get a specific screen definition
def get_screen_definition(screen_full_name, config_filename=None, force_refresh=False):
    return ballcosmos.CTS.write(
        "get_screen_definition", screen_full_name, config_filename, force_refresh
    )
