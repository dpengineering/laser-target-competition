from random import random
from timeit import timeit

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window




from datetime import datetime
from time import time, time_ns

from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel
from pidev.kivy.ImageButton import ImageButton
from pidev.kivy import DPEAButton # I know these are grey buts it's required trust me

time = time



screen_manager = ScreenManager()
target_screen_name = 'target'
player_screen_name = 'player'


class LaserTargetCompetitionUI(App):
    """
        Handles running the app
    """

    def build(self):
        return screen_manager


Window.clearcolor = (0, 0, 0, 1)


class PlayerScreen(Screen):
    """
        Class to handle player screen
    """

    def right_button_pressed(self):
        print("Left button pressed")


    def left_button_pressed(self):
        print("Right button pressed")


    @staticmethod
    def transition_to_target_screen():
        screen_manager.transition.direction = "left"
        screen_manager.current = target_screen_name



class TargetScreen(Screen):
    """
        Class to handle a mini target clicker
        that simulates the lasers hitting targets
    """

    def __init__(self, **kwargs):
        """
        Loads the TargetScreen.kv file instead of having everything in main.kv
        Supers Screen's __init__
        **kwargs is normal kivy.uix.screenmanager.Screen attributes
        """

        self.target_hits = None
        self.targets_are_in = None
        Builder.load_file('TargetScreen.kv')

        super(TargetScreen, self).__init__(**kwargs)
        self.clock_scheduled = False
        self.time_start = time_ns()
        self.time_s = None
        self.targets = False
        self.points = 0
        self.state = "idle"
        self.off_screen = None
        self.targets_hit = None


    def start(self):
        print("Starting target game - setting state to targets")
        self.state = "targets"
        self.ids.start.x = self.width + 300
        self.schedule_clock()
        self.time_start = time_ns()
        self.time_s = 0
        self.targets = True
        self.points = 0
        self.targets_are_in = [False, False, False, False]
        self.target_hits = [False, False, False, False]
        self.targets_hit = 0

    def end(self):
        print("running end")
        self.state = "idle"
        self.ids.start.center_x = 400
        self.update_time_left_image(15)




    def update_all(self, dt=None): # dt for clock scheduling
        print(f"targets_hit={self.targets_hit}")
        self.update_time_left_image(self.update_time_left())

        if screen_manager.current == target_screen_name:
            if self.targets and self.targets_hit < 4:
                self.move_targets()
                print("moving target in")
            elif self.time_s <= 0 or self.targets_hit == 4:
                self.clock_scheduled = False
                self.end()

        return self.clock_scheduled

    def schedule_clock(self):
        if not self.clock_scheduled:
            Clock.schedule_interval(self.update_all, 0)
            self.clock_scheduled = True
        else:
            self.clock_scheduled = False

    def update_time_left(self):
        #print(f"Updating Label, Time {self.time_s}")
        self.time_s = -round((time_ns() / 1000000000) - (self.time_start / 1000000000 + 16))
        return self.time_s

    def update_time_left_image(self, num):
        print("updating time left")
        print(f"num={num}")
        on_screen = 800 - 64 - 8
        self.off_screen = 800 + 64
        if num == 0:
            self.end()
            self.ids.timer_1.x = self.off_screen
            self.ids.timer_0.x = on_screen
        elif num == 1:
            self.ids.timer_2.x = self.off_screen
            self.ids.timer_1.x = on_screen
        elif num == 2:
            self.ids.timer_3.x = self.off_screen
            self.ids.timer_2.x = on_screen
        elif num == 3:

            self.ids.timer_4.x = self.off_screen
            self.ids.timer_3.x = on_screen
        elif num == 4:

            self.ids.timer_5.x = self.off_screen
            self.ids.timer_4.x = on_screen
        elif num == 5:

            self.ids.timer_6.x = self.off_screen
            self.ids.timer_5.x = on_screen
        elif num == 6:
            self.ids.timer_7.x = self.off_screen
            self.ids.timer_6.x = on_screen
        elif num == 7:
            self.ids.timer_8.x = self.off_screen
            self.ids.timer_7.x = on_screen
        elif num == 8:
            self.ids.timer_9.x = self.off_screen
            self.ids.timer_8.x = on_screen
        elif num == 9:
            self.ids.timer_10.x = self.off_screen
            self.ids.timer_9.x = on_screen
        elif num == 10:
            self.ids.timer_11.x = self.off_screen
            self.ids.timer_10.x = on_screen
        elif num == 11:
            self.ids.timer_12.x = self.off_screen
            self.ids.timer_11.x = on_screen
        elif num == 12:
            self.ids.timer_13.x = self.off_screen
            self.ids.timer_12.x = on_screen
        elif num == 13:
            self.ids.timer_14.x = self.off_screen
            self.ids.timer_13.x = on_screen
        elif num == 14:
            self.ids.timer_15.x = self.off_screen
            self.ids.timer_14.x = on_screen
        else:
            self.ids.timer_1.x = self.off_screen
            self.ids.timer_2.x = self.off_screen
            self.ids.timer_3.x = self.off_screen
            self.ids.timer_4.x = self.off_screen
            self.ids.timer_5.x = self.off_screen
            self.ids.timer_6.x = self.off_screen
            self.ids.timer_7.x = self.off_screen
            self.ids.timer_8.x = self.off_screen
            self.ids.timer_9.x = self.off_screen
            self.ids.timer_10.x = self.off_screen
            self.ids.timer_11.x = self.off_screen
            self.ids.timer_12.x = self.off_screen
            self.ids.timer_13.x = self.off_screen
            self.ids.timer_14.x = self.off_screen
            self.ids.timer_15.x = on_screen



    def move_targets(self):
        print("moving targets")
        rand_128 = round(random() * 64)
        rand_x = round(random() * 700)
        rand_y = round(random() * 400)

        print(f"rand_128={rand_128}rand_x={rand_x}rand_y={rand_y}")

        if rand_128 == 1 and not self.target_hits[0]:
            self.ids.target_1.x = rand_x
            self.ids.target_1.y = rand_y
            self.targets_are_in[0] = True
        if rand_128 == 2 and not self.target_hits[1]:
            self.ids.target_2.x = rand_x
            self.ids.target_2.y = rand_y
            self.targets_are_in[1] = True
        if rand_128 == 3 and not self.target_hits[2]:
            self.ids.target_3.x = rand_x
            self.ids.target_3.y = rand_y
            self.targets_are_in[2] = True
        if rand_128 == 4 and not self.target_hits[3]:
            self.ids.target_4.x = rand_x
            self.ids.target_4.y = rand_y
            self.targets_are_in[3] = True



    def target_hit(self, target_num):
        pedestal_x = 0
        pedestal_y = 600 - 64
        if self.state == "targets":
            self.targets_hit += 1
            print(f"Target {target_num} Hit!")
            self.points += 100
            if self.points == 100:
                pedestal_x = 0
            elif self.points == 200:
                pedestal_x = 64
            elif self.points == 300:
                pedestal_x = 128
            elif self.points == 400:
                pedestal_x = 128 + 64
            match target_num:
                case 1:
                    self.target_hits[0] = True
                    self.ids.target_1.x = pedestal_x
                    self.ids.target_1.y = pedestal_y
                case 2:
                    self.target_hits[1] = True
                    self.ids.target_2.x = pedestal_x
                    self.ids.target_2.y = pedestal_y
                case 3:
                    self.target_hits[2] = True
                    self.ids.target_3.x = pedestal_x
                    self.ids.target_3.y = pedestal_y
                case 4:
                    self.target_hits[3] = True
                    self.ids.target_4.x = pedestal_x
                    self.ids.target_4.y = pedestal_y


    @staticmethod
    def transition_to_player_screen():
        screen_manager.transition.direction = "right"
        screen_manager.current = player_screen_name




Builder.load_file('main.kv')
screen_manager.add_widget(PlayerScreen(name=player_screen_name))
screen_manager.add_widget(TargetScreen(name=target_screen_name))


if __name__ == "__main__":

    # Window.fullscreen = 'auto' #uncomment this when actually loading on a screen, not computer screen
    LaserTargetCompetitionUI().run()
