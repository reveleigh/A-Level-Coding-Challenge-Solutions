"""
================================================================================
  UNIT CONVERTER — Pygame Educational Version
  A-Level Computing | Pygame GUI Project
================================================================================
  Demonstrates:
    • Object-Oriented Programming (class with __init__ and methods)
    • Lambda functions stored as data (strategy pattern)
    • Event-driven programming (Pygame event loop)
    • String handling and type conversion
    • Basic GUI layout without external libraries

  Libraries used:
    pygame  — window creation, drawing, events, text rendering
    sys     — clean exit from the program

  Run:  python main.py
================================================================================
"""

# ============================================================
#  SECTION 1 — IMPORTS & PYGAME BOOTSTRAP
# ============================================================

import pygame   # Main game / GUI library
import sys      # Used for sys.exit() to close the window cleanly

pygame.init()           # Initialise ALL pygame sub-systems (display, fonts, events …)
pygame.key.set_repeat(400, 40)  # Hold-key repeats: 400 ms delay, then every 40 ms

# ============================================================
#  SECTION 2 — CONSTANTS  (colours, sizes, layout values)
# ============================================================

# --- Window dimensions ----------------------------------------------------------
WIN_W  = 860    # Total window width  (pixels)
WIN_H  = 560    # Total window height (pixels)
FPS    = 60     # Frames per second — keeps CPU usage sensible

# --- Colour palette: clean scientific / lab aesthetic ---------------------------
# Each colour is an (R, G, B) tuple; values range from 0 to 255

COL_BG          = (248, 246, 240)   # Warm white — main background
COL_PANEL_L     = (235, 230, 218)   # Warm light tan — left panel bg
COL_PANEL_R     = (255, 254, 250)   # Clean white — right panel bg
COL_ACCENT      = ( 70,  95,  70)   # Sage green — primary accent (buttons, borders)
COL_ACCENT_LT   = (110, 140, 110)   # Lighter sage — hover / border highlight
COL_TEAL        = ( 90, 115,  75)   # Moss green — selected-button highlight
COL_TEAL_LT     = (120, 150, 100)   # Lighter moss — selected button feel
COL_INK         = ( 28,  25,  20)   # Rich dark charcoal — primary text colour
COL_INK_LIGHT   = ( 95,  88,  78)   # Warm mid-brown — secondary labels
COL_INPUT_BG    = (255, 253, 248)   # Warm white — input box background
COL_INPUT_FOCUS = (245, 248, 238)   # Pale sage tint when input box is focused
COL_RESULT_BG   = (240, 245, 232)   # Very light sage tint — result box background
COL_BTN_CONV    = ( 90, 115,  75)   # Convert button face (moss green)
COL_BTN_HOVER   = ( 65,  90,  52)   # Convert button when mouse hovers over it
COL_ERROR       = (165,  45,  35)   # Deep brick red — shown when input is not valid
COL_WHITE       = (255, 255, 255)   # Pure white — used for button text

# --- Layout constants -----------------------------------------------------------
LEFT_W     = 230    # Width of the left panel (button list)
MARGIN     = 18     # General spacing margin (pixels)
BTN_H      = 52     # Height of each conversion-selector button
BTN_RADIUS = 8      # Corner radius for rounded rectangles

# --- Font sizes -----------------------------------------------------------------
FONT_TITLE  = 22    # App title
FONT_BTN    = 15    # Left-panel selector buttons
FONT_LABEL  = 14    # Unit labels (FROM / TO)
FONT_INPUT  = 26    # Large number inside input / result boxes
FONT_HINT   = 12    # Small grey hint text
FONT_CONV   = 16    # "Convert" button label

# ============================================================
#  SECTION 3 — THE Conversion CLASS
# ============================================================

class Conversion:
    """
    Represents one type of unit conversion.

    Attributes
    ----------
    label     : str      — human-readable name shown in the left panel
    from_unit : str      — name of the source unit  (e.g. "Grams")
    to_unit   : str      — name of the target unit  (e.g. "Kilograms")
    factor_fn : callable — a lambda (or function) that takes a float value
                           and returns the converted float value

    Class attribute
    ---------------
    registry  : list[Conversion]  — all available conversions (built below)
    """

    registry = []   # Class-level list — shared across ALL instances

    def __init__(self, label, from_unit, to_unit, factor_fn):
        """
        Initialise a new Conversion object and add it to the class registry.

        Parameters
        ----------
        label     : str      — display name for the conversion pair
        from_unit : str      — name of the input unit
        to_unit   : str      — name of the output unit
        factor_fn : callable — lambda / function that performs the maths
        """
        self.label     = label       # Store the display label
        self.from_unit = from_unit   # Store the source unit name
        self.to_unit   = to_unit     # Store the target unit name
        self.factor_fn = factor_fn   # Store the conversion function

        # Automatically register this instance in the class-level list
        Conversion.registry.append(self)

    def convert(self, value):
        """
        Apply the conversion formula to a numeric value.

        Parameters
        ----------
        value : float — the number to convert (in from_unit)

        Returns
        -------
        float — the converted result (in to_unit)
        """
        return float(self.factor_fn(value))  # Apply lambda and ensure float


