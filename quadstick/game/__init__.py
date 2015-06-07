'''
game/__init__.py - Python class for polling game controllers

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

from quadstick import QuadStick

class Game(QuadStick):

    def __init__(self, name, jsid=0, hidden=False):
        '''
        Creates a new Game object.
        '''
        QuadStick.__init__(self, name, hidden)

        # Support alt/pos-hold through repeated button clicks
        self.buttonstate = 0

    def _get_autopilot(self):

        return QuadStick._toggle_autopilot(self, self.joystick.get_button(self.autobutton))
            
    def _get_alt_hold(self):

        self._count()

        return self.buttonstate in [2,3,4]

    def _get_pos_hold(self):

        self._count()

        return self.buttonstate == 4

    def _count(self):
        
        if self.joystick.get_button(self.holdbutton):
            if self.buttonstate == 0:
                self.buttonstate = 1
            elif self.buttonstate == 2:
                self.buttonstate = 3
            elif self.buttonstate == 4:
                self.buttonstate = 5
        else:
            if self.buttonstate == 1:
                self.buttonstate = 2            
            elif self.buttonstate == 3:
                self.buttonstate = 4
            elif self.buttonstate == 5:
                self.buttonstate = 0
