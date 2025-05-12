from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout


class ScoreCounter(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.final_score = 50000
        self.current_score = 0
        self.update_interval = 0.01
        self.scheduled_event = Clock.schedule_interval(self.update_score, self.update_interval)
        self.slower = 0

    def update_score(self, dt):
        # Increase score faster at first, then slow down
        remaining = self.final_score - self.current_score
        if remaining > 10000:
            self.current_score += 200
        if remaining > 5000:
            self.current_score += 107
        elif remaining > 2500:
            self.current_score += 51
        elif remaining > 125:
            self.current_score += 28
        elif remaining > 65:
            self.current_score += 13
        elif remaining > 10:
            self.slower += 1
            if self.slower == 2:
                self.current_score += 1
                self.slower = 0
        elif remaining > 3:
            self.slower += 1
            if self.slower == 16:
                self.current_score += 1
                self.slower = 0
        else:
            self.slower += 1
            if self.slower == 32:
                self.current_score += 1
                self.slower = 0


        if self.current_score >= self.final_score:
            self.current_score = self.final_score
            self.text = str(self.current_score)
            self.scheduled_event.cancel()
            return

        self.text = str(self.current_score)


class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__()
        self.score_label = None

    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.score_label = ScoreCounter()
        layout.add_widget(self.score_label)
        return layout


if __name__ == '__main__':
    MyApp().run()
