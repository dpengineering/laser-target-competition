from random import random
from timeit import timeit

from kivy.app import App
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window




from datetime import datetime
from time import time, time_ns

from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel
from pidev.kivy.ImageButton import ImageButton
from pidev.kivy import DPEAButton

from leaderboard import Leaderboard

# I know these are grey buts it's required trust me

time = time



screen_manager = ScreenManager()
target_screen_name = 'target'
player_screen_name = 'player'
leaderboard = Leaderboard()


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
    def __init__(self, **kw):
        super().__init__(**kw)
        self.get_leaderboard()


    def get_leaderboard(self):
        for i, score in enumerate(leaderboard.scores[1]): # 1 is the level
            if (i + 1) == 1:
                self.ids.name_1.text = str(score['name'])
                self.ids.score_1.text = str(score['points'])
            elif (i+1) == 2:
                self.ids.name_2.text = str(score['name'])
                self.ids.score_2.text = str(score['points'])
            elif (i+1) == 3:
                self.ids.name_3.text = str(score['name'])
                self.ids.score_3.text = str(score['points'])
            elif (i+1) == 4:
                self.ids.name_4.text = str(score['name'])
                self.ids.score_4.text = str(score['points'])
            elif (i+1) == 5:
                self.ids.name_5.text = str(score['name'])
                self.ids.score_5.text = str(score['points'])
            elif (i+1) == 6:
                self.ids.name_6.text = str(score['name'])
                self.ids.score_6.text = str(score['points'])
            elif (i+1) == 7:
                self.ids.name_7.text = str(score['name'])
                self.ids.score_7.text = str(score['points'])
            print(str((i + 1)) + ". " + str(score['name']) + " " + str(score['points']))


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
        self.off_screen = 800 + 64 - 8
        self.targets_hit = None

        #unused(for now)
        self.difficulty = "easy"


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
        self.move_targets_offscreen()

    def move_targets_offscreen(self):
        self.ids.target_1.x = self.off_screen
        self.ids.target_2.x = self.off_screen
        self.ids.target_3.x = self.off_screen
        self.ids.target_4.x = self.off_screen

    def end(self):
        self.state = "idle"
        print(f"state={self.state}")
        self.ids.start.center_x = 400
        self.update_time_left_image(15)

        if leaderboard.in_top_ten(1, self.points):
            leaderboard.add_score("HLS", self.points, 1)
            leaderboard.draw_leaderboard()




    def update_all(self, dt=None): # dt for clock scheduling
        print(f"state={self.state}, points={self.points}")
        self.update_time_left_image(self.update_time_left())
        if screen_manager.current == target_screen_name:
            if self.targets and self.targets_hit < 4 and self.time_s > 0:
                self.move_targets()
            elif self.time_s == 0 or self.targets_hit == 4:
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
        #print("updating time left")
        #print(f"time_left={num}")
        #please someone make this whole timer system a SelfUpdatingLabel!!!!!!
        #I don't have the time for that so this will do, but still please
        self.off_screen = 800 + 64
        if num == 0:
            self.end()
            self.ids.time_left.text = "00"
        elif num == 1:
            self.ids.time_left.text = "01"
        elif num == 2:
            self.ids.time_left.text = "02"
        elif num == 3:
            self.ids.time_left.text = "03"
        elif num == 4:
            self.ids.time_left.text = "04"
        elif num == 5:
            self.ids.time_left.text = "05"
        elif num == 6:
            self.ids.time_left.text = "06"
        elif num == 7:
            self.ids.time_left.text = "07"
        elif num == 8:
            self.ids.time_left.text = "08"
        elif num == 9:
            self.ids.time_left.text = "09"
        elif num == 10:
            self.ids.time_left.text = "10"
        elif num == 11:
            self.ids.time_left.text = "11"
        elif num == 12:
            self.ids.time_left.text = "12"
        elif num == 13:
            self.ids.time_left.text = "13"
        elif num == 14:
            self.ids.time_left.text = "14"
        else:
            self.ids.time_left.text = "15"

    def move_specific_target(self, target_num):
        if self.targets_are_in[target_num - 1]:
            return
        rand_x = round(random() * 800) - 64 # 800 - 64 = screen width - target size
                                           # targets can't spawn offscreen
        rand_y = round(random() * 600) - 64 # 600 = 64 = screen height - target size

        if rand_y < 0:
            rand_y = 0
        if rand_x < 0:
            rand_x = 0

        if target_num == 1:
            self.ids.target_1.x = rand_x
            self.ids.target_1.y = rand_y
            self.targets_are_in[0] = True
        if target_num == 2:
            self.ids.target_2.x = rand_x
            self.ids.target_2.y = rand_y
            self.targets_are_in[1] = True
        if target_num == 3:
            self.ids.target_3.x = rand_x
            self.ids.target_3.y = rand_y
            self.targets_are_in[2] = True
        if target_num == 4:
            self.ids.target_4.x = rand_x
            self.ids.target_4.y = rand_y
            self.targets_are_in[3] = True


    def move_targets(self):
        if self.clock_scheduled:
            #print("moving targets")
            rand = round(random() * 128)

            #print(f"rand={rand}rand_x={rand_x}rand_y={rand_y}")


            # difficulty
            # easy - one target at a time
            # medium - multiple targets at once, but the same total number of targets as easy
            # hard - multiple targets at once, more targets than easy or medium, and targets spawn faster


            # gameplay
            # move a random target on the screen
            # player clicks that target, gets points for the quality of target clicked
            # that target starts as a prismatic shard, then loses quality
            # after 300ms it becomes a diamond (0.3 seconds after appearing)
            # 300ms after that it becomes an emerald (600ms/0.6s aa)
            # 600ms after that it becomes an amethyst (1200ms/1.2s aa)
            # 1800ms after that it becomes a gold bar (3000ms/3s aa)


            # Points:
            # Prismatic Shard - 1200 points
            # Diamond - 900p
            # Emerald - 600p
            # Amethyst - 300p
            # Gold Bar - 100p

            if rand == 1 and not self.target_hits[0]:
                self.move_specific_target(1)
            if rand == 2 and not self.target_hits[1]:
                self.move_specific_target(2)
            if rand == 3 and not self.target_hits[2]:
                self.move_specific_target(3)
            if rand == 4 and not self.target_hits[3]:
                self.move_specific_target(4)



    def target_hit(self, target_num):
        pedestal_x = 0
        pedestal_y = 600 - 64
        if self.state == "targets":
            self.targets_hit += 1
            #print(f"Target {target_num} Hit!")
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
LabelBase.register(name='PixelFont', fn_regular='assets/fonts/Tiny5-Regular.ttf')
screen_manager.add_widget(PlayerScreen(name=player_screen_name))
screen_manager.add_widget(TargetScreen(name=target_screen_name))


if __name__ == "__main__":

    # Window.fullscreen = 'auto' #uncomment this when actually loading on a screen, not computer screen
    LaserTargetCompetitionUI().run()
