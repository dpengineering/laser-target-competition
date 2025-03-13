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
instructions_screen_name = 'instructions'
leaderboard = Leaderboard()


class LaserTargetCompetitionUI(App):
    """
        Handles running the app
    """

    def build(self):
        return screen_manager


Window.clearcolor = (0, 0, 0, 1)

class InstructionsScreen(Screen):
    """
        Class to handle instructions screen
    """
    def __init__(self, **kw):
        Builder.load_file('InstructionsScreen.kv')
        super(InstructionsScreen, self).__init__(**kw)
        self.can_play = True # change to false
        self.clock_scheduled = False
        self.enter_pressed

    def blink_cursor(self):
        print()

    def blink_letter(self):
        print()

    def update_all(self, dt=None): # dt for clock scheduling
        print("running clock!")
        if screen_manager.current == instructions_screen_name:
            if not self.is_letter_typed and not self.enter_pressed:
                self.blink_cursor()
            elif self.is_letter_typed and not self.enter_pressed:
                self.blink_letter()
            elif self.enter_pressed:
                self.clock_scheduled = False
        return self.clock_scheduled

    def schedule_clock(self):
        if not self.clock_scheduled:
            Clock.schedule_interval(self.update_all, 0)
            self.clock_scheduled = True
        else:
            self.clock_scheduled = False

    def on_enter(self, *args):
        self.schedule_clock()

    def play_button_pressed(self):
        if self.can_play:
            self.transition_to_target_screen()
        else:
            print("cannot play, enter name first")

    @staticmethod
    def transition_to_player_screen():
        screen_manager.transition.direction = "left"
        screen_manager.current = player_screen_name

    @staticmethod
    def transition_to_target_screen():
        screen_manager.transition.direction = "left"
        screen_manager.current = target_screen_name