# ============================================================
#  SECTION 4 — REGISTERING ALL CONVERSIONS
#  (Creating Conversion objects populates Conversion.registry)
# ============================================================

# --- Mass -------------------------------------------------------------------
Conversion(
    label     = "Grams to Kilograms",
    from_unit = "Grams",
    to_unit   = "Kilograms",
    factor_fn = lambda v: v / 1000          # 1 kg = 1000 g  ->  divide by 1000
)

Conversion(
    label     = "Kilograms to Grams",
    from_unit = "Kilograms",
    to_unit   = "Grams",
    factor_fn = lambda v: v * 1000          # Reverse: multiply by 1000
)

# --- Currency: USD / EUR ----------------------------------------------------
Conversion(
    label     = "USD to Euro",
    from_unit = "US Dollars",
    to_unit   = "Euros",
    factor_fn = lambda v: v * 0.85          # Approximate exchange rate
)

Conversion(
    label     = "Euro to USD",
    from_unit = "Euros",
    to_unit   = "US Dollars",
    factor_fn = lambda v: v / 0.85          # Reverse: divide by 0.85
)

# --- Temperature ------------------------------------------------------------
Conversion(
    label     = "Celsius to Fahrenheit",
    from_unit = "Celsius",
    to_unit   = "Fahrenheit",
    factor_fn = lambda v: (v * 9 / 5) + 32  # Standard C -> F formula
)

Conversion(
    label     = "Fahrenheit to Celsius",
    from_unit = "Fahrenheit",
    to_unit   = "Celsius",
    factor_fn = lambda v: (v - 32) * 5 / 9  # Reverse: subtract 32 first
)

# --- Volume -----------------------------------------------------------------
Conversion(
    label     = "Litres to Gallons",
    from_unit = "Litres",
    to_unit   = "Gallons (US)",
    factor_fn = lambda v: v * 0.264172       # 1 litre = 0.264172 US gallons
)

Conversion(
    label     = "Gallons to Litres",
    from_unit = "Gallons (US)",
    to_unit   = "Litres",
    factor_fn = lambda v: v * 3.78541        # 1 US gallon = 3.78541 litres
)

# --- Currency: USD / GBP ----------------------------------------------------
Conversion(
    label     = "USD to GBP",
    from_unit = "US Dollars",
    to_unit   = "Pounds Sterling",
    factor_fn = lambda v: v * 0.72           # Approximate exchange rate
)

Conversion(
    label     = "GBP to USD",
    from_unit = "Pounds Sterling",
    to_unit   = "US Dollars",
    factor_fn = lambda v: v / 0.72           # Reverse: divide by 0.72
)

# ============================================================
#  SECTION 5 — DISPLAY & FONT SETUP
# ============================================================

screen = pygame.display.set_mode((WIN_W, WIN_H))        # Create the window surface
pygame.display.set_caption("Unit Converter — A-Level Pygame")  # Window title bar

clock = pygame.time.Clock()     # Clock object used to cap the frame rate

# Create font objects — SysFont looks for an installed font; falls back to default
# Second argument is the size in points; third (bold) is True/False
font_title  = pygame.font.SysFont("Segoe UI", FONT_TITLE,  bold=True)
font_btn    = pygame.font.SysFont("Segoe UI", FONT_BTN,    bold=False)
font_label  = pygame.font.SysFont("Segoe UI", FONT_LABEL,  bold=True)
font_input  = pygame.font.SysFont("Segoe UI Semibold", FONT_INPUT, bold=False)
font_hint   = pygame.font.SysFont("Segoe UI", FONT_HINT,  bold=False)
font_conv   = pygame.font.SysFont("Segoe UI", FONT_CONV,   bold=True)

# ============================================================
#  SECTION 6 — HELPER DRAWING FUNCTIONS
# ============================================================

