# ============================================================
#  Factorial Finder – Pygame Edition
#  A minimal Pygame application that teaches:
#    1. How to set up a Pygame window (the "bootstrap")
#    2. How to create and use a CLASS in Python
#    3. How to draw simple GUI elements (text, boxes)
#    4. How to handle keyboard input from the user
# ============================================================

# --- Step 1: Import the libraries we need ---
import pygame   # The main library that lets us open windows and draw things
import sys      # Lets us exit the program cleanly

# --- Step 2: Initialise Pygame ---
# pygame.init() MUST be called before you use anything else in pygame.
# It starts up all the internal systems (display, sound, input, etc.)
pygame.init()

# ============================================================
#  CLASS DEFINITION
#  A class is like a blueprint for an object.
#  Here we define a 'Factorial' class that knows:
#    - what number to work with  (the DATA  → "attributes")
#    - how to calculate the factorial (the BEHAVIOUR → "method")
# ============================================================
class Factorial:
    """
    Represents a factorial calculation.

    Attributes
    ----------
    number : int
        The non-negative integer whose factorial we want.
    result : int
        The computed factorial value (set after calling .calculate()).
    """

    # ----------------------------------------------------------
    # __init__ is the CONSTRUCTOR – it runs automatically when
    # you do:  my_obj = Factorial(5)
    # 'self' always refers to *this specific object*.
    # ----------------------------------------------------------
    def __init__(self, number):
        self.number = number    # Store the number on the object
        self.result = None      # We haven't calculated yet, so result is None

    # ----------------------------------------------------------
    # A METHOD is just a function that belongs to a class.
    # Call it with:  my_obj.calculate()
    # ----------------------------------------------------------
    def calculate(self):
        """Calculate the factorial using a loop and store it in self.result."""

        # Edge case: factorial of 0 is defined as 1
        if self.number == 0:
            self.result = 1
            return

        # Start with 1 and multiply up to (and including) self.number
        self.result = 1
        for i in range(1, self.number + 1):
            self.result *= i   # Same as: self.result = self.result * i

    def get_result_string(self):
        """Return a nicely formatted string for displaying on screen."""
        if self.result is None:
            return ""   # Nothing to show yet
        return f"{self.number}! = {self.result}"


# ============================================================
#  CONSTANTS  (values that never change – written in UPPER_CASE
#  by convention so they are easy to spot)
# ============================================================
WINDOW_WIDTH  = 600     # How wide the window is in pixels
WINDOW_HEIGHT = 400     # How tall the window is in pixels
FPS           = 60      # Frames per second – how often we redraw the screen

# --- Colours (Pygame uses RGB tuples: Red, Green, Blue  0-255) ---
COLOUR_BG         = (20,  20,  40)   # Dark navy background
COLOUR_TITLE      = (180, 140, 255)  # Soft purple for the title
COLOUR_LABEL      = (200, 200, 220)  # Light grey for labels
COLOUR_BOX_NORMAL = (50,  50,  80)   # Input box colour (inactive)
COLOUR_BOX_ACTIVE = (80,  80, 140)   # Input box colour (when the user is typing)
COLOUR_BOX_BORDER = (120, 100, 200)  # Border of the input box
COLOUR_RESULT     = (100, 255, 180)  # Bright green for the answer
COLOUR_ERROR      = (255, 100, 100)  # Red for error messages
COLOUR_WHITE      = (255, 255, 255)

# --- Step 3: Create the window ---
# set_mode() returns a "Surface" – think of it as the canvas we draw on.
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Give the window a title that appears in the title bar
pygame.display.set_caption("Factorial Finder – Pygame Edition")

# --- Step 4: Create a Clock object ---
# The clock controls how fast our loop runs so it doesn't go faster than FPS.
clock = pygame.time.Clock()

# --- Step 5: Load fonts ---
# pygame.font.SysFont() picks a font installed on the computer.
# The second argument is the size in points.
font_title  = pygame.font.SysFont("segoeui", 42, bold=True)
font_label  = pygame.font.SysFont("segoeui", 24)
font_input  = pygame.font.SysFont("consolas", 32, bold=True)   # Monospace for the input
font_result = pygame.font.SysFont("segoeui", 28, bold=True)

# ============================================================
#  GAME / APP STATE
#  These variables keep track of what the user has typed and
#  what result (if any) we should display.
# ============================================================
user_text    = ""      # The string the user is currently typing
result_text  = ""      # The answer we'll show (e.g. "5! = 120")
error_text   = ""      # An error message if the input is invalid
box_active   = True    # Whether the input box has "focus" (is selected)

# Define the rectangle for our input box (x, y, width, height)
input_box = pygame.Rect(150, 220, 300, 50)

# ============================================================
#  HELPER FUNCTION
#  A plain function (outside the class) that wires the GUI
#  to the Factorial class.
# ============================================================
def compute_factorial(text):
    """
    Try to create a Factorial object from the user's text,
    calculate the result, and return (result_string, error_string).
    """
    # Try to convert the text to an integer
    try:
        n = int(text)
    except ValueError:
        # If conversion fails (e.g. the user typed "abc"), return an error
        return "", "Please enter a whole number!"

    if n < 0:
        return "", "Factorial is not defined for negative numbers."

    if n > 20:
        return "", "Try a number ≤ 20 to keep things readable!"

    # --- Using the CLASS ---
    # 1. Create an INSTANCE (object) of the Factorial class
    fact_obj = Factorial(n)

    # 2. Call the calculate METHOD on that object
    fact_obj.calculate()

    # 3. Ask the object for its formatted result string
    answer = fact_obj.get_result_string()

    return answer, ""   # Return the answer and an empty error string


