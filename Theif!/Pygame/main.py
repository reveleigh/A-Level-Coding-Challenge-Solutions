# ============================================================
#  Theif! – Pygame Edition
#  Given four unique digits, crack every possible 4-digit PIN.
#
#  This file teaches:
#    1. The Pygame bootstrap (window, clock, main loop)
#    2. Classes and objects (PinCracker)
#    3. Scrollable output – more advanced GUI element
#    4. Iterating through nested loops inside a class method
#
#  Colour palette: parchment, ink, aged paper – warm & organic.
# ============================================================

import pygame
import sys

# --- Initialise Pygame (always the very first call) ---
pygame.init()

# ============================================================
#  CLASS DEFINITION  –  PinCracker
#
#  This class bundles together:
#    • the four digits the user provides  (DATA / attributes)
#    • the logic to find all combinations (BEHAVIOUR / methods)
#
#  Think of the class as a blueprint.  When we write:
#      cracker = PinCracker(["1","2","3","4"])
#  we create one *object* (instance) from that blueprint.
# ============================================================
class PinCracker:
    """
    Generates every unique 4-digit permutation of 4 given digits.

    Attributes
    ----------
    digits       : list[str]  – the four digits to permute
    combinations : list[str]  – all valid unique PINs (populated by .crack())
    """

    def __init__(self, digits):
        # Store the digits on the object so every method can access them
        self.digits = digits

        # Start with an empty list – crack() will fill it
        self.combinations = []

    def crack(self):
        """
        Fill self.combinations using four nested loops.
        Each loop picks one digit for one position in the PIN.
        We only keep combinations where all four digits are different.
        """
        # Reset in case crack() is called more than once
        self.combinations = []

        # Four nested loops – one per digit position in the PIN
        for d1 in self.digits:
            for d2 in self.digits:
                for d3 in self.digits:
                    for d4 in self.digits:
                        # All four positions must hold a different digit
                        if d1 != d2 and d1 != d3 and d1 != d4 \
                           and d2 != d3 and d2 != d4 \
                           and d3 != d4:
                            # Build the PIN string and add it to the list
                            self.combinations.append(f"{d1}{d2}{d3}{d4}")

    def get_summary(self):
        """Return a short summary string, e.g. '24 combinations found'."""
        n = len(self.combinations)
        if n == 0:
            return "No combinations yet – enter digits and press Enter."
        return f"{n} unique PINs found"


# ============================================================
#  CONSTANTS
# ============================================================
WINDOW_WIDTH  = 640
WINDOW_HEIGHT = 520
FPS           = 60

# --- Parchment / organic colour palette ---
# Think aged paper, sepia ink, warm earth tones.
COLOUR_BG          = (210, 195, 165)   # Warm parchment
COLOUR_PANEL       = (228, 215, 185)   # Lighter panel / card area
COLOUR_INK         = ( 55,  40,  20)   # Dark sepia ink (main text)
COLOUR_INK_LIGHT   = ( 95,  75,  45)   # Lighter ink (labels, hints)
COLOUR_BORDER      = (150, 120,  70)   # Aged brown border
COLOUR_BOX_IDLE    = (240, 230, 205)   # Input box background (idle)
COLOUR_BOX_ACTIVE  = (248, 240, 220)   # Input box background (focused)
COLOUR_ACCENT      = (140,  80,  30)   # Rust-orange accent (titles, results)
COLOUR_SCROLL_BG   = (195, 180, 150)   # Scroll list background
COLOUR_SCROLL_ROW  = (205, 190, 160)   # Alternating row tint
COLOUR_ERROR       = (160,  50,  30)   # Deep red for errors
COLOUR_SCROLLBAR   = (160, 130,  80)   # Scrollbar track colour

# ============================================================
#  WINDOW & CLOCK
# ============================================================
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Theif!  –  PIN Cracker (Pygame Edition)")
clock = pygame.time.Clock()

# ============================================================
#  FONTS
# ============================================================
font_title   = pygame.font.SysFont("georgia",    38, bold=True)
font_label   = pygame.font.SysFont("georgia",    20)
font_input   = pygame.font.SysFont("couriernew", 30, bold=True)
font_result  = pygame.font.SysFont("georgia",    18)
font_summary = pygame.font.SysFont("georgia",    20, bold=True)