def draw_rounded_rect(surface, colour, rect, radius):
    """
    Draw a filled rectangle with rounded corners.

    Parameters
    ----------
    surface : pygame.Surface — the surface to draw onto
    colour  : tuple(R,G,B)   — fill colour
    rect    : pygame.Rect    — position and size
    radius  : int            — corner radius in pixels
    """
    pygame.draw.rect(surface, colour, rect, border_radius=radius)


def draw_text_centered(surface, text, font, colour, rect):
    """
    Render text centred both horizontally and vertically inside a rect.

    Parameters
    ----------
    surface : pygame.Surface
    text    : str
    font    : pygame.font.Font
    colour  : tuple(R,G,B)
    rect    : pygame.Rect — the bounding box to centre within
    """
    rendered = font.render(text, True, colour)      # Render to a surface (anti-aliased)
    x = rect.x + (rect.width  - rendered.get_width())  // 2   # Centre horizontally
    y = rect.y + (rect.height - rendered.get_height()) // 2   # Centre vertically
    surface.blit(rendered, (x, y))                 # Draw onto the target surface


def draw_text_left(surface, text, font, colour, x, y):
    """
    Render text left-aligned at position (x, y).

    Parameters
    ----------
    surface : pygame.Surface
    text    : str
    font    : pygame.font.Font
    colour  : tuple(R,G,B)
    x, y    : int — top-left pixel position
    """
    rendered = font.render(text, True, colour)
    surface.blit(rendered, (x, y))


# ============================================================
#  SECTION 7 — APPLICATION STATE  (variables that change at runtime)
# ============================================================

selected_idx   = 0          # Index of the currently selected conversion in registry
input_text     = ""         # String typed by the user into the input field
result_text    = ""         # Formatted result string to display
error_msg      = ""         # Error message (empty = no error)
input_focused  = True       # Whether the input box has keyboard focus
cursor_visible = True       # Used to blink the text cursor
cursor_timer   = 0          # Millisecond accumulator for cursor blink timing

# Pre-compute button rects for the left panel (built once, reused each frame)
# Each rect covers the full width of the left panel at its vertical position
BUTTON_RECTS = []
for i in range(len(Conversion.registry)):
    # Stack buttons vertically with MARGIN gap at top, BTN_H height each
    r = pygame.Rect(
        MARGIN,                             # Left edge (with small indent)
        80 + i * (BTN_H + 6),              # Top edge: 80 px header offset + stacking
        LEFT_W - MARGIN * 2,               # Width fits inside the left panel
        BTN_H                               # Fixed button height
    )
    BUTTON_RECTS.append(r)

# Right panel layout — positions for the UI widgets on the right side
RIGHT_X     = LEFT_W + MARGIN * 2           # Left edge of right panel content
RIGHT_W     = WIN_W - RIGHT_X - MARGIN * 2  # Available width in right panel

INPUT_RECT  = pygame.Rect(RIGHT_X, 190, RIGHT_W, 60)   # Input text box
RESULT_RECT = pygame.Rect(RIGHT_X, 320, RIGHT_W, 60)   # Result display box

# Convert button sits below the result box, centred horizontally in right panel
CONV_BTN_W  = 160
CONV_BTN_H  = 44
CONV_BTN_X  = RIGHT_X + (RIGHT_W - CONV_BTN_W) // 2   # Centre it
CONV_BTN_Y  = 410
CONV_BTN_RECT = pygame.Rect(CONV_BTN_X, CONV_BTN_Y, CONV_BTN_W, CONV_BTN_H)

# ============================================================
#  SECTION 8 — CONVERSION TRIGGER FUNCTION
# ============================================================

def do_convert():
    """
    Read input_text, attempt to convert it using the selected Conversion,
    and update result_text / error_msg accordingly.
    Uses global variables (standard in simple pygame apps like this).
    """
    global result_text, error_msg   # We need to write to these module-level variables

    if not input_text.strip():       # Guard: nothing typed yet
        error_msg   = "Please type a number first."
        result_text = ""
        return

    try:
        value = float(input_text)    # Try to parse the input as a decimal number
    except ValueError:
        # The string could not be converted — tell the user
        error_msg   = f'"{input_text}" is not a valid number.'
        result_text = ""
        return

    # Retrieve the currently selected Conversion object from the registry
    conv = Conversion.registry[selected_idx]

    # Call the convert() method — this applies the lambda inside factor_fn
    raw_result = conv.convert(value)

    # Format: up to 6 decimal places, strip trailing zeros
    result_text = f"{raw_result:.6f}".rstrip("0").rstrip(".")

    error_msg = ""   # Clear any previous error since this conversion succeeded


# ============================================================
#  SECTION 9 — MAIN LOOP
# ============================================================

