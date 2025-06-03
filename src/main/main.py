"""
Hi there! This is main.py, where everything happens(mostly). It's unfinished, but I wanted to outline what I had planned.
I created three categories of importance.
- VITAL, things that need to be implemented for the game to work. Mostly just hardware integration things, like stepper motor movement etc.
- NON-VITAL, things that don't technically need to be implemented, but are pretty fun/cool features.
- AESTHETIC, things that don't need to be implemented, but make the project look good. Add these last(or don't if you are good at pixel art).

--Stepper Motor Movement (VITAL)
    -Connection between two physical buttons and a stepper motor that houses the laser.
    -Most important thing is to stop the stepper if it goes too far. Remember it houses a very powerful laser than can cause serious eye
    damage.
    -Each button should move the stepper left or right.
--Hardware Integration (MOST OF MOST VITAL)
    -Integrate with the completed physical project
--Level Selector Screen (VITAL)
    -New screen that appears after each player enters their name.
    -Is vital because of how the physical game works.
    -In the physical game, the player places blocks that bend or split the laser beam.
    -If we were to use truly random target generation, there is a chance that an impossible set of targets could be generated.
    -Levels could increase in difficulty with the leading number. 1-1, and 1-2 are easy, 2-1 is medium, 3-1 is difficult.
--EndScreen Functionality (VITAL)
    -Bug causes player two's score not to be displayed on the EndScreen.
    -pls fix
    -Leaderboard position display doesn't work either
    -Neither does player name display
--Background Pixel Art (AESTHETIC)
    -I planned on adding some background art to this project.
    -Vibe is crystal mining oriented right now, with lasers and refraction/reflection.
    -I was prolly gonna do a mining vibe, but you could do whatever you want
--Change Image Scaling (NON-VITAL)
    -Make images scale as nearest neighbor interpolation instead of bilinear interpolation
    -So that you don't have to manually scale images(most noticeable with medals right now).
    -Not technically vital as you could scale every image by hand to the correct res, but that sucks. Thumbs down.
    -I already did this for the targets and leds, it was annoying
--Improve EndScreen Aesthetics and Functionality (NON-VITAL)
    -EndScreen looks like crap rn
    -Maybe display medals and score bigger?
    -Add some stats(like avg time between target's, fastest target hit, etc...)
--Fix Double-Click Touch or Implement Workaround (VITAL)
    -When clicking the physical screen it always double-clicks, which isn't great
    -fix or move buttons
--Add Additional Sounds (NON-VITAL)
    -Perhaps an increasing in pitch ding sound for every medal acquired, like TMNF.
    -Sounds for each button press when navigating the screens
    -Background music for menu, game start, and a fanfare for EndScreen.
--Target Click Effects (AESTHETIC)
    -When clicking targets have particles fly off denoting what score you got
    -Rainbow = 2000, blue = 1000 etc...
    -It's currently hard to tell what score you got each time you click.
--Game Replayability (VITAL)
    -Currently lots of things break when after the game has completed, you play another
    -pls fix
--Add an Easter Egg (AESTHETIC)
    -Make sure to make it findable and fun!
    -Did you find mine yet? HINT: l##de#b#ard



"""
import os
os.environ["DISPLAY"] = ":0.0"
from dpeaDPi import DPiStepper
from dpeaDPi.DPiStepper import DPiStepper
from dpeaDPi.DPiComputer import DPiComputer
from dpeaDPi.DPiPowerDrive import DPiPowerDrive

from kivy.animation import Animation
from kivy.core.audio import SoundLoader

from kivy.app import App
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
import random
from enum import Enum
from termcolor import cprint

from time import time, time_ns
# I know these are grey buts it's required trust me
from pidev.kivy.ImageButton import ImageButton
from pidev.kivy import DPEAButton

from leaderboard import Leaderboard

time = time

screen_manager = ScreenManager()
target_screen_name = 'target'
player_screen_name = 'player'
end_screen_name = 'end'
instructions_screen_name = 'instructions'
leaderboard = Leaderboard()
player_count = 0 # probably can be phased out at some point
dpiStepper = DPiStepper()
dpiComputer = DPiComputer()
dpiPowerDriver = DPiPowerDrive()

