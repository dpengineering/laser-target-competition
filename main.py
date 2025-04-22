from keyring.backends.libsecret import available
from kivy import Config
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

from keyboard_handler import on_press, on_release
from leaderboard import Leaderboard
# I know these are grey buts it's required trust me

# TODO
# space bar in name entry (MAYBE NOT NEEDED)
# key for targets and points awarded DONE
# two player?  maybe a laser that you move with the arrow keys and wasd
# sound (PRIORITY)
# combos?
# points pop off target when hit?
# no transition between screens


time = time


screen_manager = ScreenManager()
target_screen_name = 'target'
player_screen_name = 'player'
instructions_screen_name = 'instructions'
leaderboard = Leaderboard()


green_source = 'assets/images/buttons/green.png'
red_source = 'assets/images/buttons/red.png'

class GameState(Enum):
    IDLE = 1
    GET_NEW_LEDS = 2
    WAIT_FOR_TARGET_HIT = 3


class SubmitState(Enum):
    PLAYER_ONE = 1
    PLAYER_TWO = 2

class TargetQuality(Enum):
    PRISMATIC_SHARD = 1
    DIAMOND = 2
    EMERALD = 3
    AMETHYST = 4
    GOLD = 5



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


    def add_score(self, add):
        self.score += add


player_one = Player()
player_two = Player()
players = [player_one, player_two]


class LaserTargetCompetitionUI(App):
    """
        Handles running the app
    """

    def build(self):
        return screen_manager


Window.clearcolor = (0, 0, 0, 1)
fullscreen = (1920, 1080)

Window.size = fullscreen


class EndScreen(Screen):
    def __init__(self, **kw):
        super(EndScreen, self).__init__(**kw)

