import sys
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ( 
    NumericProperty,ReferenceListProperty,ObjectProperty 
)
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint

#TODO - remove winnerLabel after restart
#TODO - center replay/quit buttons
#TODO - clean up game_over code
#TODO - change this syntax color

MAX_SCORE = 1

class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        game.start_clock()
        return game
        
        
class PongBall(Widget):
    # velocity of the ball on x and y axis
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    # referencelist property so we can use ball.velocity as
    # a shorthand, just like e.g. w.pos for w.x and w.y
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    
    # ``move`` function will move the ball one step. This
    #  will be called in equal intervals to animate the ball
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongPaddle(Widget):
    score = NumericProperty(0)
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            new_vel = bounced * 1.1
            ball.velocity = new_vel.x, new_vel.y + offset
    

class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self, vel=(4,0)):
        self.ball.center = self.center
        self.ball.velocity = vel
    
    def start_clock(self):
        self.game_loop = Clock.schedule_interval(self.update, 1.0/60.)
    
    def pause_clock(self):
        self.game_loop.cancel()
    
    def update(self, dt):
        self.ball.move()

        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce off top and bottom
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1
        
        # ball hits either side - score a point for the opposite player
        if self.ball.x < 0:
            self.player2.score += 1
            if self.player2.score >= MAX_SCORE:
                self.game_over()
            else:
                self.serve_ball(vel=(4,0)) 
        if self.ball.right > self.width:
            self.player1.score += 1
            if self.player1.score >= MAX_SCORE:
                self.game_over()
            else:
                self.serve_ball(vel=(-4,0))

    
    def on_touch_move(self, touch):
        if touch.x < self.width/3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width/3:
            self.player2.center_y = touch.y

    def restart_game(self, instance):
        self.player1.score = 0
        self.player2.score = 0
        self.serve_ball()
        self.start_clock()
    
    def exit_game(self, instance):
        sys.exit("Game over")

    def game_over(self):
        if self.player1.score > self.player2.score:
            winner = 'PLAYER 1 WINS'
        else:
            winner = 'PLAYER 2 WINS'
       
        winnerLabel = Label(
                            text=f"{winner}\nPlay Again?",
                            font_size=80,
                            center_x=self.center_x,
                            center_y=self.center_y)
        
        box = BoxLayout(orientation='horizontal')
        replayButton = Button(
                            text='REPLAY',
                            font_size=14)
        replayButton.bind(on_press=self.restart_game)
        quitButton = Button(
                            text='QUIT',
                            font_size=14)
        quitButton.bind(on_press=self.exit_game)
        box.add_widget(replayButton)
        box.add_widget(quitButton)
        self.add_widget(winnerLabel)
        self.add_widget(box)
        self.pause_clock()



if __name__ == '__main__':
    PongApp().run()