dpiPowerDriver.setBoardNumber(0)
print(f"Pinging PowerDriver Board:{dpiPowerDriver.ping()}")
dpiStepper.setBoardNumber(0)
print(f"Pinging Stepper Board:{dpiStepper.ping()}")

# enable the stepper motors, when disabled the motors are turned off and spin freely
dpiStepper.enableMotors(True)
# set the microstepping to 1, 2, 4, 8, 16 or 32. 8 results in 1600 steps per
# revolution of the motor's shaft
dpiStepper.setMicrostepping(8)
stepper_num = 0
# set the speed in steps/second and acceleration in steps/second/second
dpiStepper.setSpeedInStepsPerSecond(stepper_num, 1600)
dpiStepper.setAccelerationInStepsPerSecondPerSecond(stepper_num, 1600)


GREEN_SOURCE = '../../assets/images/buttons/leds/green.png'
RED_SOURCE = '../../assets/images/buttons/leds/red.png'

SOUND_FILES = {
    "target_hit": '../../assets/sounds/target_hit.wav',
    "select": '../../assets/sounds/select.wav',
    "bronze_ding": '../../assets/sounds/bronze_ding.wav',
    "silver_ding": '../../assets/sounds/bronze_ding.wav',
    "gold_ding": '../../assets/sounds/bronze_ding.wav',
    "author_ding": '../../assets/sounds/bronze_ding.wav',
    "champion_ding": '../../assets/sounds/bronze_ding.wav',
    "quack": '../../assets/sounds/quack.mp3',
    "hit_1": '../../assets/sounds/hit_1.wav',
    "hit_2": '../../assets/sounds/hit_2.wav',
    "hit_3": '../../assets/sounds/hit_3.wav',
    "hit_4": '../../assets/sounds/hit_4.wav',
}
class Gamemode(Enum):
    """
        Planned Gamemode differentiation for the physical game. Physical game is supposed to have set levels, with players competing
        for top times on those individual levels. In theory(not written), if the gamemode is set to LEVELS, then pressing play takes
        you to a level selector screen.
    """
    RANDOM = 1
    LEVELS = 2

class GameState(Enum):
    """
        Enum for handling the state of the game.
    """
    IDLE = 1
    GET_NEW_LEDS = 2
    WAIT_FOR_TARGET_HIT = 3


class SubmitState(Enum):
    """
        Enum for handling player name entry on InstructionScreen.
    """
    PLAYER_ONE = 1
    PLAYER_TWO = 2

class TargetQuality(Enum):
    """
        Enum of each target quality
    """
    PRISMATIC_SHARD = "prismatic_shard"
    DIAMOND = "diamond"
    EMERALD = "emerald"
    AMETHYST = "amethyst"
    GOLD = "gold"

class Medal(Enum):
    """
        Enum of each medal
    """
    CHAMPION = "Champion"
    AUTHOR = "Author"
    GOLD = "Gold"
    SILVER = "Silver"
    BRONZE = "Bronze"
    NONE = "no_medal"

def play_sound(s):
    """
    :param s: one of the key's on line 75(SOUND_FILES)
    Plays the sound file at the value that the key refers to.
    """
    print(f"Playing Sound {s}")
    sound = SoundLoader.load(SOUND_FILES[s])
    sound.stop()
    sound.play()



class Player:
    """
        Class for each player
    """
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
        self.photoresistors = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]



    def add_score(self, add):
        """
        Adds add to score.
        :param add: int value to add
        :return: No return
        """
        self.score += add

    def get_leaderboard_position(self):
        """
        :return: int -> Place on the leaderboard for this players score
        """
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
#fullscreen = (1920, 1080)

#Window.size = fullscreen