class PlayerScreen(Screen):
    """
        Class to handle player screen
    """
    def __init__(self, **kw):
        super().__init__(**kw)
        self.get_leaderboard()


    def on_enter(self, *args):
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
            elif (i+1) == 8:
                self.ids.name_8.text = str(score['name'])
                self.ids.score_8.text = str(score['points'])
            elif (i + 1) == 9:
                self.ids.name_9.text = str(score['name'])
                self.ids.score_9.text = str(score['points'])
            elif (i+1) == 10:
                self.ids.name_10.text = str(score['name'])
                self.ids.score_10.text = str(score['points'])
            print(str((i + 1)) + ". " + str(score['name']) + " " + str(score['points']))




    @staticmethod
    def transition_to_target_screen():
        screen_manager.transition.direction = "left"
        screen_manager.current = target_screen_name

    @staticmethod
    def transition_to_instructions_screen():
        screen_manager.transition.direction = "right"
        screen_manager.current = instructions_screen_name



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
        self.time_start = None
        self.time_s = None
        self.time_ms = None
        self.targets = False
        self.points = None
        self.target_move_to_pedestal_num = 0
        self.state = "idle"
        self.targets_hit = None
        self.off_screen = 800 + 64
        self.target_quality = {"t1": "prismatic_shard", "t2": "prismatic_shard", "t3": "prismatic_shard", "t4": "prismatic_shard",
                               "t5": "prismatic_shard", "t6": "prismatic_shard", "t7": "prismatic_shard", "t8": "prismatic_shard",
                               "t9": "prismatic_shard", "t10": "prismatic_shard"}
        self.target_move_time = 0
        self.target_time = 0
        self.level = 1


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
        self.target_move_to_pedestal_num = 0
        self.points = 0
        self.targets_are_in = [False, False, False, False, False,
                               False, False, False, False, False]
        self.target_hits = [False, False, False, False, False,
                            False, False, False, False, False]
        self.targets_hit = 0
        self.move_targets_offscreen()

    def move_targets_offscreen(self):
        self.ids.target_1.x = self.off_screen
        self.ids.target_2.x = self.off_screen
        self.ids.target_3.x = self.off_screen
        self.ids.target_4.x = self.off_screen
        self.ids.target_5.x = self.off_screen
        self.ids.target_6.x = self.off_screen
        self.ids.target_7.x = self.off_screen
        self.ids.target_8.x = self.off_screen
        self.ids.target_9.x = self.off_screen
        self.ids.target_10.x = self.off_screen

    def end(self):
        self.state = "idle"
        print(f"state={self.state}")
        self.ids.start.center_x = 400
        self.update_time_left_image(15)

        if leaderboard.in_top_ten(1, self.points):
            print("CONGRATS! Your score is on the leaderboard!")
            self.transition_to_player_screen()
            leaderboard.add_score("HLS", self.points, 1)






    def update_all(self, dt=None): # dt for clock scheduling
        print(f"state={self.state}, target_move_to_pedestal_num={self.target_move_to_pedestal_num}, points={self.points}")
        self.update_time_left_image(self.update_time())
        self.update_target_quality()
        if screen_manager.current == target_screen_name:
            if self.targets and self.targets_hit < 10 and self.time_s > 0:
                self.move_targets()
            elif self.time_s == 0 or self.targets_hit == 10:
                self.clock_scheduled = False
                self.end()
        return self.clock_scheduled

    def schedule_clock(self):
        if not self.clock_scheduled:
            Clock.schedule_interval(self.update_all, 0)
            self.clock_scheduled = True
        else:
            self.clock_scheduled = False



    def update_time(self):
        self.time_s = -round((time_ns() / 1000000000) - (self.time_start / 1000000000 + 15.5)) # seconds counting down from 15 after start has been pressed
        self.time_ms = round((time_ns() / 1000000) - (self.time_start / 1000000)) # ms since start has been pressed
        self.target_time = self.time_ms - self.target_move_time
        print(f"target_move_time={self.target_move_time}, time_ms={self.time_ms}, target_time={self.target_time}")
        return self.time_s



    def update_target_quality(self):
        quality = "prismatic_shard"
        if self.target_time > 3000:
            quality = "gold"
        elif self.target_time > 1200:
            quality = "amethyst"
        elif self.target_time > 600:
            quality = "emerald"
        elif self.target_time > 300:
            quality = "diamond"
        match self.targets_hit:
            case 0:
                self.target_quality['t1'] = quality
                self.ids.target_1.source = f"assets/images/{quality}_64.png"
            case 1:
                self.target_quality['t2'] = quality
                self.ids.target_2.source = f"assets/images/{quality}_64.png"
            case 2:
                self.target_quality['t3'] = quality
                self.ids.target_3.source = f"assets/images/{quality}_64.png"
            case 3:
                self.target_quality['t4'] = quality
                self.ids.target_4.source = f"assets/images/{quality}_64.png"
            case 4:
                self.target_quality['t5'] = quality
                self.ids.target_5.source = f"assets/images/{quality}_64.png"
            case 5:
                self.target_quality['t6'] = quality
                self.ids.target_6.source = f"assets/images/{quality}_64.png"
            case 6:
                self.target_quality['t7'] = quality
                self.ids.target_7.source = f"assets/images/{quality}_64.png"
            case 7:
                self.target_quality['t8'] = quality
                self.ids.target_8.source = f"assets/images/{quality}_64.png"
            case 8:
                self.target_quality['t9'] = quality
                self.ids.target_9.source = f"assets/images/{quality}_64.png"
            case 9:
                self.target_quality['t10'] = quality
                self.ids.target_10.source = f"assets/images/{quality}_64.png"

        print(f"t1={self.target_quality['t1']}, "
              f"t2={self.target_quality['t2']}, "
              f"t3={self.target_quality['t3']}, "
              f"t4={self.target_quality['t3']}, "
              f"t5={self.target_quality['t3']}, "
              f"t6={self.target_quality['t3']}, "
              f"t7={self.target_quality['t3']}, "
              f"t8={self.target_quality['t3']}, "
              f"t9={self.target_quality['t3']}, "
              f"t10={self.target_quality['t4']}")




    def move_specific_target(self, target_num):
        print(f"{target_num}")
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
            self.target_move_time = self.time_ms
        if target_num == 2:
            self.ids.target_2.x = rand_x
            self.ids.target_2.y = rand_y
            self.targets_are_in[1] = True
            self.target_move_time = self.time_ms
        if target_num == 3:
            self.ids.target_3.x = rand_x
            self.ids.target_3.y = rand_y
            self.targets_are_in[2] = True
            self.target_move_time = self.time_ms
        if target_num == 4:
            self.ids.target_4.x = rand_x
            self.ids.target_4.y = rand_y
            self.targets_are_in[3] = True
            self.target_move_time = self.time_ms
        if target_num == 5:
            self.ids.target_5.x = rand_x
            self.ids.target_5.y = rand_y
            self.targets_are_in[4] = True
            self.target_move_time = self.time_ms
        if target_num == 6:
            self.ids.target_6.x = rand_x
            self.ids.target_6.y = rand_y
            self.targets_are_in[5] = True
            self.target_move_time = self.time_ms
        if target_num == 7:
            self.ids.target_7.x = rand_x
            self.ids.target_7.y = rand_y
            self.targets_are_in[6] = True
            self.target_move_time = self.time_ms
        if target_num == 8:
            self.ids.target_8.x = rand_x
            self.ids.target_8.y = rand_y
            self.targets_are_in[7] = True
            self.target_move_time = self.time_ms
        if target_num == 9:
            self.ids.target_9.x = rand_x
            self.ids.target_9.y = rand_y
            self.targets_are_in[8] = True
            self.target_move_time = self.time_ms
        if target_num == 10:
            self.ids.target_10.x = rand_x
            self.ids.target_10.y = rand_y
            self.targets_are_in[9] = True
            self.target_move_time = self.time_ms



    def move_targets(self):
        num = 0
        if self.clock_scheduled:
            if self.level == 1:
                rand = round(random() * 64)
                if rand == 1 and not self.target_hits[0] and self.targets_hit == 0:
                    num = 1
                if rand == 2 and not self.target_hits[1] and self.targets_hit == 1:
                    num = 2
                if rand == 3 and not self.target_hits[2] and self.targets_hit == 2:
                    num = 3
                if rand == 4 and not self.target_hits[3] and self.targets_hit == 3:
                    num = 4
                if rand == 5 and not self.target_hits[4] and self.targets_hit == 4:
                    num = 5
                if rand == 6 and not self.target_hits[5] and self.targets_hit == 5:
                    num = 6
                if rand == 7 and not self.target_hits[6] and self.targets_hit == 6:
                    num = 7
                if rand == 8 and not self.target_hits[7] and self.targets_hit == 7:
                    num = 8
                if rand == 9 and not self.target_hits[8] and self.targets_hit == 8:
                    num = 9
                if rand == 10 and not self.target_hits[9] and self.targets_hit == 9:
                    num = 10


            elif self.level == 2:
                rand = round(random() * 128)
                if rand == 1 and not self.target_hits[0]:
                    num = 1
                if rand == 2 and not self.target_hits[1]:
                    num = 2
                if rand == 3 and not self.target_hits[2]:
                    num = 3
                if rand == 4 and not self.target_hits[3]:
                    num = 4


            self.move_specific_target(num)


            #print(f"rand={rand}rand_x={rand_x}rand_y={rand_y}")


            # difficulty - tutuorial mode
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



    def update_points(self, target):
        match self.target_quality[target]:
            case "prismatic_shard":
                self.points += 1200
            case "diamond":
                self.points += 900
            case "emerald":
                self.points += 600
            case "amethyst":
                self.points += 300
            case "gold":
                self.points += 100

    def target_hit(self, target_num):
        pedestal_x = 0
        pedestal_y = 600 - 64
        if self.state == "targets":
            self.targets_hit += 1
            #print(f"Target {target_num} Hit!")
            self.target_move_to_pedestal_num += 1
            if self.target_move_to_pedestal_num == 1:
                pedestal_x = 0
            elif self.target_move_to_pedestal_num == 2:
                pedestal_x = 64
            elif self.target_move_to_pedestal_num == 3:
                pedestal_x = 128
            elif self.target_move_to_pedestal_num == 4:
                pedestal_x = 128 + 64
            elif self.target_move_to_pedestal_num == 5:
                pedestal_x = 128 + 64 * 2
            elif self.target_move_to_pedestal_num == 6:
                pedestal_x = 128 + 64 * 3
            elif self.target_move_to_pedestal_num == 7:
                pedestal_x = 128 + 64 * 4
            elif self.target_move_to_pedestal_num == 8:
                pedestal_x = 128 + 64 * 5
            elif self.target_move_to_pedestal_num == 9:
                pedestal_x = 128 + 64 * 6
            elif self.target_move_to_pedestal_num == 10:
                pedestal_x = 128 + 64 * 7
            match target_num:
                case 1:
                    self.target_hits[0] = True
                    self.ids.target_1.x = pedestal_x
                    self.ids.target_1.y = pedestal_y
                    self.update_points("t1")
                case 2:
                    self.target_hits[1] = True
                    self.ids.target_2.x = pedestal_x
                    self.ids.target_2.y = pedestal_y
                    self.update_points("t2")
                case 3:
                    self.target_hits[2] = True
                    self.ids.target_3.x = pedestal_x
                    self.ids.target_3.y = pedestal_y
                    self.update_points("t3")
                case 4:
                    self.target_hits[3] = True
                    self.ids.target_4.x = pedestal_x
                    self.ids.target_4.y = pedestal_y
                    self.update_points("t4")
                case 5:
                    self.target_hits[4] = True
                    self.ids.target_5.x = pedestal_x
                    self.ids.target_5.y = pedestal_y
                    self.update_points("t5")
                case 6:
                    self.target_hits[5] = True
                    self.ids.target_6.x = pedestal_x
                    self.ids.target_6.y = pedestal_y
                    self.update_points("t6")
                case 7:
                    self.target_hits[6] = True
                    self.ids.target_7.x = pedestal_x
                    self.ids.target_7.y = pedestal_y
                    self.update_points("t7")
                case 8:
                    self.target_hits[7] = True
                    self.ids.target_8.x = pedestal_x
                    self.ids.target_8.y = pedestal_y
                    self.update_points("t8")
                case 9:
                    self.target_hits[8] = True
                    self.ids.target_9.x = pedestal_x
                    self.ids.target_9.y = pedestal_y
                    self.update_points("t9")
                case 10:
                    self.target_hits[9] = True
                    self.ids.target_10.x = pedestal_x
                    self.ids.target_10.y = pedestal_y
                    self.update_points("t10")

    def update_time_left_image(self, num):
        # print("updating time left")
        # print(f"time_left={num}")
        # please someone make this whole timer system a SelfUpdatingLabel!!!!!!
        # I don't have the time for that so this will do, but still please

        if num == 0:
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

    @staticmethod
    def transition_to_player_screen():
        screen_manager.transition.direction = "right"
        screen_manager.current = player_screen_name




Builder.load_file('main.kv')
LabelBase.register(name='PixelFont', fn_regular='assets/fonts/Tiny5-Regular.ttf')
screen_manager.add_widget(PlayerScreen(name=player_screen_name))
screen_manager.add_widget(TargetScreen(name=target_screen_name))
screen_manager.add_widget(InstructionsScreen(name=instructions_screen_name))


if __name__ == "__main__":

    # Window.fullscreen = 'auto' #uncomment this when actually loading on a screen, not computer screen
    LaserTargetCompetitionUI().run()
