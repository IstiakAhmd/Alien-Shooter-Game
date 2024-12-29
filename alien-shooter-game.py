from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Window dimensions
width = 800
height = 600

# Character position
character_x = width // 2
character_y = height // 2

# Movement step size
step = 0.25

# Mouse position
mouse_x = width // 2
mouse_y = height // 2

# Key state dictionary
keys = {b'w': False, b'a': False, b's': False, b'd': False}

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

def showScreen():
    global character_x, character_y, mouse_x, mouse_y

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    # Update the character's position
    update_character_position()

    # Calculate the rotation angle
    angle = calculate_angle(character_x, character_y, mouse_x, mouse_y)

    # Draw the character at the updated position, rotated to face the cursor
    glPushMatrix()
    glTranslatef(character_x, character_y, 0)  # Move to character position
    glRotatef(angle - 90, 0, 0, 1)  # Rotate to face the cursor (subtract 90 to align with triangle tip)
    draw_character()
    glPopMatrix()

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
