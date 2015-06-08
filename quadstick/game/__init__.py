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

    def __init__(self, name, switch_labels):
        '''
        Creates a new Game object.
        '''
        QuadStick.__init__(self, name, switch_labels)

        # Support alt/pos-hold through repeated button clicks
        self.buttonstate = 0

    def _get_switchval(self):

        if self.joystick.get_button(0):
            if self.buttonstate == 0:
                self.buttonstate = 1
            elif self.buttonstate == 2:
                self.buttonstate = 3
            elif self.buttonstate == 4:
                self.buttonstate = 5
        else:
            if self.buttonstate == 1:
                self.buttonstate = 2            
                retval = 1
            elif self.buttonstate == 3:
                self.buttonstate = 4
                retval = 2
            elif self.buttonstate == 5:
                self.buttonstate = 0

        return [0,1,1,1,2,0][self.buttonstate]