# ============================================================
#  LAYOUT RECTANGLES
#  Defining all positions up-front keeps the draw code clean.
# ============================================================
INPUT_BOX   = pygame.Rect(200, 160, 240,  46)   # Where the user types
LIST_AREA   = pygame.Rect( 40, 270, 480, 210)   # Scrollable results panel
SCROLLBAR_X = LIST_AREA.right + 6                # X position of scrollbar
SCROLLBAR_W = 12                                 # Width of scrollbar
ROW_HEIGHT  = 26                                 # Pixel height per result row
COLS        = 6                                  # Combinations shown per row

# ============================================================
#  APP STATE
# ============================================================
user_text    = ""    # Characters the user has typed so far
error_text   = ""    # Validation error (shown in red)
combinations = []    # List of PIN strings from PinCracker
summary_text = "Enter four unique digits, then press Enter."
scroll_offset = 0   # How many rows the list has been scrolled down


# ============================================================
#  HELPER – validate and crack
# ============================================================
def run_cracker(text):
    """
    Validate user input, create a PinCracker object, call .crack(),
    and return (combinations_list, summary_string, error_string).
    """
    # Must be exactly 4 characters
    if len(text) != 4:
        return [], "", "Please enter exactly 4 digits."

    # Every character must be a digit
    if not text.isdigit():
        return [], "", "Only numerical digits (0-9) are allowed."

    # All four digits must be different
    if len(set(text)) != 4:
        return [], "", "All four digits must be unique."

    # --- Using the CLASS ---
    digits = list(text)                  # e.g. ['1','2','3','4']
    cracker = PinCracker(digits)         # Create an INSTANCE of PinCracker
    cracker.crack()                      # Call the crack() METHOD
    return cracker.combinations, cracker.get_summary(), ""


# ============================================================
#  DRAW HELPERS
# ============================================================
def draw_panel(surface, rect, radius=10):
    """Draw a rounded-rectangle panel with a border."""
    pygame.draw.rect(surface, COLOUR_PANEL,  rect, border_radius=radius)
    pygame.draw.rect(surface, COLOUR_BORDER, rect, width=2, border_radius=radius)


def draw_text_centred(surface, text, font, colour, y):
    """Render text centred horizontally on the screen."""
    surf = font.render(text, True, colour)
    x = (WINDOW_WIDTH - surf.get_width()) // 2
    surface.blit(surf, (x, y))


