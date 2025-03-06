
from pidev.kivy.ImageButton import ImageButton

from main import PlayerScreen

class DrawingHandler:

    def draw(self, letter, x, y):
        match letter:
            case 'a':
                print("drawing an a")
                PlayerScreen.add_widget(ImageButton(
                    source='assets/images/text/name.png',
                    x= x,
                    y= y,
                    size=(144, 44)
                ))
