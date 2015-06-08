'''
quadstick/__init__.py - Python class for polling quadcopter flight-simulator controllers

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

import pygame
import pygame.locals
from platform import platform
import sys
import traceback
import os

class QuadStick(object):

    def __init__(self, name, switch_labels):
        '''
        Creates a new QuadStick object.
        '''

        # Set constants
        self.BAND = 0.2 # Must be these close to neutral for hold / autopilot

        # Init pygame
        pygame.init()
        pygame.display.init()
        
        self.screen = pygame.display.set_mode((500,280), pygame.locals.RESIZABLE)
        self.font = pygame.font.SysFont('Courier', 20)
        pygame.display.set_caption('QuadStick: ' + name)

        # Supports keyboard polling
        self.keys = []

        # Supports autopilot toggling for non-R/C controllers
        self.auto    = False
        self.toggled = False

        self.name = name

        self.platform = platform()[0:platform().find('-')]

        self.row_height = 30

        self.paused = False

        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        self.joystick.get_axis(0)

        # Enable sound
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
        datapath = os.path.abspath(os.path.dirname(__file__)) + '/data'
        self.sounds = []
        for k in range(10,110,10):
            self.sounds.append(pygame.mixer.Sound(datapath + ('/quadcopter%d.wav') % k))
        self.wantsound = False
        self.soundfile = -1

        self.ready = False

        self.switch_labels = switch_labels

    def __str__(self):
        '''
        Returns a string representation of this QuadStick object
        '''
        return self.name

    def _pump(self):

        pygame.event.pump()   


    def setVolume(self, volume):
        '''
        Sets volume for current motor sound if enabled.
        '''

        self.sounds[self.soundfile].set_volume(volume)

    def _startup(self):

        if not self.ready:

            self.message(self._startup_message())

            while True:
                self._pump()
                if self._get_throttle()  > .5:
                    break

            while True:
                self._pump()
                if self._get_throttle()  < .05 and self._get_switchval() == 0:
                    break

            self.clear()

            self.ready = True

    def poll(self):

        self._pump()

        self._startup()

        demands = self._get_pitch(), self._get_roll(), self._get_yaw(), self._get_throttle()

        if self.wantsound:

            # Modulate sound by throttle
            newfreq = int(10*demands[3])
            if newfreq != self.soundfile:
                FADE_MSEC = 400
                if self.soundfile >= 0:
                    self.sounds[self.soundfile].fadeout(FADE_MSEC)
                self.soundfile = newfreq
                self.sounds[self.soundfile].play(loops=-1, fade_ms=FADE_MSEC) # continuous loop

        switchval = self._get_switchval()

        self._show_demand(demands, 0, -1, 'Pitch')
        self._show_demand(demands, 1, -1, 'Roll')
        self._show_demand(demands, 2, +1, 'Yaw')
        self._show_demand(demands, 3, +1, 'Throttle') 
     
        self._show_switch(switchval, 0)
        self._show_switch(switchval, 1)
        self._show_switch(switchval, 2)

        pygame.display.flip()

        return demands[0], demands[1], demands[2], demands[3], switchval
 
    def running(self):
        '''
        Returns True if the QuadStick is running, False otherwise. Run can be terminated by hitting
        ESC.
        '''

        self.keys = pygame.event.get()

        for event in self.keys:

            if event.type == pygame.locals.QUIT:
                return False

            elif event.type == pygame.locals.VIDEORESIZE:
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.locals.RESIZABLE)

            elif (event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE):
                return False

        return True

    def clear(self):
        '''
        Clears the display.
        '''
        self.screen.fill((0,0,0))
 
    def error(self):
        '''
        Displays the most recent exception as an error message, and waits for ESC to quit.
        '''
        while True:

            self.clear()
            tb = traceback.format_exc()
            self._draw_label_in_row('ERROR', 0, color=(255,0,0))

            self._display(tb)

            pygame.display.flip()

            if not self.running():
                pygame.quit()
                sys.exit()

    def message(self, msg):
        '''
        Displays a message.
        '''
        self.clear()

        self._display(msg)

    def _display(self, msg):

        row = 1
        for line in msg.split('\n'):
            self._draw_label_in_row(line, row)
            row += 1

        pygame.display.flip()

    def _show_switch(self, switchval, index):

        x = 200
        y = 180 + index * 30
        r = 10

        # Draw a white ring around the button
        pygame.draw.circle(self.screen, (255,255,255), (x, y), r, 1)

        # Draw a white or black disk inside the ring depending on switch state
        pygame.draw.circle(self.screen, (255,255,255) if switchval == index else (0,0,0), (x, y), r-3)

        self._draw_label(self.switch_labels[index], y-10)

    def _show_demand(self, demands, index, sign, label):

        # color for no-demand baseline
        color = (0, 0, 255) 

        demand = sign * demands[index]

        if demand > 0:
            color =  (0, 255, 0)

        if demand < 0:
            color =  (255, 0, 0)

        w = 100			# width of rectangel for maximum demand
        h = 20

        x = 250
        y = 20 + index * 30

        # Erase previous 
        pygame.draw.rect(self.screen, (0,0,0), (x-w-1, y, x-w/2, h))

        # Draw a white hollow rectangle to represent the limits
        pygame.draw.rect(self.screen, (255,255,255), (x-w-1, y, x-w/2, h), 1)

        # Special handling for throttle
        if index == 3:
            x -= w
            w += w

        # Draw a colorful filled rectangle to represent the demand
        pygame.draw.rect(self.screen, color, (x, y, demand*w, h))

        # Draw a label for the axis
        self._draw_label(label, y)

    def _draw_label_in_row(self, text, row, color=(255,255,255)):

        self._draw_label(text, row*self.row_height, color)

    def _draw_label(self, text, y, color=(255,255,255)):

        surface = self.font.render(text, True, color, (0, 0, 0))
        surface.set_colorkey( (0, 0, 0) )
 
        self.screen.blit(surface, (20, y))
 

    def _toggle_autopilot(self, trigger):

        if trigger:
            if not self.toggled:
                self.auto = not self.auto
            self.toggled = True
        else:
            self.toggled = False

        return self.auto

    def _get_axis(self, k):

        return self.joystick.get_axis(k)

    def _get_button(self, k):

        return self.joystick.get_button(k)

    def _get_alt_hold(self):

        return self._get_alt_hold_request() and self._neutral_sticks()

    def _get_pos_hold(self):

        return self._get_pos_hold_request() and self._neutral_sticks()

    def _neutral_sticks(self):

        return self._safeband(self._get_throttle(), 0.5) and \
                self._safestick(self._get_pitch()) and \
                self._safestick(self._get_roll()) and \
                self._safestick(self._get_yaw())

    def _safestick(self, value):

        return self._safeband(value, 0)

    def _safeband(self, value, middle):

        return value > (middle-self.BAND) and value < (middle+self.BAND)