def get_medals(player):
    """
    Gets what medal each player should have based on their score.
    :param player: The player ;)
    :return:
    """
    print(f"getting medals for player {player.name}")
    medal = Medal.NONE
    if player.score > 30000:
        medal = Medal.CHAMPION
    elif player.score > 27500:
        medal = Medal.AUTHOR
    elif player.score > 21000:
        medal = Medal.GOLD
    elif player.score > 10000:
        medal = Medal.SILVER
    elif player.score > 5000:
        medal = Medal.BRONZE
    print(f"{player.name} has the {medal}")
    return medal


class EndScreen(Screen):
    """
        Class for the EndScreen, which opens after a game is finished.
    """
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
        """
        On screen enter, get the players leaderboard position, score, and start the clock.
        """
        self.lpos_1 = player_one.get_leaderboard_position()
        self.lpos_2 = player_two.get_leaderboard_position()
        self.final_score_one = player_one.score
        self.final_score_two = player_two.score
        self.scheduled_event = Clock.schedule_interval(self.update_score, self.update_interval)


    def update_score(self, dt):
        """
        Clock function that's run every frame
        :param dt: Clock var(IDK)
        :return:
        """
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
        """
        Sets the text on the screen to the players leaderboard position.
        """
        self.ids.player_1_lpos.text = f"Top {str(self.lpos_1)} World"
        self.ids.player_2_lpos.text = f"Top {str(self.lpos_2)} World"


    def set_medals(self):
        """
        If either player has a medal, play the medal animation. If neither do, do nothing.
        """
        medal_one = get_medals(player_one)
        medal_two = get_medals(player_two)
        # medal_one = Medal.CHAMPION

        print(f"Getting Medals - p1:{medal_one}")
        if not medal_one == Medal.NONE:
            self.animate_medal(Medal.BRONZE, medal_one, player_one)
        elif not medal_two == Medal.NONE:
            self.animate_medal(Medal.BRONZE, medal_two, player_two)

    def animate_medal(self, medal, top_medal, player):
        """
        Recursive function. Animates a medal if the player has one. Keeps calling itself until the medal it's animating equals
        the top medal for the player.
        :param medal: The medal to animate
        :param top_medal: The last medal to animate
        :param player: Which player's medals to animate
        """
        if top_medal == Medal.NONE:
            medal = top_medal
            print("empty medal")
        if player == player_one:
            print(f"animating medal for player one: {medal}")
            x = 400
            widget = '_1'
        else:
            print(f"animating medal for player two: {medal}")
            x = 700
            widget = '_2'
        anim = Animation(x=x, y=(self.height / 2), size=(64, 64), duration=0.4)
        if medal == Medal.BRONZE and not top_medal == Medal.BRONZE:
            anim.bind(on_complete=lambda  *args: self.animate_medal(Medal.SILVER, top_medal, player))
            play_sound("bronze_ding")
        elif medal == Medal.SILVER and not top_medal == Medal.SILVER:
            anim.bind(on_complete=lambda  *args: self.animate_medal(Medal.GOLD, top_medal, player))
            play_sound("silver_ding")
        elif medal == Medal.GOLD and not top_medal == Medal.GOLD:
            anim.bind(on_complete=lambda  *args: self.animate_medal(Medal.AUTHOR, top_medal, player))
            play_sound("gold_ding")
        elif medal == Medal.AUTHOR and not top_medal == Medal.AUTHOR:
            anim = Animation(x=x, y=(self.height / 2), size=(64, 64), duration=0.7)
            anim.bind(on_complete=lambda  *args: self.animate_medal(Medal.CHAMPION, top_medal, player))
            play_sound("author_ding")
        elif medal == Medal.CHAMPION:
            anim = Animation(x=x, y=(self.height / 2), size=(64, 64), duration=0.7)
            print("last medal")
            play_sound("champion_ding")
        if medal == top_medal and player == player_one:
            if not medal == Medal.NONE:
                self.ids.player_1_medal_text.text = f"You got the {str(medal._value_)} medal!"
            anim.bind(on_complete= lambda *args: self.animate_medal(Medal.BRONZE, get_medals(player_two), player_two))
        if medal == top_medal and player == player_two and not medal == Medal.NONE:
            self.ids.player_2_medal_text.text = f"You got the {str(medal._value_)} medal!"
        if not medal == Medal.NONE:
            anim.start(widget=self.ids[medal.value + widget])

    @staticmethod
    def transition_to_player_screen():
        """
        Transition to player screen, with no transition animation
        """
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
        self.anti_double_click = False


    def button_pressed(self, key):
        """
        Calls when an image button on the keyboard is pressed. Appends the name with the key.
        :param key: Which key was pressed

        """
        if self.anti_double_click:
            self.anti_double_click = False
            return
        if self.ids.name.text == "l":
            self.ids.name.text = ""
        if key == "backspace":
            self.ids.name.text = self.ids.name.text[:-1]
        elif key in self.keys:
            self.ids.name.text += key.upper()
        self.anti_double_click = True


    def submit_text(self):
        """
        Calls when the submit button is pressed. If the state was PLAYER_ONE, then submit to player ones name, and set the state
        to player two. If the state was set to player two, remove the submit button and add a play button.
        """
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
    def nebulizer():
        dpiPowerDriver.switchDriverOnOrOff(0, True)
        dpiPowerDriver.switchDriverOnOrOff(2, True)

    @staticmethod
    def laser():
        dpiPowerDriver.switchDriverOnOrOff(1, True)

    """
    All of these methods below are self explanatory.
    """
    @staticmethod
    def transition_to_player_screen():
        screen_manager.transition = NoTransition()
        screen_manager.current = player_screen_name


    @staticmethod
    def transition_to_target_screen():
        print("transitioning to target_screen")
        screen_manager.transition = NoTransition()
        screen_manager.current = target_screen_name

    @staticmethod
    def transition_to_end_screen():
        screen_manager.transition = NoTransition()
        screen_manager.current = end_screen_name

    @staticmethod
    def exit():
        """
        Close the application. VERY IMPORTANT SO THAT YOU CAN LEAVE THE APP WHEN RUNNING ON RASPBERRY PI.
        :return:
        """
        dpiStepper.enableMotors(False)
        Window.close()


