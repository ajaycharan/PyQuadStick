'''
rc/__init__.py - Python class for polling R/C transmitters

    Copyright (C) 2014 Simon D. Levy

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as 
    published by the Free Software Foundation, either version 3 of the 
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

'''

from quadstick.game import Game
import os

import pygame

class RC(Game):

    def __init__(self, name, jsid=0, hidden=False):
        '''
        Creates a new RC object.  Each subclass must implement the _convert_axis method.
        '''
        Game.__init__(self, name, jsid, hidden)

    def _get_pitch(self):

        return self.pitch_sign * self._get_rc_axis(self.pitch_axis)

    def _get_roll(self):
    
        return self.roll_sign * self._get_rc_axis(self.roll_axis)

    def _get_yaw(self):

        return self.yaw_sign * self._get_rc_axis(self.yaw_axis)

    def _get_throttle(self):
        
        return self._get_rc_axis(self.throttle_axis)

    def _get_rc_axis(self, index):
        
        return self._convert_axis(index, Game._get_axis(self, index))
