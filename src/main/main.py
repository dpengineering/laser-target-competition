from statistics import median_low
from typing import overload

from gi.overrides import override
from keyring.backends.libsecret import available
from kivy import Config
from kivy.core.audio import SoundLoader
from orca.sound import Player

Config.set('kivy', 'keyboard_mode', 'systemanddock')
from pynput import keyboard
from kivy.app import App
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
import random
from enum import Enum
from termcolor import cprint



from datetime import datetime
from time import time, time_ns

from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel
from pidev.kivy.ImageButton import ImageButton
from pidev.kivy import DPEAButton

from leaderboard import Leaderboard
# I know these are grey buts it's required trust me

# TODO
# space bar in name entry (MAYBE NOT NEEDED)
# key for targets and points awarded (DONE!)
# click all targets instead of just one (DONE!)
# no transition between screens (DONE)
# sound (DONE!)
# two player?  maybe a laser that you move with the arrow keys and wasd (LOW PRIORITY)
# numbers to username creation (LOW PRIORITY)
# combos?
# points pop off target when hit?
# END SCREEN (kinda priority)
#  -  Show points and position on leaderboard
#  -  leaderboard continues after 10th place
# set levels - (PRIORITY)
#  -  each level is a list of a list of each set of leds to light up
#  -  first, leds one and three will light up, then led two, then seven, eight, and nine, then etc...
#  -  for levels, time is tracked as well as points(or maybe just time, or just points??)
#  -  medals for set levels?
#  -  medals in general - copper - silver - electrum - gold - platinum - diamond(author medal)




time = time

screen_manager = ScreenManager()
target_screen_name = 'target'
player_screen_name = 'player'
end_screen_name = 'end'
instructions_screen_name = 'instructions'
leaderboard = Leaderboard()


GREEN_SOURCE = 'assets/images/buttons/leds/green.png'
RED_SOURCE = 'assets/images/buttons/leds/red.png'

SOUND_FILES = {
    "target_hit": 'assets/sounds/target_hit.wav',
    "select": 'assets/sounds/select.wav'
}
class Gamemode(Enum):
    RANDOM = 1
    LEVELS = 2

class GameState(Enum):
    IDLE = 1
    GET_NEW_LEDS = 2
    WAIT_FOR_TARGET_HIT = 3


class SubmitState(Enum):
    PLAYER_ONE = 1
    PLAYER_TWO = 2

class TargetQuality(Enum):
    PRISMATIC_SHARD = "prismatic_shard"
    DIAMOND = "diamond"
    EMERALD = "emerald"
    AMETHYST = "amethyst"
    GOLD = "gold"


def play_sound(s):
    sound = SoundLoader.load(SOUND_FILES[s])
    sound.stop()
    sound.play()

player_count = 0

class Player:
    def __init__(self):
        self.name = "Henry"
        self.score = 0
        self.targets = None
        self.target_appearance_time = 0
        self.target_lifetime = 0
        self.state = "idle"
        self.leds = []
        self.visible_targets = []
        self.player_number = player_count
        self.lit_leds = []
        self.prev_lit_leds = []


    def add_score(self, add):
        self.score += add

    def get_leaderboard_position(self):
        return leaderboard.get_placement(1, self.score)

player_count += 1
player_one = Player()
player_count += 1
player_two = Player()
players = [player_one, player_two]
targets = []
leds = []


class LaserTargetCompetitionUI(App):
    """
        Handles running the app
    """

    def build(self):
        return screen_manager


Window.clearcolor = (0, 0, 0, 1)
fullscreen = (1920, 1080)

Window.size = fullscreen


class Medal(Enum):
    CHAMPION = 1
    AUTHOR = 2
    GOLD = 3
    SILVER = 4
    BRONZE = 5
    NONE = 6


def get_medals(player):
    if player.score > 50000:
        medal = Medal.CHAMPION
    elif player.score > 37000:
        medal = Medal.AUTHOR
    elif player.score > 29000:
        medal = Medal.GOLD
    elif player.score > 20000:
        medal = Medal.SILVER
    elif player.score > 10000:
        medal = Medal.BRONZE
    else:
        medal = Medal.NONE
    return medal