# ============================================================
#  MAIN LOOP  (the heart of every Pygame program)
#
#  Every frame, we:
#    1. Process EVENTS  (key presses, mouse clicks, window close)
#    2. UPDATE  state   (change variables based on events)
#    3. DRAW    screen  (paint everything onto the canvas)
# ============================================================
running = True   # As long as this is True, the loop keeps going

while running:

    # ----------------------------------------------------------
    # 1. EVENT LOOP
    #    pygame.event.get() returns a list of things that happened
    #    since the last frame (key presses, mouse clicks, etc.)
    # ----------------------------------------------------------
    for event in pygame.event.get():

        # The user clicked the red ✕ to close the window
        if event.type == pygame.QUIT:
            running = False   # Exit the main loop

        # The user pressed a key on the keyboard
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:
                # ENTER pressed → compute the factorial
                result_text, error_text = compute_factorial(user_text)

            elif event.key == pygame.K_BACKSPACE:
                # BACKSPACE → remove the last character from user_text
                user_text = user_text[:-1]
                # Clear the result when the user starts editing again
                result_text = ""
                error_text  = ""

            else:
                # Any other key: add the character to user_text
                # event.unicode gives us the actual character typed
                # We only allow digits (0-9) to keep input clean
                if event.unicode.isdigit():
                    user_text += event.unicode
                    result_text = ""
                    error_text  = ""

    # ----------------------------------------------------------
    # 2. DRAW PHASE
    #    Fill the background first, then draw everything on top.
    # ----------------------------------------------------------

    # Fill the entire screen with the background colour
    screen.fill(COLOUR_BG)

    # --- Title ---
    title_surf = font_title.render("Factorial Finder", True, COLOUR_TITLE)
    # 'render' creates an image (Surface) of the text.
    # True = anti-aliased (smooth edges).
    # We centre it horizontally:
    title_x = (WINDOW_WIDTH - title_surf.get_width()) // 2
    screen.blit(title_surf, (title_x, 40))
    # 'blit' copies one surface onto another at a given position.

    # --- Subtitle / instruction ---
    sub_surf = font_label.render("Enter a number and press Enter", True, COLOUR_LABEL)
    sub_x = (WINDOW_WIDTH - sub_surf.get_width()) // 2
    screen.blit(sub_surf, (sub_x, 100))

    # --- Label above the input box ---
    label_surf = font_label.render("Number:", True, COLOUR_LABEL)
    screen.blit(label_surf, (input_box.x, input_box.y - 34))

    # --- Input box background ---
    box_colour = COLOUR_BOX_ACTIVE if box_active else COLOUR_BOX_NORMAL
    pygame.draw.rect(screen, box_colour, input_box, border_radius=8)
    # Draw a border (outline) around the box – the last argument is the thickness
    pygame.draw.rect(screen, COLOUR_BOX_BORDER, input_box, width=2, border_radius=8)

    # --- Text inside the input box ---
    input_surf = font_input.render(user_text, True, COLOUR_WHITE)
    # Vertically centre the text inside the box
    text_y = input_box.y + (input_box.height - input_surf.get_height()) // 2
    screen.blit(input_surf, (input_box.x + 12, text_y))

    # --- Blinking cursor (just a simple pipe character "|") ---
    # pygame.time.get_ticks() returns milliseconds since pygame.init()
    # We use it to make the cursor blink every 500 ms
    if box_active and (pygame.time.get_ticks() // 500) % 2 == 0:
        cursor_x = input_box.x + 12 + input_surf.get_width() + 2
        cursor_surf = font_input.render("|", True, COLOUR_BOX_BORDER)
        screen.blit(cursor_surf, (cursor_x, text_y))

    # --- Result ---
    if result_text:
        result_surf = font_result.render(result_text, True, COLOUR_RESULT)
        result_x = (WINDOW_WIDTH - result_surf.get_width()) // 2
        screen.blit(result_surf, (result_x, 320))

    # --- Error message ---
    if error_text:
        error_surf = font_label.render(error_text, True, COLOUR_ERROR)
        error_x = (WINDOW_WIDTH - error_surf.get_width()) // 2
        screen.blit(error_surf, (error_x, 320))

    # --- Footer hint ---
    hint_surf = font_label.render("Backspace to clear  |  Enter to calculate", True, (80, 80, 110))
    hint_x = (WINDOW_WIDTH - hint_surf.get_width()) // 2
    screen.blit(hint_surf, (hint_x, 370))

    # ----------------------------------------------------------
    # 3. UPDATE THE DISPLAY
    #    Everything we've drawn so far is in a hidden back-buffer.
    #    flip() swaps it to the screen all at once (no flickering).
    # ----------------------------------------------------------
    pygame.display.flip()

    # Pause until it's time for the next frame (keeps us at FPS)
    clock.tick(FPS)

# ============================================================
#  CLEAN UP
#  When the loop ends (running = False), we tidy up and exit.
# ============================================================
pygame.quit()   # Shut down all Pygame systems
sys.exit()      # Exit the Python script cleanly
