from timeit import timeit

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

from datetime import datetime
from time import time, time_ns

from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel
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


Window.clearcolor = (1, 1, 1, 1)


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

        Builder.load_file('TargetScreen.kv')

        super(TargetScreen, self).__init__(**kwargs)
        self.clock_scheduled = False
        self.time_start = time_ns()
        self.time_s = None


    def start(self):
        print("Starting target game")
        self.ids.start.x = self.width + 300
        self.schedule_clock()
        self.time_start = time_ns()
        self.time_s = 0
        self.ids.time_label.center_x = 800 * 0.94
        self.ids.full_timer.center_x = 800 * 1.5


    def move_label_back(self):
        self.ids.time_label.center_x = 800 * 1.5
        self.ids.full_timer.center_x = 800 * 0.94

    def update_all(self, dt=None):  # dt for clock scheduling
        if screen_manager.current == target_screen_name:
            #print(self.time_s)
            if self.time_s <= 0:
                self.move_label_back()
                self.clock_scheduled = False
        return self.clock_scheduled

    def schedule_clock(self):
        if not self.clock_scheduled:
            Clock.schedule_interval(self.update_all, 0)
            self.clock_scheduled = True
        else:
            self.clock_scheduled = False

    def update_label(self):
        self.time_s = -round((time_ns() / 1000000000) - (self.time_start / 1000000000 + 15), 1)
        return self.time_s


    def target_hit(self):
        print("Target Hit!")

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
