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
        Creates a new RC object.
        '''
        Axial.__init__(self, name, jsid, hidden)

        # Empirically determined for Wailly cable + Frsky Taranis
        self.PITCH_RANGE    = -0.711365, +0.896881
        self.ROLL_RANGE     = -0.711365, +0.989685
        self.YAW_RANGE      = -0.711365, +0.958740
        self.THROTTLE_RANGE = -0.711365, +0.999969


    def _get_pitch(self):
    
        return self.pitch_sign * self._get_rc_axis(self.pitch_axis, self.PITCH_RANGE)

    def _get_roll(self):
    
        return self.roll_sign * self._get_rc_axis(self.roll_axis, self.ROLL_RANGE)

    def _get_yaw(self):

        return self.yaw_sign * self._get_rc_axis(self.yaw_axis, self.YAW_RANGE)
 
    def _get_throttle(self):
        
        return self._get_rc_axis(self.throttle_axis, self.THROTTLE_RANGE)

    def _get_rc_axis(self, value, valrange):
        
        value = Axial._get_axis(self, value) 

        if value > 0:
            value = value / valrange[1]
        if value < 0:
            value = value / abs(valrange[0])

        return value
