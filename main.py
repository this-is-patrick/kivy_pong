from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import ( 
    NumericProperty,ReferenceListProperty,ObjectProperty 
)
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint

MAX_SCORE = 1

class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
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
                self.end_game()
            else:
                self.serve_ball(vel=(4,0)) 
        if self.ball.right > self.width:
            self.player1.score += 1
            if self.player1.score >= MAX_SCORE:
                self.end_game()
            else:
                self.serve_ball(vel=(-4,0))

    
    def on_touch_move(self, touch):
        if touch.x < self.width/3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width/3:
            self.player2.center_y = touch.y


    def end_game(self):
        if self.player1.score > self.player2.score:
            winner = 'PLAYER 1 WINS'
        else:
            winner = 'PLAYER 2 WINS'
        
        winnerLabel = Label(text=f"{winner}", font_size=80, center_x=self.center_x, center_y=self.center_y)
        self.add_widget(winnerLabel)


if __name__ == '__main__':
    PongApp().run()
