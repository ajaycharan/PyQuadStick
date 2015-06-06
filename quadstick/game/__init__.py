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

        # Support non-centering throttle stick for display
        self._throttle_factor = 1

        # Support alt/pos-hold through repeated button clicks
        self.buttonstate = 0

    def _get_autopilot(self, button):

        return QuadStick._toggle_autopilot(self, self.joystick.get_button(button))
            