class EndScreen(Screen):
    def __init__(self, **kw):

        Builder.load_file('../kv/EndScreen.kv')
        super(EndScreen, self).__init__(**kw)
        self.final_score_one = 40000
        self.final_score_two = 10000
        self.current_score_one = 0
        self.current_score_two = 0
        self.scores = {self.final_score_one: self.current_score_one, self.final_score_two: self.current_score_two}
        self.update_interval = 0.01
        self.scheduled_event = None
        self.slower = 0
        self.slower2 = 0
        self.score_one_done = False
        self.score_two_done = False
        self.lpos_1 = 12
        self.lpos_2 = 3

    def on_enter(self):
        # self.lpos_1 = player_one.get_leaderboard_position()
        # self.lpos_2 = player_two.get_leaderboard_position()
        # self.final_score_one = player_one.score
        # self.final_score_two = player_two.score
        self.scheduled_event = Clock.schedule_interval(self.update_score, self.update_interval)


    def update_score(self, dt):
        if self.score_two_done and self.score_one_done:
            self.set_leaderboard_position()
            self.set_medals()
            self.scheduled_event.cancel()


        remaining_two = self.final_score_two - self.current_score_two
        remaining_one = self.final_score_one - self.current_score_one
        if remaining_one > 10000:
            self.current_score_one += 307
        elif remaining_one > 5000:
            self.current_score_one += 107
        elif remaining_one > 2500:
            self.current_score_one += 51
        elif remaining_one > 125:
            self.current_score_one += 28
        elif remaining_one > 65:
            self.current_score_one += 13
        else:
            self.slower += 1
            if self.slower == 2:
                self.current_score_one += 1
                self.slower = 0

        if self.current_score_one >= self.final_score_one:
            self.current_score_one = self.final_score_one
            self.ids.player_1_points.text = str(self.current_score_one)
            self.score_one_done = True
            return

        self.ids.player_1_points.text = str(self.current_score_one)

        if remaining_two > 10000:
            self.current_score_two += 307
        elif remaining_two > 5000:
            self.current_score_two += 107
        elif remaining_two > 2500:
            self.current_score_two += 51
        elif remaining_two > 125:
            self.current_score_two += 28
        elif remaining_two > 65:
            self.current_score_two += 13
        else:
            self.slower2 += 1
            if self.slower2 == 2:
                self.current_score_two += 1
                self.slower2 = 0

        if self.current_score_two >= self.final_score_two:
            self.current_score_two = self.final_score_two
            self.ids.player_2_points.text = str(self.current_score_two)
            self.score_two_done = True
            return

        self.ids.player_2_points.text = str(self.current_score_two)


    def set_leaderboard_position(self):
        self.ids.player_1_lpos.text = f"Top {str(self.lpos_1)} World"
        self.ids.player_2_lpos.text = f"TOP {str(self.lpos_2)} WORLD"


    def set_medals(self):
        medal_one = get_medals(player_one)
        medal_two = get_medals(player_two)


    @staticmethod
    def transition_to_player_screen():
        screen_manager.transition = NoTransition()
        screen_manager.current = player_screen_name

class InstructionsScreen(Screen):
    """
        Class to handle instructions screen
    """

    def __init__(self, **kw):
        Builder.load_file('../kv/InstructionsScreen.kv')
        super(InstructionsScreen, self).__init__(**kw)
        self.keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.state = SubmitState.PLAYER_ONE
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)

    def start_thread(self):
        if not self.listener.is_alive():
            self.listener.start()

    def stop_thread(self):
        if self.listener.is_alive():
            self.listener.stop()

    def on_press(self, key):
        try:
            if key.char.isalpha():
                self.ids.name.text += key.char.upper()

        except AttributeError:
            if key == keyboard.Key.backspace:
                self.ids.name.text = self.ids.name.text[:-1]

        try:
            print('alphanumeric key {0} pressed'.format(
                key.char))
        except AttributeError:
            print('special key {0} pressed'.format(
                key))

    @staticmethod
    def on_release(key):
        print('{0} released'.format(
            key))

    def on_enter(self, *args):
        self.start_thread()

    def on_leave(self, *args):
        self.stop_thread()

    def button_pressed(self, key):
        if self.ids.name.text == "l":
            self.ids.name.text = ""
        if key == "backspace":
            self.ids.name.text = self.ids.name.text[:-1]
        elif key in self.keys:
            self.ids.name.text += key.upper()

    def submit_text(self):
        if self.state == SubmitState.PLAYER_ONE:
            player_one.name = self.ids.name.text
            self.ids.name.text = ''
            self.ids.player_one_name.text = player_one.name
            self.ids.instructions.text = "PLAYER TWO, ENTER YOUR NAME OR INITIALS"
            self.state = SubmitState.PLAYER_TWO
        elif self.state == SubmitState.PLAYER_TWO:
            player_two.name = self.ids.name.text
            self.ids.player_two_name.text = player_two.name
            self.ids.play.x = 0
            self.ids.play_button.x = self.width / 2 - 110
            self.ids.submit.x = 1245
            self.ids.submit_button.x = self.width + 500


    @staticmethod
    def transition_to_player_screen():
        screen_manager.transition = NoTransition()
        screen_manager.current = player_screen_name


    @staticmethod
    def transition_to_target_screen():
        screen_manager.transition = NoTransition()
        screen_manager.current = target_screen_name

    @staticmethod
    def transition_to_end_screen():
        screen_manager.transition = NoTransition()
        screen_manager.current = end_screen_name


