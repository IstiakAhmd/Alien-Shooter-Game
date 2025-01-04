from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Constants
WIDTH = 800
HEIGHT = 600
STEP = 0.26
ALIEN_SPAWN_INTERVAL = 120
BULLET_SPEED = 2
PLAYER_HEALTH = 3

# Globals
character_x = WIDTH // 2
character_y = HEIGHT // 2
player_health = PLAYER_HEALTH
mouse_x = WIDTH // 2
mouse_y = HEIGHT // 2
keys = {b'w': False, b'a': False, b's': False, b'd': False}
aliens = []
bullets = []
frame_count = 0


# Classes
class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = BULLET_SPEED

    def move(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

    def draw(self):
        glColor3f(1.0, 0.0, 0.0)
        glPointSize(5)
        glBegin(GL_POINTS)
        glVertex2f(self.x, self.y)
        glEnd()


class Alien:
    def __init__(self, x, y, speed, health=3):
        self.x = x
        self.y = y
        self.speed = speed
        self.is_dodged = False
        self.health = health

    def move(self):
        if not self.is_dodged:
            angle = math.atan2(character_y - self.y, character_x - self.x)
            self.x += self.speed * math.cos(angle)
            self.y += self.speed * math.sin(angle)
        else:
            self.y -= self.speed

    def is_hit(self, bullet):
        distance = math.sqrt((self.x - bullet.x) ** 2 + (self.y - bullet.y) ** 2)
        return distance < 10

    def draw(self):
        glColor3f(1.6, 0.0, 1.0)
        glPointSize(2)
        glBegin(GL_POINTS)
        for i in range(360):
            theta = math.radians(i)
            dx = 10 * math.cos(theta)
            dy = 10 * math.sin(theta)
            glVertex2f(self.x + dx, self.y + dy)
        glEnd()

        glColor3f(1.0, 1.0, 0.0)
        glPointSize(2)
        glBegin(GL_POINTS)
        for i in range(8):
            glVertex2f(self.x - 3 - i, self.y + 10 + i)
            glVertex2f(self.x + 3 + i, self.y + 10 + i)
        glEnd()

        glColor3f(0.0, 1.0, 0.0)
        glPointSize(3.5)
        glBegin(GL_POINTS)
        glVertex2f(self.x - 3, self.y + 3)
        glVertex2f(self.x + 3, self.y + 3)
        glEnd()

        glColor3f(1.0, 1.0, 0.0)
        glPointSize(2)
        glBegin(GL_POINTS)
        for i in range(3):
            glVertex2f(self.x - 10 - i, self.y - 3 + i)
        for i in range(8):
            glVertex2f(self.x - 13, self.y - 5 - i)
        for i in range(3):
            glVertex2f(self.x + 10 + i, self.y - 3 + i)
        for i in range(8):
            glVertex2f(self.x + 13, self.y - 5 - i)
        glEnd()


# Helper Functions
def spawn_bullets():
    angle = math.atan2(mouse_y - character_y, mouse_x - character_x)
    arm_length = 10
    left_gun_x = character_x - 8 + arm_length * math.cos(angle)
    left_gun_y = character_y + 10 + arm_length * math.sin(angle)
    right_gun_x = character_x + 8 + arm_length * math.cos(angle)
    right_gun_y = character_y + 10 + arm_length * math.sin(angle)
    bullets.append(Bullet(left_gun_x, left_gun_y, angle))
    bullets.append(Bullet(right_gun_x, right_gun_y, angle))


def draw_bullets():
    for bullet in bullets:
        bullet.draw()

def draw_character():
    global mouse_x, mouse_y, character_x, character_y

    # Calculate the angle between the character and the mouse
    angle = math.atan2(mouse_y - character_y, mouse_x - character_x)

    # Head (filled circle)
    glColor3f(1.0, 0.8, 0.6)  # Skin tone color
    glBegin(GL_POLYGON)
    for i in range(360):
        theta = math.radians(i)
        dx = 5 * math.cos(theta)  # Radius for the head
        dy = 5 * math.sin(theta)
        glVertex2f(dx, 15 + dy)  # Positioned above the body
    glEnd()

    # Body (filled rectangle)
    glColor3f(0.0, 0.0, 1.0)  # Blue color for the body
    glBegin(GL_POLYGON)
    glVertex2f(-8, -10)
    glVertex2f(8, -10)
    glVertex2f(8, 10)
    glVertex2f(-8, 10)
    glEnd()

    # Belt (horizontal line)
    glColor3f(0.5, 0.2, 0.0)  # Brown color for the belt
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2f(-8, -2)
    glVertex2f(8, -2)
    glEnd()

    # Arms
    glColor3f(1.0, 0.8, 0.6)  # Skin tone color for arms
    arm_length = 10
    glBegin(GL_LINES)
    # Left arm
    glVertex2f(-8, 10)
    glVertex2f(-8 + arm_length * math.cos(angle), 10 + arm_length * math.sin(angle))
    # Right arm
    glVertex2f(8, 10)
    glVertex2f(8 + arm_length * math.cos(angle), 10 + arm_length * math.sin(angle))
    glEnd()

    # Guns
    glColor3f(0.2, 0.2, 0.2)  # Dark gray color for the guns
    gun_length = 10
    gun_thickness = 2
    glBegin(GL_QUADS)
    # Left gun
    left_arm_x = -8 + arm_length * math.cos(angle)
    left_arm_y = 10 + arm_length * math.sin(angle)
    glVertex2f(left_arm_x, left_arm_y)
    glVertex2f(left_arm_x + gun_length * math.cos(angle), left_arm_y + gun_length * math.sin(angle))
    glVertex2f(left_arm_x + gun_length * math.cos(angle) - gun_thickness * math.sin(angle),
               left_arm_y + gun_length * math.sin(angle) + gun_thickness * math.cos(angle))
    glVertex2f(left_arm_x - gun_thickness * math.sin(angle), left_arm_y + gun_thickness * math.cos(angle))

    # Right gun
    right_arm_x = 8 + arm_length * math.cos(angle)
    right_arm_y = 10 + arm_length * math.sin(angle)
    glVertex2f(right_arm_x, right_arm_y)
    glVertex2f(right_arm_x + gun_length * math.cos(angle), right_arm_y + gun_length * math.sin(angle))
    glVertex2f(right_arm_x + gun_length * math.cos(angle) - gun_thickness * math.sin(angle),
               right_arm_y + gun_length * math.sin(angle) + gun_thickness * math.cos(angle))
    glVertex2f(right_arm_x - gun_thickness * math.sin(angle), right_arm_y + gun_thickness * math.cos(angle))
    glEnd()

    # Legs
    glColor3f(0.0, 0.0, 0.0)  # Black color for legs
    glBegin(GL_LINES)
    # Left leg
    glVertex2f(-4, -10)
    glVertex2f(-6, -20)
    # Right leg
    glVertex2f(4, -10)
    glVertex2f(6, -20)
    glEnd()

def spawn_alien():
    x = random.randint(0, WIDTH)
    y = HEIGHT
    speed = 0.05
    aliens.append(Alien(x, y, speed))


def check_collisions():
    global bullets, aliens
    updated_bullets = []
    for bullet in bullets:
        hit = False
        for alien in aliens:
            if alien.is_hit(bullet):
                alien.health -= 1
                hit = True
                break
        if not hit:
            updated_bullets.append(bullet)
    bullets = updated_bullets
    aliens = [alien for alien in aliens if alien.health > 0]


def check_collision_with_player(alien):
    distance = math.sqrt((alien.x - character_x) ** 2 + (alien.y - character_y) ** 2)
    return distance < 20


def update_aliens():
    global player_health, aliens
    updated_aliens = []
    for alien in aliens:
        alien.move()
        if check_collision_with_player(alien):
            player_health -= 1
            if player_health <= 0:
                print("Game Over!")
        else:
            updated_aliens.append(alien)
    aliens = updated_aliens


def update_bullets():
    global bullets
    updated_bullets = []
    for bullet in bullets:
        bullet.move()
        if 0 <= bullet.x <= WIDTH and 0 <= bullet.y <= HEIGHT:
            updated_bullets.append(bullet)
    bullets = updated_bullets


def update_character_position():
    global character_x, character_y
    if keys[b'w']:
        character_y += STEP
    if keys[b's']:
        character_y -= STEP
    if keys[b'a']:
        character_x -= STEP
    if keys[b'd']:
        character_x += STEP
    character_x = max(10, min(WIDTH - 10, character_x))
    character_y = max(10, min(HEIGHT - 10, character_y))


def iterate():
    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, WIDTH, 0.0, HEIGHT, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


# GLUT Callbacks
def show_screen():
    global frame_count
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    update_character_position()
    frame_count += 1
    if frame_count >= ALIEN_SPAWN_INTERVAL:
        spawn_alien()
        frame_count = 0
    update_aliens()
    update_bullets()
    check_collisions()
    glPushMatrix()
    glTranslatef(character_x, character_y, 0)
    draw_character()
    glPopMatrix()
    draw_bullets()
    for alien in aliens:
        alien.draw()
    glutSwapBuffers()


def key_down(key, x, y):
    if key in keys:
        keys[key] = True


def key_up(key, x, y):
    if key in keys:
        keys[key] = False


def mouse_motion(x, y):
    global mouse_x, mouse_y
    mouse_x = x
    mouse_y = HEIGHT - y


def mouse_click(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        spawn_bullets()


# Main
glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(WIDTH, HEIGHT)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Alien Shooter Game")
glutDisplayFunc(show_screen)
glutIdleFunc(show_screen)
glutKeyboardFunc(key_down)
glutKeyboardUpFunc(key_up)
glutPassiveMotionFunc(mouse_motion)
glutMouseFunc(mouse_click)
glutMainLoop()
