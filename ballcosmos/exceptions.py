#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
exceptions.py
"""


class BallCosmosError(RuntimeError):
    pass


class BallCosmosConnectionError(BallCosmosError):
    pass


class BallCosmosRequestError(BallCosmosError):
    pass


class BallCosmosResponseError(BallCosmosError):
    pass
