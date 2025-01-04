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
step = .20

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
    """Draw the character as a rotated triangle."""
    glColor3f(0.0, 1.0, 0.0)  # Green color for the character
    glBegin(GL_TRIANGLES)
    glVertex2f(0, 10)  # Tip of the triangle
    glVertex2f(-10, -10)
    glVertex2f(10, -10)
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
    global character_x, character_y, mouse_x, mouse_y,frame_count

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

    # Calculate the rotation angle
    angle = calculate_angle(character_x, character_y, mouse_x, mouse_y)

    # Draw the character at the updated position, rotated to face the cursor
    glPushMatrix()
    glTranslatef(character_x, character_y, 0)  # Move to character position
    glRotatef(angle - 90, 0, 0, 1)  # Rotate to face the cursor (subtract 90 to align with triangle tip)
    draw_character()
    glPopMatrix()
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

glutMainLoop()