def draw_scrollable_list(surface, items, area, row_h, cols, scroll_y):
    """
    Draw 'items' as a grid inside 'area', scrolled by 'scroll_y' rows.
    Returns the scrollbar thumb rect for hit-testing.
    """
    # Clip drawing to the list area so text doesn't spill out
    old_clip = surface.get_clip()
    surface.set_clip(area)

    # Background
    pygame.draw.rect(surface, COLOUR_SCROLL_BG, area, border_radius=6)

    col_width = area.width // cols
    visible_rows = area.height // row_h

    for idx, pin in enumerate(items):
        row = idx // cols          # Which row this item belongs to
        col = idx %  cols          # Which column
        draw_row = row - scroll_y  # Adjust for scroll

        # Only draw rows that are visible
        if 0 <= draw_row < visible_rows:
            x = area.x + col * col_width + 6
            y = area.y + draw_row * row_h + 4

            # Alternate row tint for readability
            if row % 2 == 0:
                cell = pygame.Rect(area.x, area.y + draw_row * row_h,
                                   area.width, row_h)
                pygame.draw.rect(surface, COLOUR_SCROLL_ROW, cell)

            pin_surf = font_result.render(pin, True, COLOUR_INK)
            surface.blit(pin_surf, (x, y))

    surface.set_clip(old_clip)

    # --- Scrollbar ---
    total_rows = (len(items) + cols - 1) // cols   # Total rows needed
    if total_rows <= visible_rows:
        return None   # No scrollbar needed

    bar_area = pygame.Rect(SCROLLBAR_X, area.y, SCROLLBAR_W, area.height)
    pygame.draw.rect(surface, COLOUR_BORDER, bar_area, border_radius=4)

    # Thumb size proportional to visible fraction
    thumb_h = max(20, area.height * visible_rows // total_rows)
    thumb_y = area.y + (area.height - thumb_h) * scroll_y // max(1, total_rows - visible_rows)
    thumb = pygame.Rect(SCROLLBAR_X, thumb_y, SCROLLBAR_W, thumb_h)
    pygame.draw.rect(surface, COLOUR_SCROLLBAR, thumb, border_radius=4)
    return thumb


# ============================================================
#  MAIN LOOP
# ============================================================
running = True

while running:

    # ----------------------------------------------------------
    # 1. EVENTS
    # ----------------------------------------------------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Run the cracker when the user presses Enter
                combinations, summary_text, error_text = run_cracker(user_text)
                scroll_offset = 0   # Jump back to the top of the list

            elif event.key == pygame.K_BACKSPACE:
                user_text    = user_text[:-1]
                combinations = []
                error_text   = ""
                summary_text = "Enter four unique digits, then press Enter."
                scroll_offset = 0

            else:
                # Accept digits only, and cap at 4 characters
                if event.unicode.isdigit() and len(user_text) < 4:
                    user_text    += event.unicode
                    combinations  = []
                    error_text    = ""
                    summary_text  = "Enter four unique digits, then press Enter."

        # Mouse-wheel scrolling for the results list
        if event.type == pygame.MOUSEWHEEL:
            total_rows   = (len(combinations) + COLS - 1) // COLS
            visible_rows = LIST_AREA.height // ROW_HEIGHT
            max_scroll   = max(0, total_rows - visible_rows)
            # event.y is +1 (scroll up) or -1 (scroll down)
            scroll_offset = max(0, min(max_scroll, scroll_offset - event.y))

    # ----------------------------------------------------------
    # 2. DRAW
    # ----------------------------------------------------------
    screen.fill(COLOUR_BG)

    # Title
    draw_text_centred(screen, "Theif!", font_title, COLOUR_ACCENT, 28)

    # Subtitle
    draw_text_centred(screen, "Enter four unique digits to crack all possible PINs",
                      font_label, COLOUR_INK_LIGHT, 80)

    # Input panel
    draw_panel(screen, pygame.Rect(120, 120, 400, 110), radius=10)

    # Label
    label = font_label.render("Digits:", True, COLOUR_INK_LIGHT)
    screen.blit(label, (INPUT_BOX.x, INPUT_BOX.y - 28))

    # Input box
    box_col = COLOUR_BOX_ACTIVE   # Always active in this simple version
    pygame.draw.rect(screen, box_col,       INPUT_BOX, border_radius=7)
    pygame.draw.rect(screen, COLOUR_BORDER, INPUT_BOX, width=2, border_radius=7)

    # Typed text inside input box (spaced-out digits look cleaner)
    spaced = "  ".join(list(user_text))
    inp_surf = font_input.render(spaced, True, COLOUR_INK)
    ty = INPUT_BOX.y + (INPUT_BOX.height - inp_surf.get_height()) // 2
    screen.blit(inp_surf, (INPUT_BOX.x + 12, ty))

    # Blinking cursor
    if (pygame.time.get_ticks() // 500) % 2 == 0:
        cur_x = INPUT_BOX.x + 12 + inp_surf.get_width() + 3
        cur_surf = font_input.render("|", True, COLOUR_BORDER)
        screen.blit(cur_surf, (cur_x, ty))

    # Error or summary text
    if error_text:
        err_surf = font_label.render(error_text, True, COLOUR_ERROR)
        ex = (WINDOW_WIDTH - err_surf.get_width()) // 2
        screen.blit(err_surf, (ex, 240))
    else:
        draw_text_centred(screen, summary_text, font_summary, COLOUR_ACCENT, 240)

    # Results list
    if combinations:
        draw_panel(screen, LIST_AREA.inflate(12, 12), radius=8)
        draw_scrollable_list(screen, combinations, LIST_AREA,
                             ROW_HEIGHT, COLS, scroll_offset)

    # Footer hint
    hint = "Backspace to clear  ·  Enter to crack  ·  Scroll to browse"
    draw_text_centred(screen, hint, font_label, COLOUR_INK_LIGHT, WINDOW_HEIGHT - 28)

    # ----------------------------------------------------------
    # 3. FLIP  (show the completed frame)
    # ----------------------------------------------------------
    pygame.display.flip()
    clock.tick(FPS)

# ============================================================
#  CLEAN UP
# ============================================================
pygame.quit()
sys.exit()
