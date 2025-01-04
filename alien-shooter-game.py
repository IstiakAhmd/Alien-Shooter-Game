from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Window dimensions
width = 800
height = 600

# Character position
character_x = width // 2
character_y = height // 2

# Movement step size
step = .26

# Mouse position
mouse_x = width // 2
mouse_y = height // 2

# Key state dictionary
keys = {b'w': False, b'a': False, b's': False, b'd': False}
# List to store aliens
aliens = []

# Alien appearance interval (frames)
alien_spawn_interval = 120  # Adjust for difficulty
frame_count = 0
# List to store bullets
bullets = []
class Bullet:
    """Class to represent a bullet fired from the character's guns."""
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 2  # Speed of the bullet

    def move(self):
        """Move the bullet in the direction of its angle."""
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

    def draw(self):
        """Draw the bullet."""
        glColor3f(1.0, 0.0, 0.0)  # Red color for the bullet
        glPointSize(5)  # Bullet size
        glBegin(GL_POINTS)
        glVertex2f(self.x, self.y)
        glEnd()

def spawn_bullets():
    """Spawn bullets from both guns towards the mouse click position."""
    global mouse_x, mouse_y, character_x, character_y

    # Calculate the angle to the target
    angle = math.atan2(mouse_y - character_y, mouse_x - character_x)

    # Spawn two bullets, one from each gun
    arm_length = 10  # Length of the arm
    left_gun_x = character_x - 8 + arm_length * math.cos(angle)
    left_gun_y = character_y + 10 + arm_length * math.sin(angle)
    right_gun_x = character_x + 8 + arm_length * math.cos(angle)
    right_gun_y = character_y + 10 + arm_length * math.sin(angle)

    bullets.append(Bullet(left_gun_x, left_gun_y, angle))
    bullets.append(Bullet(right_gun_x, right_gun_y, angle))

def update_bullets():
    """Update the positions of bullets and remove those that go off-screen."""
    global bullets
    updated_bullets = []
    for bullet in bullets:
        bullet.move()
        # Keep bullets that are still on the screen
        if 0 <= bullet.x <= width and 0 <= bullet.y <= height:
            updated_bullets.append(bullet)
    bullets = updated_bullets

def draw_bullets():
    """Draw all bullets."""
    for bullet in bullets:
        bullet.draw()

def mouse_click(button, state, x, y):
    """Handle mouse click to fire bullets."""
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        spawn_bullets()


class Alien:
    """Class to represent an alien entity."""
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.is_dodged = False  # Flag to check if the alien is dodged

    def move(self):
        """Move the alien."""
        if not self.is_dodged:
            # Move towards the character
            angle = math.atan2(character_y - self.y, character_x - self.x)
            self.x += self.speed * math.cos(angle)
            self.y += self.speed * math.sin(angle)
        else:
            # Move straight downward when dodged
            self.y -= self.speed

    def draw(self):
        """Draws the body of the alien with vertically holding knife"""
        glColor3f(1.6, 0.0, 1.0)  # pinkish color for the alien body
        glPointSize(2)  # smaller size for the bodies
        glBegin(GL_POINTS)

        # Main body (smaller circle-like using points)
        for i in range(360):
            theta = math.radians(i)
            dx = 10 * math.cos(theta)  # small circle radius to make the body smaller
            dy = 10 * math.sin(theta)
            glVertex2f(self.x + dx, self.y + dy)

        glEnd()

        # making antennae using points
        glColor3f(1.0, 1.0, 0.0)  # Yellow color
        glPointSize(2)
        glBegin(GL_POINTS)
        for i in range(8):  #  antennae
            # Left antenna
            glVertex2f(self.x - 3 - i, self.y + 10 + i)
            # Right antenna
            glVertex2f(self.x + 3 + i, self.y + 10 + i)
        glEnd()

        # Add eyes using points
        glColor3f(0.0, 1.0, 0.0)  #  color for eyes
        glPointSize(3.5)  #  eyes
        glBegin(GL_POINTS)
        glVertex2f(self.x - 3, self.y + 3)  # Left eye
        glVertex2f(self.x + 3, self.y + 3)  # Right eye
        glEnd()

        # Add arms holding vertical knives using points
        glColor3f(1.0, 1.0, 0.0)  # Red color for knives
        glPointSize(2)
        glBegin(GL_POINTS)

        # Left arm
        for i in range(3):  # Short arm
            glVertex2f(self.x - 10 - i, self.y - 3 + i)  # Arm
        #  knife
        for i in range(8):  # Vertical knife
            glVertex2f(self.x - 13, self.y - 5 - i)  # Knife points (straight down)

        # Right arm
        for i in range(3):  # Short arm
            glVertex2f(self.x + 10 + i, self.y - 3 + i)  #Arm
        # knife
        for i in range(8):  # Vertical knife
            glVertex2f(self.x + 13, self.y - 5 - i)  # Knife (straight down)

        glEnd()

