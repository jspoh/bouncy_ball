# attempt at making a ball with physics - bounce off the ground/wall, movement acceleration, and friction
# sorry for the messy code lol this is the first program I'm making after learning classes
# this program is controlled via arrow keys

import pygame
import random
import time

pygame.init()

win_width = 600
win_height = 600

window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Boing")

c_white = (255, 255, 255)
c_amber = (80, 80, 50)

win_border = 7  # there's a weird border thing to account for (change it to 0 to see what I mean)


class Collisions:
    def __init__(self):
        self.grounded = False  # in order to prevent the ball from slowing down while in the air (see friction)

    def ground(self):
        if ball.y + ball.radius > win_height - win_border:
            self.grounded = True
            ball.y = win_height - ball.radius - win_border
            ball.dy = -ball.dy * ball.bounciness
        else:
            self.grounded = False

    def wall(self):
        if ball.x - ball.radius < 0 + win_border:
            ball.x = 0 + ball.radius + win_border
            ball.dx = -ball.dx
        elif ball.x + ball.radius > win_width - win_border:
            ball.x = win_width - ball.radius - win_border
            ball.dx = -ball.dx


class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10
        self.dx = 0
        self.dy = 0
        self.direction = ""
        self.ball_max_speed = 100
        self.acceleration = 0.1
        self.ball_terminal_velocity = 100
        self.jump_force = 5
        self.bounciness = 0.7
        self.ground_friction = 0.05
        self.air_friction = 0.01

    def draw_ball(self):
        pygame.draw.circle(surface=window, color=c_white, center=(self.x, self.y), radius=self.radius)

    def gravity(self):
        if self.dy < self.ball_terminal_velocity:
            self.dy += 0.1
        else:
            self.dy = self.ball_terminal_velocity
        self.y += self.dy

    def movement(self, direction):
        if direction == "left":
            if self.dx > -self.ball_max_speed:
                self.dx -= self.acceleration
            elif self.dx < -self.ball_max_speed:
                self.dx = -self.ball_max_speed
        elif direction == "right":
            if self.dx < self.ball_max_speed:
                self.dx += self.acceleration
            elif self.dx > self.ball_max_speed:
                self.dx = self.ball_max_speed
        elif direction == "":
            if self.dx > 0:  # moving to the right
                if self.dx < 0.1:  # stop when speed is low enough
                    self.dx = 0
                elif col.grounded:  # if ball is on the ground, higher friction
                    self.dx -= self.ground_friction
                elif not col.grounded:  # if ball is in the air, lower friction
                    self.dx -= self.air_friction
            elif self.dx < 0:  # moving to the left
                if self.dx > -0.1:
                    self.dx = 0
                elif col.grounded:
                    self.dx += self.ground_friction
                elif not col.grounded:
                    self.dx += self.air_friction
        self.x += self.dx
#        print(self.dx)  # activate to check current dx lol (may lag program)

    def jump(self):
        self.dy = -self.jump_force

    def show_pos(self):
        print(self.x, self.y)


ball = Ball(random.randint(0, win_width), random.randint(0, win_height))
col = Collisions()


running = True
while running:
    window.fill(color=c_amber)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ball.direction = "left"
            if event.key == pygame.K_RIGHT:
                ball.direction = "right"
            if event.key == pygame.K_UP:
                ball.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                ball.direction = ""

    col.ground()
    col.wall()

    ball.movement(ball.direction)
#    ball.show_pos()  # activate to show ball pos lol (may lag the program)
    ball.gravity()
    ball.draw_ball()

    time.sleep(0.01)

    pygame.display.update()