class InstructionsScreen(Screen):
    """
        Class to handle instructions screen
    """

    def __init__(self, **kw):
        Builder.load_file('InstructionsScreen.kv')
        super(InstructionsScreen, self).__init__(**kw)
        self.player_one_name = "HENRY" #default name for all the cool people who think they can just put no name (nope! it's gonna be my name!).
        self.player_two_name = "HENRY"
        self.keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.state = SubmitState.PLAYER_ONE
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        self.listener.start()



    def on_press(self, key):
        if self.ids.name.text == "l":
            self.ids.name.text = ""
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

    def button_pressed(self, key):
        if self.ids.name.text == "l":
            self.ids.name.text = ""

        if key == "backspace":
            self.ids.name.text = self.ids.name.text[:-1]
        elif key in self.keys:
            self.ids.name.text += key.upper()

    def get_player_one_name(self):
        print(f"p1 name: {self.player_one_name}")
        return self.player_one_name

    def get_player_two_name(self):
        print(f"p2 name: {self.player_two_name}")
        return self.player_two_name

    def submit_text(self):
        if self.state == SubmitState.PLAYER_ONE:
            self.player_one_name = self.ids.name.text
            self.ids.name.text = ''
            self.ids.player_one_name.text = self.player_one_name
            self.ids.instructions.text = "PLAYER TWO, ENTER YOUR NAME OR INITIALS"
            self.state = SubmitState.PLAYER_TWO
        elif self.state == SubmitState.PLAYER_TWO:
            self.player_two_name = self.ids.name.text
            self.ids.player_two_name.text = self.player_two_name
            self.ids.play.x = 0
            self.ids.play_button.x = self.width / 2 - 110
            self.ids.submit.x = 1245
            self.ids.submit_button.x = self.width + 500


    @staticmethod
    def on_release(key):
        print('{0} released'.format(
            key))
        if key == keyboard.Key.esc:
            # Stop listener
            return False

    @staticmethod
    def transition_to_player_screen():
        screen_manager.transition = NoTransition()
        screen_manager.current = player_screen_name


    @staticmethod
    def transition_to_target_screen():
        screen_manager.transition = NoTransition()
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
            #print(str((i + 1)) + ". " + str(score['name']) + " " + str(score['points']))




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



        Builder.load_file('TargetScreen.kv')
        super(TargetScreen, self).__init__(**kwargs)

        self.clock_scheduled = False
        self.time_start = None
        self.time_s = None
        self.time_ms = None
        self.countdown_time_s = None
        self.countdown_timer_start = None
        self.countdown = None
        self.prev_lit_leds = []

        #Player Variables
        self.p1_points = None # todo unused
        self.p2_points = None # todo unused
        self.p1_name = None # todo unused
        self.p2_name = None # todo unused
        player_one.targets = [self.ids.get(f'target_{i}') for i in range(13)]
        player_two.targets = [self.ids.get(f'target_{100 + i}') for i in range(13)]
        self.targets_p1 = [self.ids.get(f'target_{i}') for i in range(13)]  # todo unused target_1 to target_12
        self.targets_p2 = [self.ids.get(f'target_{100 + i}') for i in range(13)]# todo unused

        self.p1_target_appearance_time = 0 # todo unused
        self.p2_target_appearance_time = 0 # todo unused
        self.p1_target_lifetime = 0 # todo unused
        self.p2_target_lifetime = 0 # todo unused
        self.p1_state = "idle" # todo unused
        self.p2_state = "idle" # todo unused
        self.player1_leds = [self.ids.get(f'led_{i}') for i in range(13)]  # led_0 to led_12 # todo unused
        self.player2_leds = [self.ids.get(f'led_{100 + i}') for i in range(13)]  # led_100 to led_112 # todo unused
        player_two.leds = [self.ids.get(f'led_{100 + i}') for i in range(13)]  # led_100 to led_112
        player_one.leds = [self.ids.get(f'led_{i}') for i in range(13)]  # led_0 to led_12
        self.p1_visible_targets = [] # todo unused
        self.p2_visible_targets = [] # todo unused

        # List of states:
        #   - idle -> doing nothing, game hasn't started yet
        #   - get_new_leds -> get new leds to light up
        #   - wait_for_target_hit -> we lit up the leds, now we have to wait for the correct target to be hit
        #   - game_ending(unused) -> game is ending, score is calculating



        #unused(for now)
        easy = 0.1
        medium = 0.3
        hard = 0.5
        impossible = 0.7
        self.difficulty = easy

    def on_enter(self, *args):
        self.p1_name = InstructionsScreen.get_player_one_name(screen_manager.get_screen(instructions_screen_name)) # todo unused
        self.p2_name = InstructionsScreen.get_player_two_name(screen_manager.get_screen(instructions_screen_name)) # todo unused
        self.ids.player_1_name.text = player_one.name
        self.ids.player_2_name.text = player_two.name
        self.ids.player_1_name.text = self.p1_name  # todo unused
        self.ids.player_2_name.text = self.p2_name # todo unused


    def startup_countdown(self):
        self.countdown = True
        self.ids.countdown.x = 0
        self.countdown_timer_start = time_ns()

    def start(self):
        print("Starting target game - setting state to targets")
        self.startup_countdown()
        self.p1_state = "get_new_leds" # todo unused
        self.p2_state = "get_new_leds" # todo unused
        player_two.state = GameState.GET_NEW_LEDS
        player_one.state = GameState.GET_NEW_LEDS
        self.ids.start.center_x = self.width + 300
        self.schedule_clock()
        self.time_start = time_ns()
        self.time_s = 0
        player_two.score = 0
        player_one.score = 0

        self.p1_points = 0 # todo unused
        self.p2_points = 0 # todo unused
        self.ids.player_1_points.text = "00000"
        self.ids.player_2_points.text = "00000"
        # print(f"Player one name: {self.p1_name} Player two name: {self.p2_name}")



    def end(self):
        player_one.state = "idle"
        player_two.state = "idle"
        self.p1_state = "idle" # todo unused
        self.p2_state = "idle" # todo unused
        print(f"p1_state={self.p1_state}")
        print(f"p2_state={self.p2_state}")
        self.ids.start.center_x = self.width / 2
        self.update_time_left_image(15)
        print(f"Your score is: {self.p1_points}, Player one")

        for player in players:
            leaderboard.add_score(player.name, player.score, 1)
            self.transition_to_player_screen()



    def update_all(self, dt=None): # dt for clock scheduling
        #print(f"state={self.state}, target_move_to_pedestal_num={self.target_move_to_pedestal_num}, points={self.points}")
        self.update_time_left_image(self.update_time())
        if screen_manager.current == target_screen_name:
            if self.time_s > 15:
                player_one.target_appearance_time = self.time_ms
                player_two.target_appearance_time = self.time_ms
                self.p1_target_appearance_time = self.time_ms
                self.p2_target_appearance_time = self.time_ms
            if self.time_s > 0:
                self.update_target_quality()
                self.get_new_targets(self.difficulty)
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
        self.time_s = -round((time_ns() / 1000000000) - (self.time_start / 1000000000 + 18.5)) # seconds counting down from 15 after start has been pressed
        self.time_ms = round((time_ns() / 1000000) - (self.time_start / 1000000)) # ms since start has been pressed
        self.countdown_time_s = -round((time_ns() / 1000000000) - (self.countdown_timer_start / 1000000000 + 3.5))
        player_one.target_lifetime = self.time_ms - player_one.target_appearance_time
        player_two.target_lifetime = self.time_ms - player_two.target_appearance_time
        self.p1_target_lifetime = self.time_ms - self.p1_target_appearance_time # todo unused
        self.p2_target_lifetime = self.time_ms - self.p2_target_appearance_time # todo unused
        #print(f"target_move_time={self.target_move_time}, time_ms={self.time_ms}, target_time={self.target_time}")
        return self.time_s


    def update_target_quality(self):
        player_quality = TargetQuality.PRISMATIC_SHARD
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
                player.visible_targets[i].source = f"assets/images/{player_quality}_64.png"
                player.visible_targets[i].quality = str(player_quality)
            except AttributeError:
                print("Attribute Error")

    def get_new_targets(self, difficulty):
        #print("getting new targets, lighting up leds")
        for player in players:
            if player.state == GameState.GET_NEW_LEDS:
                x_offset = 64
                y_offset = 0

                for led in player.leds:
                    led.source = red_source

                for target in player.targets:
                    target.x = self.width + 10

                lit_leds = []

                available_leds = player.leds.copy()

                for led in self.prev_lit_leds:
                    if led in available_leds:
                        available_leds.remove(led)

                first_led = random.choice(available_leds)
                first_led.source = green_source
                lit_leds.append(first_led)
                available_leds.remove(first_led)

                led_chance = random.random()
                while led_chance <= difficulty and available_leds:
                    next_led= random.choice(available_leds)
                    next_led.source = green_source
                    lit_leds.append(next_led)
                    available_leds.remove(next_led)
                    led_chance = random.random()

                self.prev_lit_leds = set(lit_leds)

                lit_led_names = [name for name, widget in self.ids.items() if widget in lit_leds]
                lit_led_indices = [player.leds.index(led) for led in lit_leds]

                for i in lit_led_indices:
                    player.leds[i].source = green_source
                    if i < 4:
                        x_offset = 0
                        y_offset = -64
                    elif i < 9:
                        x_offset = 64
                        y_offset = 0
                    elif i < 13:
                        x_offset = 0
                        y_offset = 64

                    led_x, led_y = player.leds[i].x, player.leds[i].y
                    # Move Player 2's target next to the lit LED
                    player.targets[i].x, player.targets[i].y = led_x + x_offset, led_y + y_offset
                    player.visible_targets.append(player.targets[i])
                    player.target_appearance_time = self.time_ms

                    print(f"Got p2 LEDs to light up, they are: {lit_led_names}")
                    print(f"Got p2 LEDs to light up, they are: {lit_led_indices}")

                    player.state = GameState.WAIT_FOR_TARGET_HIT


    def target_hit(self, target_num):
        #print(f"target {target_num} hit")
        if self.time_s <= 15:
            for player in players:
                if target_num > 99 and player.state == GameState.WAIT_FOR_TARGET_HIT:
                    self.update_points(player.targets[target_num - 100])
                    player.state = GameState.GET_NEW_LEDS
                elif target_num <= 100 and player.state == GameState.WAIT_FOR_TARGET_HIT:
                    self.update_points(player.targets[target_num])
                    player.state = GameState.GET_NEW_LEDS

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
            self.ids.player_1_points.text = str(player_one.score)
        else:
            player_two.add_score(points)
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


Builder.load_file('main.kv')
LabelBase.register(name='PixelFont', fn_regular='assets/fonts/Tiny5-Regular.ttf')
screen_manager.add_widget(PlayerScreen(name=player_screen_name))
screen_manager.add_widget(TargetScreen(name=target_screen_name))
screen_manager.add_widget(InstructionsScreen(name=instructions_screen_name))


if __name__ == "__main__":

    # Window.fullscreen = 'auto' #uncomment this when actually loading on a screen, not computer screen
    LaserTargetCompetitionUI().run()
