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
boss_alien = None
boss_spawned = False


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
import math
import random

class Alien:
    def __init__(self, screen_width, screen_height, speed, health=3):
        # Determine spawn side: 0 = top, 1 = bottom, 2 = left, 3 = right
        self.spawn_side = random.choice([0, 1, 2, 3])
        self.speed = speed
        self.health = health
        self.is_dodged = False

        # Initialize position based on the spawn side
        if self.spawn_side == 0:  # Top
            self.x = random.uniform(0, screen_width)
            self.y = screen_height
        elif self.spawn_side == 1:  # Bottom
            self.x = random.uniform(0, screen_width)
            self.y = 0
        elif self.spawn_side == 2:  # Left
            self.x = 0
            self.y = random.uniform(0, screen_height)
        elif self.spawn_side == 3:  # Right
            self.x = screen_width
            self.y = random.uniform(0, screen_height)

        # Target a random point near the center or other areas
        self.target_x = random.uniform(screen_width * 0.3, screen_width * 0.7)
        self.target_y = random.uniform(screen_height * 0.3, screen_height * 0.7)

    def move(self):
        if not self.is_dodged:
            # Move towards the target point
            angle = math.atan2(self.target_y - self.y, self.target_x - self.x)
            self.x += self.speed * math.cos(angle)
            self.y += self.speed * math.sin(angle)
        else:
            # Move upward if dodged (or implement your own logic)
            self.y -= self.speed

    def is_hit(self, bullet):
        # Check if the alien is hit by a bullet
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
#Boss alien
class BossAlien:
    def __init__(self, x, y, size=50, health=20):
        self.x = x
        self.y = y
        self.size = size
        self.health = health
        self.projectiles = []  # List to store boss projectiles
        self.movement_counter = 0
        self.movement_direction = 1  # Determines whether the boss moves left or right

    def move(self, screen_width):
        # Boss moves left and right periodically
        self.movement_counter += 1
        if self.movement_counter >= 60:  # Change direction every 60 frames
            self.movement_direction *= -1
            self.movement_counter = 0
        self.x += self.movement_direction * 2  # Adjust speed as needed
        self.x = max(self.size, min(screen_width - self.size, self.x))  # Keep boss within screen bounds

    def shoot(self):
        # Boss shoots a projectile downward
        self.projectiles.append({'x': self.x, 'y': self.y - self.size, 'speed': -5})

    def update_projectiles(self):
        # Update the position of projectiles and remove those off-screen
        for projectile in self.projectiles[:]:
            projectile['y'] += projectile['speed']
            if projectile['y'] < 0:
                self.projectiles.remove(projectile)

    def draw(self):
        # Body: Donut Shape (Yellow)
        glColor3f(1.0, 1.0, 0.0)  # Yellow for the outer circle
        glBegin(GL_POLYGON)
        for angle in range(360):
            theta = math.radians(angle)
            dx = self.size * math.cos(theta)
            dy = self.size * math.sin(theta)
            glVertex2f(self.x + dx, self.y + dy)
        glEnd()

        # Hole: Inner Circle (Background color to carve out the hole)
        glColor3f(0.0, 0.0, 0.0)  # Black (or replace with the background color)
        glBegin(GL_POLYGON)
        for angle in range(360):
            theta = math.radians(angle)
            dx = self.size * 0.5 * math.cos(theta)  # Inner radius for the hole
            dy = self.size * 0.5 * math.sin(theta)
            glVertex2f(self.x + dx, self.y + dy)
        glEnd()

        # Eyes: Positioned like umbrella handle holders outside the hole
        glColor3f(1.0, 0.0, 0.0)  # Bright Red
        # Left Eye
        glBegin(GL_POLYGON)
        for angle in range(360):
            theta = math.radians(angle)
            dx = self.size * 0.1 * math.cos(theta)
            dy = self.size * 0.1 * math.sin(theta)
            glVertex2f(
                self.x - self.size * 0.6 + dx,  # Position left of the body
                self.y + self.size * 0.7 + dy  # Above the outer edge
            )
        glEnd()

        # Right Eye
        glBegin(GL_POLYGON)
        for angle in range(360):
            theta = math.radians(angle)
            dx = self.size * 0.1 * math.cos(theta)
            dy = self.size * 0.1 * math.sin(theta)
            glVertex2f(
                self.x + self.size * 0.6 + dx,  # Position right of the body
                self.y + self.size * 0.7 + dy  # Above the outer edge
            )
        glEnd()

        # Health Bar
        glColor3f(0.0, 1.0, 0.0)  # Green for health
        glBegin(GL_QUADS)
        glVertex2f(self.x - self.size, self.y + self.size + 10)
        glVertex2f(self.x - self.size, self.y + self.size + 15)
        glVertex2f(self.x - self.size + 2 * self.size * (self.health / 20), self.y + self.size + 15)
        glVertex2f(self.x - self.size + 2 * self.size * (self.health / 20), self.y + self.size + 10)
        glEnd()

        # Draw projectiles
        for projectile in self.projectiles:
            glColor3f(1.0, 1.0, 0.0)  # Yellow
            glBegin(GL_QUADS)
            glVertex2f(projectile['x'] - 5, projectile['y'])
            glVertex2f(projectile['x'] + 5, projectile['y'])
            glVertex2f(projectile['x'] + 5, projectile['y'] + 10)
            glVertex2f(projectile['x'] - 5, projectile['y'] + 10)
            glEnd()


    def is_hit(self, bullet):
            """
            Check if the boss is hit by a bullet.
            
            The boss has a circular hitbox for its body. 
            For more precise collision detection, adjust for arms or spikes if needed.
            """
            # Distance from bullet to boss center
            distance = math.sqrt((self.x - bullet.x) ** 2 + (self.y - bullet.y) ** 2)
            
            # Check if the bullet hits the main body (donut shape)
            if distance < self.size:
                return True
            
            # Optional: Check collision with arms or spikes
            # Left spike
            spike_left_x = self.x - self.size * 1.35  # Center of left spike
            spike_left_y = self.y
            distance_to_left_spike = math.sqrt((spike_left_x - bullet.x) ** 2 + (spike_left_y - bullet.y) ** 2)
            
            # Right spike
            spike_right_x = self.x + self.size * 1.35  # Center of right spike
            spike_right_y = self.y
            distance_to_right_spike = math.sqrt((spike_right_x - bullet.x) ** 2 + (spike_right_y - bullet.y) ** 2)
            
            # Hit detection for spikes
            if distance_to_left_spike < self.size * 0.3 or distance_to_right_spike < self.size * 0.3:
                return True

            return False


def spawn_boss():
    global boss_alien, boss_spawned
    if not boss_spawned and len(aliens) >= 10:  # Adjust condition as needed
        boss_alien = BossAlien(WIDTH // 2, HEIGHT - 100)  # Spawn boss at the top center
        boss_spawned = True


def check_boss_collision(bullets):
    global boss_spawned, boss_alien
    if boss_spawned:
        for bullet in bullets[:]:  # Iterate over a copy to avoid modification issues
            if boss_alien.is_hit(bullet):
                print("Boss hit!")
                boss_alien.health -= 1
                bullets.remove(bullet)  # Remove bullet after collision
                if boss_alien.health <= 0:
                    print("Boss defeated!")
                    boss_spawned = False  # Remove boss after it's defeated

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
    global running
    # Call spawn_boss to check if conditions are met
    spawn_boss()
    
    # Draw aliens
    for alien in aliens:
        alien.move()
        alien.draw()
        global running
    # Move and draw bullets
    for bullet in bullets:
        bullet.move()
        bullet.draw()

    # Check collision between boss and bullets
    check_boss_collision(bullets)
    # Draw the boss if spawned
    if boss_spawned:

        boss_alien.draw()
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
