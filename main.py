import pygame
import sys
import math
import random

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 600))
screen_width = 800
screen_height = 600
current_time = 0
# creating players
playerImg = pygame.image.load('img/ping-pong.png')
px = screen_width / 2 - 40  # specifying x and y co ordinates to position player
py = screen_height - 70
player_speed = 1
p_score = 0

# creating opponent
oppImg = pygame.image.load('img/ping-pong.png')
ox = screen_width / 2 - 40
oy = 10
opp_speed = 1
op_score = 0

# Creating Game Shapes(Rectangles) We convert drawn rectangles to different shapes like ellipse
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 26, 26)

# defining movement for ball
ball_speedx = 1
ball_speedy = 1

# Creating Colors
ball_color = (200, 200, 200)  # pygame.Color('grey12') can also be used!
line_color = (255, 255, 255)

# Creating text to be rendered on screen
game_font = pygame.font.Font("freesansbold.ttf", 32)

# creating timer
time = None


def ball_start():
    global ball_speedy, ball_speedx, current_time, time
    current_time = pygame.time.get_ticks()
    ball.center = (screen_width / 2, screen_height / 2)
    game = game_font.render(("Game Begins in..."), True, (255, 255, 0))
    screen.blit(game, (20, 20))

    if current_time - time < 700:
        three = game_font.render("3", True, (255, 255, 255))
        screen.blit(three, (300, 20))

    if current_time > 700 and current_time - time < 1400:
        two = game_font.render("2", True, (255, 255, 255))
        screen.blit(two, (300, 20))

    if current_time > 1400 and current_time - time < 2100:
        one = game_font.render("1", True, (255, 255, 255))
        screen.blit(one, (300, 20))

    if current_time - time < 2100:
        ball_speedx = 0
        ball_speedy = 0
    else:
        ball_speedx = 1 * random.choice((-1, 1))
        ball_speedy = 1 * random.choice((-1, 1))
        time = None


# player function to draw image on screen
def player():
    screen.blit(playerImg, (px, py))


def opponent():
    screen.blit(oppImg, (ox, oy))


def ball_animation():
    global ball_speedy, ball_speedx, p_score, op_score, time
    ball.x += ball_speedx
    ball.y += ball_speedy
    # setting boundaries for ball
    if ball.top <= 0:
        p_score += 1
        ball_start()  # restarting the game when ball hits top or bottom boundary
        time = pygame.time.get_ticks()

    if ball.bottom >= screen_height:
        op_score += 1

        time = pygame.time.get_ticks()

        # ball_speedy *= -1
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speedx *= -1  # reversing speed for x axis movement


# collision of ball with player

def iscollisonP(px, py, ball_x, ball_y):
    global ball_speedy
    d = math.hypot(ball_x - px, ball_y - py)
    if d <= 40:
        ball_speedy *= -1


# collision of ball with opponent

def iscollisonOP(ox, oy, ball_x, ball_y):
    global ball_speedy, ball_speedx
    d = math.hypot(ball_x - ox, ball_y - oy)
    if d <= 40:
        ball_speedy *= -1


def player_animation():
    global px
    if px <= 64:
        px = 64
    if px >= screen_width - 74:
        px = screen_width - 80


def opponent_animation():
    global ox, oy, opp_speed
    if ox < ball.left:
        ox += opp_speed
    if ox > ball.right:
        ox -= opp_speed
    if ox <= 64:
        ox = 64
    if ox >= screen_width - 74:
        ox = screen_width - 80


while True:
    pygame.display.set_caption('Game On!')
    screen.fill((38, 171, 55))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            button_press_time = pygame.time.get_ticks()
            if event.key == pygame.K_RIGHT:
                player_speed += 1
            if event.key == pygame.K_LEFT:
                player_speed -= 1

    # Drawing ball on screen
    pygame.draw.ellipse(screen, ball_color, ball)
    pygame.draw.aaline(screen, line_color, (0, screen_height / 2), (screen_width, screen_height / 2))
    # player score display
    player_text = game_font.render(str(p_score), True, ball_color)
    screen.blit(player_text, (screen_width / 2, screen_height / 2 + 14))
    # Computer's score display
    opp_text = game_font.render(str(op_score), True, ball_color)
    screen.blit(opp_text, (screen_width / 2, screen_height / 2 - 34))
    # timer

    if time:
        ball_start()

    # Function Calls
    player()
    opponent()
    ball_animation()
    iscollisonP(px, py, ball.x, ball.y)
    iscollisonOP(ox, oy, ball.x, ball.y)
    px += player_speed
    player_animation()
    opponent_animation()

    pygame.display.update()
    # clock.tick(640)
