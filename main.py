

from pynput import keyboard
from kivy.app import App
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import random
from termcolor import cprint


from datetime import datetime
from time import time, time_ns

from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel
from pidev.kivy.ImageButton import ImageButton
from pidev.kivy import DPEAButton

from keyboard_handler import on_press, on_release
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
        self.enter_pressed = False
        self.is_letter_typed = False
        self.time_s = 0
        self.highlighted_letter = "l"
        self.player_name = "HLS"

        listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        listener.start()


    def on_press(self, key):
        if self.ids.name.text == "l":
            self.ids.name.text = ""
        try:
            if key.char.isalpha():
                self.ids.name.text += key.char.upper()
                self.player_name = self.ids.name.text

        except AttributeError:
            if key == keyboard.Key.backspace:
                self.ids.name.text = self.ids.name.text[:-1]
            if key == keyboard.Key.enter:
                self.player_name = self.ids.name.text
                self.transition_to_target_screen()

        try:
            print('alphanumeric key {0} pressed'.format(
                key.char))
        except AttributeError:
            print('special key {0} pressed'.format(
                key))

    def get_player_name(self):
        return self.player_name

    def on_release(self, key):
        print('{0} released'.format(
            key))
        if key == keyboard.Key.esc:
            # Stop listener
            return False

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
            #print(str((i + 1)) + ". " + str(score['name']) + " " + str(score['points']))




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


        self.prev_lit_leds = []
        Builder.load_file('TargetScreen.kv')
        super(TargetScreen, self).__init__(**kwargs)
        self.clock_scheduled = False
        self.time_start = None
        self.time_s = None
        self.time_ms = None

        #Player Variables
        self.p1_points = None
        self.p2_points = None

        self.targets_p1 = [self.ids.get(f'target_{i}') for i in range(13)]  # target_1 to target_12
        self.targets_p2 = [self.ids.get(f'target_{100 + i}') for i in range(13)]
        print(self.targets_p1)
        self.p1_target_move_time = 0
        self.p2_target_move_time = 0
        self.p1_target_time = 0
        self.p2_target_time = 0
        self.p1_state = "idle"
        self.p2_state = "idle"
        self.player1_leds = [self.ids.get(f'led_{i}') for i in range(13)]  # led_0 to led_12
        self.player2_leds = [self.ids.get(f'led_{100 + i}') for i in range(13)]  # led_100 to led_112

        # List of states:
        #   - idle -> doing nothing, game hasn't started yet
        #   - get_new_leds -> get new leds to light up
        #   - wait_for_target_hit -> we lit up the leds, now we have to wait for the correct target to be hit
        #   - game_ending(unused) -> game is ending, score is calculating
        self.p1_visible_targets = []
        self.p2_visible_targets = []






        self.off_screen = 800 + 64

        #unused(for now)
        easy = 0.1
        medium = 0.3
        hard = 0.5
        impossible = 0.7
        self.difficulty = easy



    def start(self):
        print("Starting target game - setting state to targets")
        self.p1_state = "get_new_leds"
        self.p2_state = "get_new_leds"
        self.ids.start.x = self.width + 300
        self.schedule_clock()
        self.time_start = time_ns()
        self.time_s = 0
        self.p1_points = 0
        self.p2_points = 0



    def end(self):
        self.p1_state = "idle"
        self.p2_state = "idle"
        print(f"p1_state={self.p1_state}")
        print(f"p2_state={self.p2_state}")
        self.ids.start.center_x = 400
        self.update_time_left_image(15)

        if leaderboard.in_top_ten(1, self.p1_points):

            print(f"CONGRATS  PLAYER 1 {InstructionsScreen.get_player_name(screen_manager.get_screen(instructions_screen_name))}! Your score is on the leaderboard!")
            print(f"Your score is: {self.p1_points}")
            leaderboard.add_score(
                InstructionsScreen.get_player_name(
                    screen_manager.get_screen(
                        instructions_screen_name)), self.p1_points, 1)
            self.transition_to_player_screen()

        if leaderboard.in_top_ten(1, self.p2_points):
            print(f"CONGRATS PLAYER 2 {InstructionsScreen.get_player_name(screen_manager.get_screen(instructions_screen_name))}! Your score is on the leaderboard!")
            print(f"Your score is: {self.p2_points}")
            leaderboard.add_score(
                InstructionsScreen.get_player_name(
                    screen_manager.get_screen(
                        instructions_screen_name)), self.p2_points, 1)
            self.transition_to_player_screen()


    def update_all(self, dt=None): # dt for clock scheduling
        #print(f"state={self.state}, target_move_to_pedestal_num={self.target_move_to_pedestal_num}, points={self.points}")
        self.update_time_left_image(self.update_time())
        self.update_target_quality()
        if screen_manager.current == target_screen_name:
            if self.time_s > 0:
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
        self.time_s = -round((time_ns() / 1000000000) - (self.time_start / 1000000000 + 15.5)) # seconds counting down from 15 after start has been pressed
        self.time_ms = round((time_ns() / 1000000) - (self.time_start / 1000000)) # ms since start has been pressed
        self.p1_target_time = self.time_ms - self.p1_target_move_time
        self.p2_target_time = self.time_ms - self.p2_target_move_time
        #print(f"target_move_time={self.target_move_time}, time_ms={self.time_ms}, target_time={self.target_time}")
        return self.time_s



    def update_target_quality(self):
        p2_quality = "prismatic_shard"
        if self.p2_target_time > 900:
            p2_quality = "gold"
        elif self.p2_target_time > 650:
            p2_quality = "amethyst"
        elif self.p2_target_time > 450:
            p2_quality = "emerald"
        elif self.p2_target_time > 325:
            p2_quality = "diamond"

        for i in range(0, len(self.p2_visible_targets)):
            try:
                self.p2_visible_targets[i].source = f"assets/images/{p2_quality}_64.png"
                self.p2_visible_targets[i].quality = p2_quality
            except AttributeError:
                print("Attribute Error")

        p1_quality = "prismatic_shard"
        if self.p1_target_time > 900:
            p1_quality = "gold"
        elif self.p1_target_time > 650:
            p1_quality = "amethyst"
        elif self.p1_target_time > 450:
            p1_quality = "emerald"
        elif self.p1_target_time > 325:
            p1_quality = "diamond"

        for i in range(0, len(self.p1_visible_targets)):
            try:
                self.p1_visible_targets[i].source = f"assets/images/{p1_quality}_64.png"
                self.p1_visible_targets[i].quality = p1_quality
            except AttributeError:
                print("Attribute Error")



    def get_new_targets(self, difficulty):
        #print("getting new targets, lighting up leds")
        if self.p2_state == "get_new_leds":
            x_offset = 64
            y_offset = 0

            for led in self.player2_leds:
                led.source = 'assets/images/buttons/red.png'


            # Reset all targets off-screen
            for target in self.targets_p2:
                target.x = 810  # Move them off-screen

            lit_leds = []

            # Pick at least one LED to light up
            available_leds = self.player2_leds.copy()

            for led in self.prev_lit_leds:
                if led in available_leds:
                    available_leds.remove(led)

            # Pick at least one LED at random
            first_led = random.choice(available_leds)
            first_led.source = 'assets/images/buttons/green.png'
            lit_leds.append(first_led)
            available_leds.remove(first_led)

            # Chance to light up additional LEDs
            led_chance = random.random()
            while led_chance <= difficulty and available_leds:
                next_led = random.choice(available_leds)
                next_led.source = 'assets/images/buttons/green.png'
                lit_leds.append(next_led)
                available_leds.remove(next_led)
                led_chance = random.random()

            self.prev_lit_leds = set(lit_leds)

            lit_led_names = [name for name, widget in self.ids.items() if widget in lit_leds]
            # Find numeric indices of the lit LEDs
            lit_led_indices = [self.player2_leds.index(led) for led in lit_leds]


            for i in lit_led_indices:
                self.player2_leds[i].source = 'assets/images/buttons/green.png'
                if i < 4:
                    x_offset = 0
                    y_offset = -64
                elif i < 9:
                    x_offset = 64
                    y_offset = 0
                elif i < 13:
                    x_offset = 0
                    y_offset = 64

                led_x_p2, led_y_p2 = self.player2_leds[i].x, self.player2_leds[i].y

                # Move Player 2's target next to the lit LED
                self.targets_p2[i].x, self.targets_p2[i].y = led_x_p2 + x_offset, led_y_p2 + y_offset

                #print(f"Player 2: Moving target_{101 + i} to x={self.targets_p2[i].x}, y={self.targets_p2[i].y} next to LED {i}")
                self.p2_visible_targets.append(self.targets_p2[i])

                self.p2_target_move_time = self.time_ms

            # Print the lit LED names
            print(f"Got p2 LEDs to light up, they are: {lit_led_names}")
            print(f"Got p2 LEDs to light up, they are: {lit_led_indices}")
            self.p2_state = "wait_for_target_hit"

        if self.p1_state == "get_new_leds":
            x_offset = 64
            y_offset = 0


            # Reset all LEDs to red first
            for led in self.player1_leds:
                led.source = 'assets/images/buttons/red.png'

                # Reset all targets off-screen
            for target in self.targets_p1:
                target.x = 810  # Move them off-screen

            # Create a list to track which LEDs have been lit
            lit_leds = []

            # Pick at least one LED to light up
            available_leds = self.player1_leds.copy()

            for led in self.prev_lit_leds:
                if led in available_leds:
                    available_leds.remove(led)

            # Pick at least one LED at random
            first_led = random.choice(available_leds)
            first_led.source = 'assets/images/buttons/green.png'
            lit_leds.append(first_led)
            available_leds.remove(first_led)

            # Chance to light up additional LEDs
            led_chance = random.random()
            while led_chance <= difficulty and available_leds:
                next_led = random.choice(available_leds)
                next_led.source = 'assets/images/buttons/green.png'
                lit_leds.append(next_led)
                available_leds.remove(next_led)
                led_chance = random.random()

            self.prev_lit_leds = set(lit_leds)

            lit_led_names = [name for name, widget in self.ids.items() if widget in lit_leds]
            # Find numeric indices of the lit LEDs
            lit_led_indices = [self.player1_leds.index(led) for led in lit_leds]


            for i in lit_led_indices:
                self.player1_leds[i].source = 'assets/images/buttons/green.png'
                if i < 4:
                    x_offset = 0
                    y_offset = -64
                elif i < 9:
                    x_offset = -64
                    y_offset = 0
                elif i < 13:
                    x_offset = 0
                    y_offset = 64
                led_x, led_y = self.player1_leds[i].x, self.player1_leds[i].y

                # Move Player 1's target next to the lit LED
                self.targets_p1[i].x, self.targets_p1[i].y = led_x + x_offset, led_y + y_offset # Offset to the right
                self.p1_visible_targets.append(self.targets_p1[i])

                self.p1_target_move_time = self.time_ms

            # Print the lit LED names
            print(f"Got LEDs to light up, they are: {lit_led_names}")
            print(f"Got LEDs to light up, they are: {lit_led_indices}")

            self.p1_state = "wait_for_target_hit"


    def update_points(self, target):
        if target.player == 1:
            if target.quality == "prismatic_shard":
                self.p1_points += 2000
                cprint(f"Hit a prismatic shard! You have {self.p1_points} points", "red")
            elif target.quality == "diamond":
                self.p1_points += 1000
                cprint(f"Hit a diamond! You have {self.p1_points} points", "cyan")
            elif target.quality == "emerald":

                self.p1_points += 700
                cprint(f"Hit an emerald! You have {self.p1_points} points", "light_green")
            elif target.quality == "amethyst":

                self.p1_points += 500
                cprint(f"Hit an amethyst! You have {self.p1_points} points", "magenta")
            elif target.quality == "gold":

                self.p1_points += 250
                cprint(f"Hit gold! You have {self.p1_points} points", "yellow")

            self.ids.player_1_points.text = str(self.p1_points)
            target.quality = "prismatic_shard" #resets the target to its original quality
        else:
            if target.quality == "prismatic_shard":
                self.p2_points += 2000
                cprint(f"Hit a prismatic shard! You have {self.p2_points} points", "red")
            elif target.quality == "diamond":
                self.p2_points += 1000
                cprint(f"Hit a diamond! You have {self.p2_points} points", "cyan")
            elif target.quality == "emerald":

                self.p2_points += 700
                cprint(f"Hit an emerald! You have {self.p2_points} points", "light_green")
            elif target.quality == "amethyst":

                self.p2_points += 500
                cprint(f"Hit an amethyst! You have {self.p2_points} points", "magenta")
            elif target.quality == "gold":

                self.p2_points += 250
                cprint(f"Hit gold! You have {self.p2_points} points", "yellow")

            self.ids.player_2_points.text = str(self.p2_points)
            target.quality = "prismatic_shard"  # resets the target to its original quality


    def target_hit(self, target_num):
        #print(f"target {target_num} hit")
        if target_num > 99 and self.p2_state == "wait_for_target_hit":
            print("Player two target hit!")
            self.update_points(self.targets_p2[target_num - 100])
            self.p2_state = "get_new_leds"
        elif target_num <= 100 and self.p1_state == "wait_for_target_hit":
            self.update_points(self.targets_p1[target_num])
            self.p1_state = "get_new_leds"


    def update_time_left_image(self, num):
        if num > 9:
            self.ids.time_left.text = str(num)
        else:
            self.ids.time_left.text = "0" + str(num)


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