running = True   # Loop sentinel — set to False to quit

while running:

    dt = clock.tick(FPS)   # dt = milliseconds since last frame; also caps to FPS

    # --------------------------------------------------------
    #  9a  EVENT HANDLING
    # --------------------------------------------------------

    for event in pygame.event.get():

        # --- Quit events --------------------------------------------------------
        if event.type == pygame.QUIT:           # User clicked the window X button
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:    # Escape key also quits
                running = False

            # --- Input box keyboard handling ------------------------------------
            if input_focused:

                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    do_convert()               # Enter key triggers conversion

                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]   # Remove the last character
                    result_text = ""               # Clear stale result
                    error_msg   = ""

                else:
                    char = event.unicode           # The printable character pressed
                    # Only allow digits, one decimal point, and a leading minus sign
                    if char in "0123456789":
                        input_text += char
                        result_text = ""
                        error_msg   = ""
                    elif char == "." and "." not in input_text:
                        input_text += char         # Allow only one decimal point
                        result_text = ""
                        error_msg   = ""
                    elif char == "-" and input_text == "":
                        input_text += char         # Allow minus only at the start
                        result_text = ""
                        error_msg   = ""

        # --- Mouse click handling -----------------------------------------------
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            mx, my = event.pos   # Pixel coordinates of the click

            # Check if a conversion selector button was clicked
            for i, btn_rect in enumerate(BUTTON_RECTS):
                if btn_rect.collidepoint(mx, my):
                    selected_idx = i     # Switch to clicked conversion
                    input_text   = ""    # Reset input when switching type
                    result_text  = ""
                    error_msg    = ""
                    input_focused = True

            # Check if the input box was clicked -> give it focus
            if INPUT_RECT.collidepoint(mx, my):
                input_focused = True

            # Check if the Convert button was clicked
            if CONV_BTN_RECT.collidepoint(mx, my):
                do_convert()

    # --------------------------------------------------------
    #  9b  CURSOR BLINK LOGIC
    # --------------------------------------------------------
    cursor_timer += dt                     # Accumulate elapsed time
    if cursor_timer >= 530:                # Toggle every 530 ms = standard blink
        cursor_visible = not cursor_visible
        cursor_timer   = 0

    # --------------------------------------------------------
    #  9c  DRAW — clear then rebuild the entire frame
    # --------------------------------------------------------

    screen.fill(COL_BG)   # Fill the whole window with the background colour

    # === LEFT PANEL BACKGROUND ===================================================
    left_panel = pygame.Rect(0, 0, LEFT_W, WIN_H)
    draw_rounded_rect(screen, COL_PANEL_L, left_panel, 0)  # Flat left edge -> radius 0

    # Panel title
    draw_text_left(screen, "Conversions", font_title, COL_ACCENT, MARGIN, MARGIN)
    draw_text_left(screen, "Select a type below:", font_hint, COL_INK_LIGHT,
                   MARGIN, MARGIN + 28)

    # --- Draw each conversion selector button -----------------------------------
    for i, conv in enumerate(Conversion.registry):
        rect     = BUTTON_RECTS[i]           # Pre-computed rect for this button
        selected = (i == selected_idx)        # Is this the currently chosen one?

        # Choose colours based on selected state
        bg_col   = COL_TEAL   if selected else COL_ACCENT
        text_col = COL_WHITE

        # Draw the button background
        draw_rounded_rect(screen, bg_col, rect, BTN_RADIUS)

        # Draw a subtle lighter border on top edge for a "raised" feel
        border_col = COL_TEAL_LT if selected else COL_ACCENT_LT
        pygame.draw.rect(screen, border_col, rect, 2, border_radius=BTN_RADIUS)

        # Draw the conversion label, centred in the button
        draw_text_centered(screen, conv.label, font_btn, text_col, rect)

    # === RIGHT PANEL BACKGROUND ==================================================
    right_panel = pygame.Rect(LEFT_W, 0, WIN_W - LEFT_W, WIN_H)
    draw_rounded_rect(screen, COL_PANEL_R, right_panel, 0)

    # Thin vertical divider line between panels
    pygame.draw.line(screen, COL_ACCENT_LT, (LEFT_W, 0), (LEFT_W, WIN_H), 2)

    # --- Right panel header -----------------------------------------------------
    active_conv = Conversion.registry[selected_idx]   # Currently selected conversion

    draw_text_left(screen, "Unit Converter", font_title, COL_ACCENT, RIGHT_X, MARGIN)
    draw_text_left(screen,
                   active_conv.from_unit + "  ->  " + active_conv.to_unit,
                   font_label, COL_INK_LIGHT, RIGHT_X, MARGIN + 30)

    # Horizontal separator under the header
    pygame.draw.line(screen, COL_ACCENT_LT,
                     (RIGHT_X, 70), (WIN_W - MARGIN, 70), 1)

    # --- FROM label & input box -------------------------------------------------
    draw_text_left(screen, "Enter value in " + active_conv.from_unit + ":",
                   font_label, COL_INK, RIGHT_X, 140)

    # Choose input box colour based on focus
    input_bg = COL_INPUT_FOCUS if input_focused else COL_INPUT_BG
    draw_rounded_rect(screen, input_bg, INPUT_RECT, BTN_RADIUS)
    pygame.draw.rect(screen, COL_ACCENT, INPUT_RECT, 2, border_radius=BTN_RADIUS)

    # Build the display string: add blinking cursor when focused
    display_str = input_text
    if input_focused and cursor_visible:
        display_str += "|"   # Simple text cursor character

    # Draw the typed text inside the input box, vertically centred
    if display_str:
        text_surf = font_input.render(display_str, True, COL_INK)
        # Clip long text to stay inside the box
        max_w = INPUT_RECT.width - 16   # 8 px padding each side
        if text_surf.get_width() > max_w:
            # Blit from the right edge of the text surface so latest chars show
            screen.blit(text_surf,
                        (INPUT_RECT.x + 8, INPUT_RECT.y + 14),
                        area=pygame.Rect(text_surf.get_width() - max_w, 0,
                                         max_w, text_surf.get_height()))
        else:
            screen.blit(text_surf, (INPUT_RECT.x + 8, INPUT_RECT.y + 14))
    else:
        # Show placeholder hint text when input is empty
        draw_text_left(screen, "Type a number...", font_hint, COL_INK_LIGHT,
                       INPUT_RECT.x + 10, INPUT_RECT.y + 22)

    # --- RESULT area ------------------------------------------------------------
    draw_text_left(screen, "Result in " + active_conv.to_unit + ":",
                   font_label, COL_INK, RIGHT_X, 290)

    draw_rounded_rect(screen, COL_RESULT_BG, RESULT_RECT, BTN_RADIUS)
    pygame.draw.rect(screen, COL_TEAL, RESULT_RECT, 2, border_radius=BTN_RADIUS)

    if error_msg:
        # Show error in red inside the result box
        draw_text_centered(screen, error_msg, font_hint, COL_ERROR, RESULT_RECT)
    elif result_text:
        # Show the conversion result in large ink-coloured text
        text_surf = font_input.render(result_text, True, COL_INK)
        # Shrink to fit if the number is very long
        if text_surf.get_width() > RESULT_RECT.width - 16:
            small_font = pygame.font.SysFont("Segoe UI", 18)
            text_surf  = small_font.render(result_text, True, COL_INK)
        rx = RESULT_RECT.x + (RESULT_RECT.width  - text_surf.get_width())  // 2
        ry = RESULT_RECT.y + (RESULT_RECT.height - text_surf.get_height()) // 2
        screen.blit(text_surf, (rx, ry))
    else:
        # Placeholder when no conversion has been run yet
        draw_text_centered(screen, "Result will appear here",
                           font_hint, COL_INK_LIGHT, RESULT_RECT)

    # --- CONVERT BUTTON ---------------------------------------------------------
    mouse_pos   = pygame.mouse.get_pos()
    btn_hovered = CONV_BTN_RECT.collidepoint(mouse_pos)  # Is mouse over the button?
    btn_col     = COL_BTN_HOVER if btn_hovered else COL_BTN_CONV

    draw_rounded_rect(screen, btn_col, CONV_BTN_RECT, BTN_RADIUS)
    draw_text_centered(screen, "Convert  >", font_conv, COL_WHITE, CONV_BTN_RECT)

    # --- Footer hint ------------------------------------------------------------
    draw_text_left(screen,
                   "Tip: press  Enter  to convert   |   Escape to quit",
                   font_hint, COL_INK_LIGHT,
                   RIGHT_X, WIN_H - 24)

    # --------------------------------------------------------
    #  9d  FLIP — push the completed frame to the screen
    # --------------------------------------------------------
    pygame.display.flip()   # Show everything drawn (double-buffered swap)

# ============================================================
#  SECTION 10 — CLEAN SHUTDOWN
# ============================================================

pygame.quit()   # Shut down all pygame sub-systems gracefully
sys.exit()      # Exit the Python interpreter
