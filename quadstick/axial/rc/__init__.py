'''
rc/__init__.py - Python class for polling R/C transmitters using 
                 Wailly PPM-to-USB cable.

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

from quadstick.axial import Axial
import os

import pygame

class RC(Axial):

    def __init__(self, name, jsid=0, hidden=False):
        '''
        Creates a new RC object.  To use this with a real R/C transmitter, you should:

        (1) Move all sticks to center, run qstest.py, and adjust the trims to get a centered (blue) readout.

        (2) If necessary, adjust the self.AXIS_MIN value below to compensate inadequate minimum value.
        '''
        Axial.__init__(self, name, jsid, hidden)

        # Empirically determined for Wailly cable + Frsky Taranis
        self.AXIS_MIN = -0.711365

    def _get_pitch(self):

        return self.pitch_sign * self._get_rc_axis(self.pitch_axis)

    def _get_roll(self):
    
        return self.roll_sign * self._get_rc_axis(self.roll_axis)
        

    def _get_yaw(self):

        return self.yaw_sign * self._get_rc_axis(self.yaw_axis)

    def _get_throttle(self):
        
        return self._get_rc_axis(self.throttle_axis)

    def _get_rc_axis(self, index):
        
        value = Axial._get_axis(self, index) 
 
        return value/abs(self.AXIS_MIN) if value < 0 else value
