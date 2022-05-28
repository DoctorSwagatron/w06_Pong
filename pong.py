"""
By Kevin Davis
for BYUI CSE 210
"""
import arcade #allows the python game library to do its thing 
import random #brings in randomization from Python library! Used for color changing and velocity changing

"""Global Variables!"""
#Game variables
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCORE = 1 #how many points are earned by each point

#Ball Variables
BALL_RADIUS = 10 #how wide the ball is
COLORS = [arcade.color.YELLOW, arcade.color.BLUE, arcade.color.ORANGE, arcade.color.GREEN, arcade.color.PURPLE]
BALL_VELOCITY = [-5, -4, -3, -6, 6, 3, 4, 5]
CONTACT_VELOCITY = -1.1 #Causes the ball to speed up every time it hits a paddle  

#Paddle variables
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
MOVE_AMOUNT = 10 #how many pixels the paddles move by


class Game(arcade.Window):
    """The game class! Makes the screen appear, and makes the drawing, updating, and other things run"""
    def __init__(self, width, height):
        #INITIALIZE!!!!
        super().__init__(width, height)
        #creates the objects - ball and paddles
        self.ball = Ball()
        self.paddle = Paddle()
        self.paddletwo = PaddleTwo()
        #initialize scores to zero
        self.score = 0
        self.scoretwo = 0
        #starts motion of the paddles at zero - assume we're not pressing the buttons
        self.holding_left = False
        self.holding_right = False
        self.holding_left_two = False
        self.holding_right_two = False

        arcade.set_background_color(arcade.color.BLACK) 

    def on_draw(self):
        """
        Draws all the objects
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # draw each object
        self.ball.draw()
        self.paddle.draw()
        self.paddletwo.draw()

        self.draw_score()

    def draw_score(self):
        """
        Puts the current score on the screen
        """
        #Handles scores for the CYAN player
        score_text = "Score: {}".format(self.score)
        start_x = 10+ PADDLE_WIDTH
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=self.ball.color)
        #Handles the scores for the RED player 
        score_text_two = "Score: {}".format(self.scoretwo)
        start_x_two = SCREEN_WIDTH-80 - PADDLE_WIDTH
        start_y_two = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text_two, start_x=start_x_two, start_y=start_y_two, font_size=12, color=self.ball.color)

    def update(self, delta_time):
        """
        Update each object in the game as it moves. 
        """

        # Move the ball forward one element in time
        self.ball.advance()

        # Check to see if keys are being held, and then do stuff
        self.check_keys()

        # check for ball at important places
        self.check_miss()
        self.check_hit()
        self.check_bounce()

    def check_hit(self):
        """
        Check for collisions! If so do things
        """
        too_close_x = (PADDLE_WIDTH / 2) + BALL_RADIUS
        too_close_y = (PADDLE_HEIGHT / 2) + BALL_RADIUS

        if (abs(self.ball.center.x - self.paddle.center.x) < too_close_x and
                    abs(self.ball.center.y - self.paddle.center.y) < too_close_y and
                    self.ball.velocity.dx > 0):
            # we are too close and moving RIGHT, this is a hit!
            self.ball.bounce_horizontal()
        if (abs(self.ball.center.x - self.paddletwo.center.x) < too_close_x and
                    abs(self.ball.center.y - self.paddletwo.center.y) < too_close_y and
                    self.ball.velocity.dx < 0):
            # we are too close and moving LEFT, this is a hit!
            self.ball.bounce_horizontal()

    def check_miss(self):
        """
        Checks to see if the ball went past the paddle
        and if so, restarts it.
        """
        if self.ball.center.x > SCREEN_WIDTH:
            # We missed RIGHT!
            self.score += SCORE
            self.ball.restart()
        if self.ball.center.x < 0:
            # We missed LEFT!
            self.scoretwo += SCORE
            self.ball.restart()

        

    def check_bounce(self):
        """
        Checks to see if the ball has hit the borders
        of the screen OR the paddles, and if so, calls its bounce methods.
        """
        if self.ball.center.y < 0 and self.ball.velocity.dy < 0:
            self.ball.bounce_vertical()

        if self.ball.center.y > SCREEN_HEIGHT and self.ball.velocity.dy > 0:
            self.ball.bounce_vertical()

    def check_keys(self):
        """
        Checks to see if the user is holding down an
        arrow key, and if so, takes appropriate action.
        """
        #These control the CYAN paddle (right side of the screen)
        if self.holding_left:
            self.paddle.move_down()

        if self.holding_right:
            self.paddle.move_up()
        #These control the RED paddle (left side of the screen)
        if self.holding_left_two:
            self.paddletwo.move_down()

        if self.holding_right_two:
            self.paddletwo.move_up()

    def on_key_press(self, key, key_modifiers):
        """
        Performs an action when keys are pressed
        """
        #These control the CYAN paddle (right side of the screen)
        if key == arcade.key.LEFT or key == arcade.key.DOWN:
            self.holding_left = True

        if key == arcade.key.RIGHT or key == arcade.key.UP:
            self.holding_right = True
        
        #These control the RED paddle (left side of the screen)
        if key == arcade.key.S or key == arcade.key.A:
            self.holding_left_two = True
        
        if key == arcade.key.D or key == arcade.key.W:
            self.holding_right_two = True

    def on_key_release(self, key, key_modifiers):
        """
        Stops performing the action when the keys are released 
        """
        #These control the CYAN paddle (right side of the screen)
        if key == arcade.key.LEFT or key == arcade.key.DOWN:
            self.holding_left = False

        if key == arcade.key.RIGHT or key == arcade.key.UP:
            self.holding_right = False
                
        #These control the RED paddle (left side of the screen)
        if key == arcade.key.S or key == arcade.key.A:
            self.holding_left_two = False   
        
        if key == arcade.key.D or key == arcade.key.W:
            self.holding_right_two = False

class Ball ():
    """Handles drawing, and logic of the ball"""
    def __init__(self):
        """INITIALIZE. THAT. FUNCTION!!!"""
        self.velocity = Velocity()
        self.center = Point()
        self.center.x = SCREEN_WIDTH/2
        self.center.y = random.uniform(0, SCREEN_HEIGHT)
        self.velocity.dx = BALL_VELOCITY[random.randint(0,7)]
        self.velocity.dy = random.uniform(1,5)
        self.color = COLORS[random.randint(0,4)] 
    
    def draw(self):
        """This method calls from arcade the logic that renders the ball on screen! 
        (and sets to self.color -which does some cool stuff later) ;)"""
        arcade.draw_circle_filled(self.center.x, self.center.y, BALL_RADIUS, self.color)
    
    def advance(self):
        """Handles motion of the ball across the screen"""
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy

    def bounce_horizontal(self):
        """Handles change in direction when the ball hits a paddle"""
        self.velocity.dx *= CONTACT_VELOCITY
        self.color = COLORS[random.randint(0,4)] #THIS! This is the cool stuff! When it hits the paddle, change the color of the ball!
        #(actually, this does more than that - but hang tight. I'll tell you more in a bit.

    def bounce_vertical(self):
        """Handles change in direction when the ball hits the top or bottom"""
        self.velocity.dy *= -1
        self.color = COLORS[random.randint(0,4)] #OH YEAH! LOOK! I change the color of the ball when I hit the top or bottom too! :)
    
    def restart(self):
        """Restart class! puts the ball back in the middle with a randomized velocity (see above)"""
        self.__init__()

class Point():
    """This tracks the center of any object that is moving in the game - ball or paddle"""
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
    

class Velocity():
    #This tracks the velocity of any object in game - ball or paddle
   def __init__(self):
       self.dx = 2.0
       self.dy = 2.0


class Paddle():
    """Hello! I am the CYAN paddle! I am on the RIGHT side of the screen.
    This class handles everything I do - from drawing me, to tracking my motion"""
    def __init__(self):
        #INITIALIZE THAT FUNCTION!!!!1
        self.center = Point() #enables tracking of the paddle
        self.center.x = SCREEN_WIDTH - 20 #We want it on the right side of the screen, but not off the screen. 
        
    def draw(self):
        #Make the magic happen - the paddle (a rectangle) on the screen.
        arcade.draw_rectangle_filled(self.center.x, self.center.y, PADDLE_WIDTH, PADDLE_HEIGHT, arcade.color.CYAN)

    def move_up(self):
        #handles moving up
        if self.center.y < SCREEN_HEIGHT-PADDLE_HEIGHT/2:
            self.center.y += MOVE_AMOUNT

    def move_down(self):
        #handles moving down
        if self.center.y > 0+PADDLE_HEIGHT/2:
            self.center.y -= MOVE_AMOUNT

class PaddleTwo(Paddle):
    """Hello! I am the RED paddle! I am on the LEFT side of the screen.
    This class handles everything I do - from drawing me, to tracking my motion"""
    def __init__(self):
        #INITIALIZE! (sounds like star trek) 
        self.center = Point()
        self.center.x = 20
    def draw(self):
        #Draw - aka make rectangle appear :) 
        arcade.draw_rectangle_filled(self.center.x, self.center.y, PADDLE_WIDTH, PADDLE_HEIGHT, arcade.color.RED)
    def move_up(self):
        #handles moving up
        if self.center.y < SCREEN_HEIGHT-PADDLE_HEIGHT/2:
            self.center.y += MOVE_AMOUNT
    def move_down(self):
        #handles moving down :O
        if self.center.y > 0+PADDLE_HEIGHT/2:
            self.center.y -= MOVE_AMOUNT
    

# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()