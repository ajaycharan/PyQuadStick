'''
frsky.py - Support for FrSky R/C transmitters

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

from quadstick.axial.rc import RC

class Taranis(RC):
    '''
    Class for FrSky Taranis transmitter used with mini-USB cable.  
    You should set up channel mixing such that Channel 5 maps to Switch A and Channel 6 to Switch B.
    '''
 
    def __init__(self, jsid=0, hidden=False):
        '''
        Creates a new Taranis object.
        '''

        RC.__init__(self, 'Taranis', jsid, hidden)

        # Default to Linux 
        self.pitch_axis     = 2
        self.roll_axis      = 1
        self.yaw_axis       = 3
        self.throttle_axis  = 0
        self.switch_axis    = 4

        if self.platform == 'Windows':
            self.yaw_axis    = 5
            self.switch_axis = 3
            
        elif self.platform == 'Darwin':
            self.pitch_axis    = 0
            self.roll_axis     = 3
            self.yaw_axis      = 1
            self.throttle_axis = 2
            self.switch_axis   = 4

        self.pitch_sign = +1
        self.roll_sign  = -1
        self.yaw_sign   = +1

    def poll(self):
        '''
        Polls the Taranis R/C transmitter.

        Controls are Mode 2 (Left stick throttle / yaw; Right stick pitch / roll).

        Altitude hold: Switch A halfway down
        Position hold: Switch A completely down
        Autopilot:     Switch B down (overrides altitude / position hold)

        Returns demands (pitch, roll, yaw, throttle) and switches (pos-hold, alt-hold, autopilot).
        '''

        return RC._poll(self)

    def _convert_axis(self, index, value):

        return value

    def _get_alt_hold(self):

        switch = RC._get_axis(self, self.switch_axis)
        return switch > -1 and switch < +1

    def _get_pos_hold(self):

        return RC._get_axis(self, self.switch_axis) > 0.9

    def _get_autopilot(self):
        
        # XXX Autopilot currently not supported for Taranis.
        return False

class TH9X(RC):
    '''
    Class for FrSky TH9X transmitter used with Wailly PPM->USB cable.
    '''

    def __init__(self, jsid=0, hidden=False):
        '''
        Creates a new TH9X object.
        '''

        RC.__init__(self, 'TH9X', jsid, hidden)

    # Default to Linux 
        self.pitch_axis  = 1
        self.roll_axis   = 0
        self.yaw_axis    = 5
        self.throttle_axis  = 2
        self.switch_axis = 3

        if self.platform == 'Windows':
            self.yaw_axis    = 3
            self.switch_axis = 5

        elif self.platform == 'Darwin':
            self.pitch_axis  = 3
            self.roll_axis   = 2
            self.yaw_axis    = 1
            self.throttle_axis  = 0
            self.switch_axis = 4

        self.pitch_sign = +1
        self.roll_sign  = -1
        self.yaw_sign   = +1

    def poll(self):
        '''
        Polls the TH9X R/C transmitter.

        Controls are Mode 2 (Left stick throttle / yaw; Right stick pitch / roll).

        For altitude / position hold and autopilot, see 
        http://3drobotics.com/wp-content/uploads/2014/04/IRIS-Flight-Checklist-v5.pdf

        Returns demands (pitch, roll, yaw, throttle) and switches (pos-hold, alt-hold, autopilot).
        '''

        return RC._poll(self)

    def _convert_axis(self, index, value):

        maxval = 1

        if index == 0:
            maxval = 0.9
        elif index == 1:
            maxval = 0.8

        return value / 0.7125 if value < 0 else value / maxval

    def _get_alt_hold(self):

        switch = RC._get_axis(self, self.switch_axis) 

        return  switch > -0.3 and switch < 0.1

    def _get_pos_hold(self):

        switch = RC._get_axis(self, self.switch_axis) 

        return  switch >= 0 and switch < 0.2

    def _get_autopilot(self):

        return RC._get_axis(self, self.switch_axis) > 0.1
