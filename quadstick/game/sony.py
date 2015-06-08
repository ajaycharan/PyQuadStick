'''
sony.py - Python class for Sony PlayStation 3 controller

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

class PS3(Game):

    def __init__(self, switch_labels):
        '''
        Creates a new PS3 object.
        '''
        Game.__init__(self, 'PS3', switch_labels)

        # Special handling for OS X
        self.switch_axis = 9 if self.platform == 'Darwin' else 7

        self.throttle = 0

        self.THROTTLE_INC = .001

    def _startup(self):

        return

    def _get_pitch(self):
    
        return Game._get_axis(self, 3)

    def _get_roll(self):
    
        return -Game._get_axis(self, 2)

    def _get_yaw(self):

        return Game._get_axis(self, 0)

    def _get_throttle(self):

        self.throttle -= self.THROTTLE_INC * Game._get_axis(self, 1)

        self.throttle = min(max(self.throttle, 0), 1)

        return self.throttle