class PlayerScreen(Screen):
    """
        Class to handle player screen
    """
    def __init__(self, **kw):
        super().__init__(**kw)
        self.scheduled_event = None
        self.duck_counter = 0  # important trust
        self.duck_state = 0

    def on_enter(self, *args):
        self.get_leaderboard()

    def get_leaderboard(self):
        """
        Gets the top 10 names and scores from leaderboard and display's them
        """
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

    def duck(self):
        self.duck_counter += 1
        if self.duck_counter == 5:
            play_sound("quack")
            self.scheduled_event = Clock.schedule_interval(self.update_duck, 0.1)
            return
        elif self.duck_counter > 5:
            return
        play_sound(f"hit_{self.duck_counter}")


    def update_duck(self, dt):
        stationary = '../../assets/questionmark/questionmark_1.png'
        walking = '../../assets/questionmark/questionmark_2.png'
        print()
        print("running update_duck")
        if self.ids.duck.x > self.width:
            self.scheduled_event = False
        if self.duck_state == 4:
            self.ids.duck.source = stationary
            self.duck_state = 0
        elif self.duck_state == 2:
            self.ids.duck.source = walking
        self.duck_state += 1
        self.ids.duck.x += 1
        return self.scheduled_event


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

        self.fan_time_ms = None
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


        """
        Difficulty determines how likely additional targets besides the fist target are lit up. After the first target, the program runs
        a random number generator between 0 and 1. If the random number is <= 0.1, then light up a second target. 0.1 can be changed so 
        that it's more likely for additional targets to be lit up, which makes the game harder.
        """
        easy = 0.1
        medium = 0.3
        hard = 0.5
        impossible = 0.7
        self.difficulty = easy

    def on_enter(self, *args):
        dpiStepper.enableMotors(True)
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

    def spin_stepper(self, left, right):
        if left:
            self.left()
        elif right:
            self.right()

    def update_all(self, dt=None): # dt for clock scheduling
        #print(f"state={self.state}, target_move_to_pedestal_num={self.target_move_to_pedestal_num}, points={self.points}")
        self.update_time_left_image(self.update_time('s'))
        self.spin_stepper(dpiComputer.readDigitalIn(0), dpiComputer.readDigitalIn(1))
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

    def update_time(self, s):
        countdown_time = 3.5
        play_time = 16
        self.time_s = -round((time_ns() / 1000000000) - (self.time_start / 1000000000 + countdown_time + play_time)) # seconds counting down from 15 after start has been pressed
        self.time_ms = round((time_ns() / 1000000) - (self.time_start / 1000000)) # ms since start has been pressed
        player_one.target_lifetime = self.time_ms - player_one.target_appearance_time
        player_two.target_lifetime = self.time_ms - player_two.target_appearance_time
        if s == 's':
            return self.time_s
        elif s == 'ms':
            return self.time_ms
        else:
            return self.time_s


    def update_target_quality(self):
        for player in players:
            player_quality = TargetQuality.PRISMATIC_SHARD
            if player.target_lifetime > 900:
                player_quality = TargetQuality.GOLD
            elif player.target_lifetime > 675:
                player_quality = TargetQuality.AMETHYST
            elif player.target_lifetime > 475:
                player_quality = TargetQuality.EMERALD
            elif player.target_lifetime > 350:
                player_quality = TargetQuality.DIAMOND

            for i in range(0, len(player.visible_targets)):
                try:
                    player.visible_targets[i].source = f"../../assets/images/buttons/targets/{player_quality.value}_64.png"
                    player.visible_targets[i].quality = player_quality.value
                except AttributeError:
                    print("Attribute Error")

    def remove_target(self, target, led):
        for p in targets:
            for t in p:
                if t == target:
                    t.x = -65
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
                    target.x = -65

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
            points += 750
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
    def left():
        if dpiStepper.getStepperStatus(0)[1] == 1:
            print("hitting a wall")
            return
        print("Running left")
        dpiStepper.enableMotors(True)
        wait_to_finish_moving_flg = True
        velocity = -1600
        # move 1600 steps in the backward direction, this function will return after the
        # motor stops because "wait_to_finish_moving_flg" is set to True
        print(f"Attempting to move dpiStepper {stepper_num}, velocity={velocity}, wait_to_finish_moving_flg={wait_to_finish_moving_flg}")
        dpiStepper.moveToRelativePositionInSteps(stepper_num, velocity, wait_to_finish_moving_flg)

    @staticmethod
    def right():
        print("Running right")
        dpiStepper.enableMotors(True)
        wait_to_finish_moving_flg = True
        # move 1600 steps in the backward direction, this function will return after the
        # motor stops because "wait_to_finish_moving_flg" is set to True
        dpiStepper.moveToRelativePositionInSteps(0, 1600, wait_to_finish_moving_flg)

    @staticmethod
    def transition_to_player_screen():
        screen_manager.transition = NoTransition()
        screen_manager.current = player_screen_name

    @staticmethod
    def transition_to_end_screen():
        screen_manager.transition = NoTransition()
        screen_manager.current = end_screen_name

    @staticmethod
    def exit():
        """
        Close the application. VERY IMPORTANT SO THAT YOU CAN LEAVE THE APP WHEN RUNNING ON RASPBERRY PI.
        :return:
        """
        dpiStepper.enableMotors(False)
        Window.close()

Builder.load_file('../kv/main.kv')
LabelBase.register(name='PixelFont', fn_regular='../../assets/fonts/Tiny5-Regular.ttf')
screen_manager.add_widget(PlayerScreen(name=player_screen_name))
screen_manager.add_widget(TargetScreen(name=target_screen_name))
screen_manager.add_widget(InstructionsScreen(name=instructions_screen_name))
screen_manager.add_widget(EndScreen(name=end_screen_name))

if __name__ == "__main__":

    Window.fullscreen = 'auto' #uncomment this when actually loading on a screen, not computer screen
    LaserTargetCompetitionUI().run()