class PlayerScreen(Screen):
    """
        Class to handle player screen
    """
    def __init__(self, **kw):
        super().__init__(**kw)

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

    @staticmethod
    def transition_to_target_screen():
        screen_manager.transition = NoTransition()
        screen_manager.current = target_screen_name

    @staticmethod
    def transition_to_instructions_screen():
        screen_manager.transition = NoTransition()
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

        Builder.load_file('../kv/TargetScreen.kv')
        super(TargetScreen, self).__init__(**kwargs)
        self.clock_scheduled = False
        self.time_start = None
        self.time_s = None
        self.time_ms = None
        self.countdown_time_s = None
        self.countdown_timer_start = None
        self.countdown = None

        self.gamemode = Gamemode.RANDOM

        #Player Variables set
        player_one.targets = [self.ids.get(f'target_{i}') for i in range(13)]
        player_two.targets = [self.ids.get(f'target_{100 + i}') for i in range(13)]
        player_two.leds = [self.ids.get(f'led_{100 + i}') for i in range(13)]  # led_100 to led_112
        player_one.leds = [self.ids.get(f'led_{i}') for i in range(13)]  # led_0 to led_12
        targets.append(player_one.targets)
        targets.append(player_two.targets)
        leds.append(player_one.leds)
        leds.append(player_one.leds)

        # Levels
        self.level_1 = [[self.ids.get('target_1'), self.ids.get('target_3')],
                   [self.ids.get('target_2')],
                   [self.ids.get('target_7'), self.ids.get('target_8'), self.ids.get('target_9')],
                   [self.ids.get('target_12'), self.ids.get('target_3'), self.ids.get('target_5')]]


        #unused(for now)
        easy = 0.1
        medium = 0.3
        hard = 0.5
        impossible = 0.7
        self.difficulty = easy

    def on_enter(self, *args):
        self.ids.player_1_name.text = player_one.name
        self.ids.player_2_name.text = player_two.name

    def startup_countdown(self):
        self.countdown = True
        self.ids.countdown.x = 0
        self.countdown_timer_start = time_ns()

    def start(self):
        print("Starting target game - setting state to targets")
        self.startup_countdown()
        player_two.state = GameState.GET_NEW_LEDS
        player_one.state = GameState.GET_NEW_LEDS
        self.ids.start.center_x = self.width + 300
        self.schedule_clock()
        self.time_start = time_ns()
        self.time_s = 0
        player_two.score = 0
        player_one.score = 0
        self.ids.player_1_points.text = "00000"
        self.ids.player_2_points.text = "00000"

    def end(self):
        player_one.state = "idle"
        player_two.state = "idle"
        self.ids.start.center_x = self.width / 2
        self.update_time_left_image(15)
        self.ids.go.x = self.width = 1
        for player in players:
            leaderboard.add_score(player.name, player.score, 1)
            self.transition_to_end_screen()

    def update_all(self, dt=None): # dt for clock scheduling
        #print(f"state={self.state}, target_move_to_pedestal_num={self.target_move_to_pedestal_num}, points={self.points}")
        self.update_time_left_image(self.update_time())
        if screen_manager.current == target_screen_name:
            if self.time_s > 15:
                player_one.target_appearance_time = self.time_ms
                player_two.target_appearance_time = self.time_ms
            if self.time_s > 0:
                self.update_target_quality()
                self.activate_random_targets(self.difficulty)
            elif self.time_s == 0:
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
        countdown_time = 3.5
        play_time = 15
        self.time_s = -round((time_ns() / 1000000000) - (self.time_start / 1000000000 + countdown_time + play_time)) # seconds counting down from 15 after start has been pressed
        self.time_ms = round((time_ns() / 1000000) - (self.time_start / 1000000)) # ms since start has been pressed
        self.countdown_time_s = -round((time_ns() / 1000000000) - (self.countdown_timer_start / 1000000000 + countdown_time))
        player_one.target_lifetime = self.time_ms - player_one.target_appearance_time
        player_two.target_lifetime = self.time_ms - player_two.target_appearance_time
        return self.time_s


    def update_target_quality(self):
        for player in players:
            player_quality = TargetQuality.PRISMATIC_SHARD
            if player.target_lifetime > 900:
                player_quality = TargetQuality.GOLD
            elif player.target_lifetime > 650:
                player_quality = TargetQuality.AMETHYST
            elif player.target_lifetime > 450:
                player_quality = TargetQuality.EMERALD
            elif player.target_lifetime > 325:
                player_quality = TargetQuality.DIAMOND

            for i in range(0, len(player.visible_targets)):
                try:
                    player.visible_targets[i].source = f"assets/images/buttons/targets/{player_quality.value}_64.png"
                    player.visible_targets[i].quality = player_quality.value
                except AttributeError:
                    print("Attribute Error")

    def remove_target(self, target, led):
        for p in targets:
            for t in p:
                if t == target:
                    t.x = self.width + 10
        for p in leds:
            for l in p:
                if l == led:
                    led.source = RED_SOURCE




    def activate_specific_targets(self, level_round):
        for p in players:
            if p.state == GameState.GET_NEW_LEDS:
                x_offset = 64
                y_offset = 0

                for led in p.leds:
                    led.source = RED_SOURCE

                for target in p.targets:
                    target.x = self.width + 10

                p.lit_leds = []


                for led in self.level_1[level_round]:
                    led.source = GREEN_SOURCE
                    p.lit_leds.append(led)

                lit_led_names = [name for name, widget in self.ids.items() if widget in p.lit_leds]
                lit_led_indices = [p.leds.index(led) for led in p.lit_leds]

                for i in lit_led_indices:
                    p.leds[i].source = GREEN_SOURCE
                    if i < 4:
                        x_offset = 0
                        y_offset = -64
                    elif i < 9:
                        if p.player_number == 1:
                            x_offset = -64
                        else:
                            x_offset = 64
                        y_offset = 0
                    elif i < 13:
                        x_offset = 0
                        y_offset = 64

                    led_x, led_y = p.leds[i].x, p.leds[i].y
                    # Move Player 2's target next to the lit LED
                    p.targets[i].x, p.targets[i].y = led_x + x_offset, led_y + y_offset
                    p.visible_targets.append(p.targets[i])
                    p.target_appearance_time = self.time_ms
                    p.state = GameState.WAIT_FOR_TARGET_HIT
                    print(f"Got LEDs to light up, they are: {lit_led_names}")
                    print(f"Got LEDs to light up, they are: {lit_led_indices}")



    def activate_random_targets(self, difficulty):
        for p in players:
            if p.state == GameState.GET_NEW_LEDS:
                x_offset = 64
                y_offset = 0

                for led in p.leds:
                    led.source = RED_SOURCE

                for target in p.targets:
                    target.x = self.width + 10

                p.lit_leds = []

                available_leds = p.leds.copy()

                for led in p.prev_lit_leds:
                        available_leds.remove(led)

                first_led = random.choice(available_leds)
                first_led.source = GREEN_SOURCE
                p.lit_leds.append(first_led)
                available_leds.remove(first_led)

                led_chance = random.random()
                while led_chance <= difficulty and available_leds:
                    next_led= random.choice(available_leds)
                    next_led.source = GREEN_SOURCE
                    p.lit_leds.append(next_led)
                    available_leds.remove(next_led)
                    led_chance = random.random()

                p.prev_lit_leds = set(p.lit_leds)

                lit_led_names = [name for name, widget in self.ids.items() if widget in p.lit_leds]
                lit_led_indices = [p.leds.index(led) for led in p.lit_leds]

                for i in lit_led_indices:
                    p.leds[i].source = GREEN_SOURCE
                    if i < 4:
                        x_offset = 0
                        y_offset = -64
                    elif i < 9:
                        if p.player_number == 1:
                            x_offset = -64
                        else:
                            x_offset = 64
                        y_offset = 0
                    elif i < 13:
                        x_offset = 0
                        y_offset = 64

                    led_x, led_y = p.leds[i].x, p.leds[i].y
                    # Move Player 2's target next to the lit LED
                    p.targets[i].x, p.targets[i].y = led_x + x_offset, led_y + y_offset
                    p.visible_targets.append(p.targets[i])
                    p.target_appearance_time = self.time_ms
                    p.state = GameState.WAIT_FOR_TARGET_HIT
                    print(f"Got LEDs to light up, they are: {lit_led_names}")
                    print(f"Got LEDs to light up, they are: {lit_led_indices}")


    def target_hit(self, target, led):
        if self.time_s <= 15:
            self.remove_target(target, led)
            play_sound("target_hit")
            if target.player == 2 and player_two.state == GameState.WAIT_FOR_TARGET_HIT:
                player_two.lit_leds.remove(led)
                if not player_two.lit_leds:
                    player_two.state = GameState.GET_NEW_LEDS
                self.update_points(target)
            elif target.player == 1 and player_one.state == GameState.WAIT_FOR_TARGET_HIT:
                player_one.lit_leds.remove(led)
                if not player_one.lit_leds:
                    player_one.state = GameState.GET_NEW_LEDS
                self.update_points(target)


    def update_points(self, target):
        points = 0
        if target.quality == "prismatic_shard":
            points += 2000
            cprint(f"Hit a prismatic shard! You have {points} points", "red")
        elif target.quality == "diamond":
            points += 1000
            cprint(f"Hit a diamond! You have {points} points", "cyan")
        elif target.quality == "emerald":
            points += 700
            cprint(f"Hit an emerald! You have {points} points", "light_green")
        elif target.quality == "amethyst":
            points += 500
            cprint(f"Hit an amethyst! You have {points} points", "magenta")
        elif target.quality == "gold":
            points += 250
            cprint(f"Hit gold! You have {points} points", "yellow")
        if target.player == 1:
            player_one.add_score(points)
            print(f"Player one Score: {player_one.score}")
            self.ids.player_1_points.text = str(player_one.score)
        else:
            player_two.add_score(points)
            print(f"Player two Score: {player_two.score}")
            self.ids.player_2_points.text = str(player_two.score)
        target.quality = "prismatic_shard" #resets the target to its original quality

    def update_countdown_image(self, num):
        if num > 0:
            self.ids.countdown.text = str(num)
        else:
            self.countdown = False
            self.ids.countdown.x = self.width + 100

    def update_time_left_image(self, num):
        if num > 15:
            self.ids.countdown.text = str(num - 15)
        elif num == 15:
            self.ids.countdown.x = self.width + 100
            self.ids.go.x = 0
        elif num == 14:
            self.ids.go.x = self.width + 100
            self.ids.time_left.text = str(num)
        elif num > 9:
            self.ids.time_left.text = str(num)
        else:
            self.ids.time_left.text = "0" + str(num)

    @staticmethod
    def transition_to_player_screen():
        screen_manager.transition = NoTransition()
        screen_manager.current = player_screen_name

    @staticmethod
    def transition_to_end_screen():
        screen_manager.transition = NoTransition()
        screen_manager.current = end_screen_name

Builder.load_file('../kv/main.kv')
LabelBase.register(name='PixelFont', fn_regular='assets/fonts/Tiny5-Regular.ttf')
screen_manager.add_widget(PlayerScreen(name=player_screen_name))
screen_manager.add_widget(TargetScreen(name=target_screen_name))
screen_manager.add_widget(InstructionsScreen(name=instructions_screen_name))
screen_manager.add_widget(EndScreen(name=end_screen_name))

if __name__ == "__main__":

    # Window.fullscreen = 'auto' #uncomment this when actually loading on a screen, not computer screen
    LaserTargetCompetitionUI().run()