def update_aliens():
    """Update positions of all aliens and remove those that are dodged or off-screen."""
    global aliens
    dodge_distance = 50  # Distance threshold for dodging

    updated_aliens = []
    for alien in aliens:
        # Check if the alien is close enough to be dodged
        if abs(alien.x - character_x) < dodge_distance and abs(alien.y - character_y) < dodge_distance:
            # Alien is dodged, do not add it to the updated list
            continue
        alien.move()
        # Keep aliens that are still within the screen
        if 0 <= alien.x <= width and 0 <= alien.y <= height:
            updated_aliens.append(alien)

    # Update the list of aliens
    aliens = updated_aliens

def draw_character():
    """Draws the hero with a polished design, featuring guns, arms, legs, and no cape."""
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
    gun_length = 20
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


def iterate():
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def update_character_position():
    """Update the character's position based on key states."""
    global character_x, character_y

    if keys[b'w']:
        character_y += step
    if keys[b's']:
        character_y -= step
    if keys[b'a']:
        character_x -= step
    if keys[b'd']:
        character_x += step

    # Prevent character from going out of bounds
    character_x = max(10, min(width - 10, character_x))
    character_y = max(10, min(height - 10, character_y))

def calculate_angle(x1, y1, x2, y2):
    """Calculate the angle (in degrees) between two points."""
    return math.degrees(math.atan2(y2 - y1, x2 - x1))
def spawn_alien():
    """Spawn a new alien at a random edge position."""
    edge = "top"
    if edge == "top":
        x = random.randint(0, width)
        y = height 
    speed = 0.05
    aliens.append(Alien(x, y, speed))


def showScreen():
    global character_x, character_y, mouse_x, mouse_y, frame_count

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    # Update the character's position
    update_character_position()

    # Spawn aliens periodically
    frame_count += 1
    if frame_count >= alien_spawn_interval:
        spawn_alien()
        frame_count = 0

    # Update alien positions
    update_aliens()

    # Update bullet positions
    update_bullets()

    # Calculate the rotation angle
    angle = calculate_angle(character_x, character_y, mouse_x, mouse_y)

    # Draw the character at the updated position, rotated to face the cursor
    glPushMatrix()
    glTranslatef(character_x, character_y, 0)  # Move to character position
    glRotatef(angle - 90, 0, 0, 1)  # Rotate to face the cursor (subtract 90 to align with triangle tip)
    draw_character()
    glPopMatrix()

    # Draw all bullets
    draw_bullets()

    # Draw all aliens
    for alien in aliens:
        alien.draw()

    glutSwapBuffers()

def key_down(key, x, y):
    """Handle key press events."""
    if key in keys:
        keys[key] = True

def key_up(key, x, y):
    """Handle key release events."""
    if key in keys:
        keys[key] = False

def mouse_motion(x, y):
    """Handle mouse movement to update cursor position."""
    global mouse_x, mouse_y
    # Flip the y-coordinate to match OpenGL's coordinate system
    mouse_x = x
    mouse_y = height - y

# Initialize GLUT
glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(width, height)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Alien Shooter Game")
glutDisplayFunc(showScreen)
glutIdleFunc(showScreen)  # Continuously update the screen
glutKeyboardFunc(key_down)  # Set key press callback
glutKeyboardUpFunc(key_up)  # Set key release callback
glutPassiveMotionFunc(mouse_motion)  # Track mouse movement
glutMouseFunc(mouse_click)
glutMainLoop()
