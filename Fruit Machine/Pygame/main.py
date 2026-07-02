# =============================================================================
# FRUIT MACHINE - Pygame Edition
# =============================================================================
# A-Level Computer Science — Educational Pygame Project
#
# Learning objectives:
#   • Object-Oriented Programming (classes, methods, encapsulation)
#   • Game loops (events → update → draw → flip)
#   • Random number generation
#   • String formatting and f-strings
#   • Conditional logic and nested conditions
# =============================================================================

import pygame   # Main game library — handles graphics, events, sound
import random   # Used to randomly pick symbols for each reel
import sys      # Used to exit the program cleanly

# =============================================================================
# SECTION 1 — CONSTANTS & COLOUR PALETTE
# =============================================================================
# Constants are values that never change during the game.
# Using ALL_CAPS is a Python convention to show something is a constant.

# --- Window dimensions ---
WINDOW_WIDTH  = 700    # Width of the game window in pixels
WINDOW_HEIGHT = 600    # Height of the game window in pixels
FPS           = 60     # Frames per second — how often the screen is redrawn

# --- British Seaside Arcade Colour Palette (R, G, B tuples, each value 0-255) ---
COLOUR_BG           = (245, 240, 228)  # Warm ivory background
COLOUR_PANEL        = (228, 220, 200)  # Slightly darker cream panel behind reels
COLOUR_REEL_BG      = (255, 252, 242)  # Bright warm white for each reel box
COLOUR_REEL_OUTLINE = (180, 130,  50)  # Warm antique gold outline around reel boxes
COLOUR_GOLD         = (160, 110,  30)  # Antique gold — headings & credit
COLOUR_GOLD_DARK    = (120,  85,  20)  # Darker gold for shadows / disabled text
COLOUR_WHITE        = (255, 255, 255)  # Pure white
COLOUR_BLACK        = (  0,   0,   0)  # Pure black
COLOUR_TEXT_DARK    = ( 30,  25,  20)  # Rich dark charcoal — text on light surfaces
COLOUR_RESULT_WIN   = ( 30, 110,  55)  # Forest green — winning result messages
COLOUR_RESULT_LOSS  = (170,  40,  30)  # Deep red — losing result messages
COLOUR_RESULT_NEUT  = ( 80,  90, 100)  # Slate grey — neutral result messages

# --- Button colours ---
COLOUR_SPIN_ACTIVE  = ( 40, 110,  60)  # Forest green — spin button when enabled
COLOUR_SPIN_HOVER   = ( 55, 140,  80)  # Lighter green — when mouse is over it
COLOUR_SPIN_DISABLED= (180, 175, 165)  # Muted grey — spin button when disabled
COLOUR_QUIT_ACTIVE  = (140,  45,  35)  # Deep red — quit button
COLOUR_QUIT_HOVER   = (170,  60,  45)  # Lighter red — quit button hover
COLOUR_BTN_TEXT     = (255, 255, 255)  # White text on buttons

# --- Fruit machine game logic constants ---
START_CREDIT  = 100    # Starting credit in PENCE (100p = £1.00)
                       # Using integers for pence avoids floating-point rounding errors
COST_PER_SPIN =  20    # Cost of each spin in pence (20p = £0.20)

# --- Symbols: each is a string displayed as large text on the reel ---
# The list order matters — symbols earlier in the list appear more often
# because random.choice picks uniformly, but we could weight them by repeating entries.
SYMBOLS = ["🍒", "🔔", "🍋", "🍊", "⭐", "💀"]

# Human-readable names matching each symbol (used in result messages)
SYMBOL_NAMES = {
    "🍒": "Cherry",
    "🔔": "Bell",
    "🍋": "Lemon",
    "🍊": "Orange",
    "⭐": "Star",
    "💀": "Skull",
}

# =============================================================================
# SECTION 2 — FruitMachine CLASS
# =============================================================================
# This class models the fruit machine's internal state and rules.
# It knows nothing about pygame — it is purely logic/data.
# This separation of concerns is good software design.

class FruitMachine:
    """Encapsulates all fruit machine game logic and state."""

    def __init__(self):
        """Initialise the machine with starting values."""
        self.credit       = START_CREDIT  # Current credit in pence
        self.reels        = ["🍒", "🍒", "🍒"]  # The three displayed symbols
        self.last_winnings = 0             # Pence won/lost on the last spin
        self.last_message  = "Press SPIN to play!"  # Result shown to the player
        self.spun_once     = False         # Track whether any spin has happened

    # -------------------------------------------------------------------------
    def roll(self):
        """
        Spin all three reels by randomly choosing a symbol for each one.
        Returns the list of three symbols chosen.
        """
        # random.choice picks one item at random from the list each time
        self.reels = [random.choice(SYMBOLS) for _ in range(3)]
        return self.reels  # Return the new symbols so the caller can use them

    # -------------------------------------------------------------------------
    def calculate_winnings(self):
        """
        Apply the prize rules to the current reel symbols.
        Updates self.credit and self.last_winnings.
        Returns a (winnings_in_pence, message_string) tuple.

        Prize table:
          Three Skulls          -> credit set to 0 (bankrupt!)
          Two Skulls            -> lose 80p extra on top of spin cost
          Three Bells           -> win 480p (4.80)
          Three of same (other) -> win 80p (0.80)
          Two of same           -> win 40p (0.40)
          No match              -> no extra win/loss (spin cost already deducted)
        """
        s = self.reels           # Shorthand — s[0], s[1], s[2] are the symbols
        skull = "💀"             # Shorthand for the skull symbol

        # Count how many skulls appear across the three reels
        skull_count = s.count(skull)

        # Count how many of the same symbol appear (for any symbol)
        # We look at each unique symbol and find the maximum frequency
        counts = {sym: s.count(sym) for sym in set(s)}  # e.g. {"🍒": 2, "🍋": 1}
        max_count = max(counts.values())                  # e.g. 2

        # --- Apply rules in priority order (most severe first) ---

        if skull_count == 3:
            # Three skulls: instant bankrupt — set credit to zero
            delta   = -self.credit          # Lose everything remaining
            message = "💀💀💀 THREE SKULLS! You lose everything! 💀💀💀"

        elif skull_count == 2:
            # Two skulls: lose an extra 80p on top of the spin cost
            delta   = -80
            message = "💀💀 Two Skulls! You lose an extra £0.80!"

        elif s[0] == s[1] == s[2] and s[0] == "🔔":
            # Three Bells: the jackpot!
            delta   = 480
            message = "🔔🔔🔔 THREE BELLS! JACKPOT! +£4.80! 🔔🔔🔔"

        elif max_count == 3:
            # Three of the same symbol (not Bells, already handled above)
            name    = SYMBOL_NAMES[s[0]]       # Look up the human-readable name
            delta   = 80
            message = f"{s[0]}{s[0]}{s[0]} Three {name}s! +£0.80!"

        elif max_count == 2:
            # Two of the same symbol — find which symbol is repeated
            # next() with a generator expression finds the first matching key
            matched_sym = next(sym for sym, cnt in counts.items() if cnt == 2)
            name    = SYMBOL_NAMES[matched_sym]
            delta   = 40
            message = f"Two {name}s! +£0.40!"

        else:
            # No match — no extra prize, spin cost already taken
            delta   = 0
            message = "No match. Better luck next time!"

        # Apply the delta to credit
        self.credit        += delta
        self.last_winnings  = delta
        self.last_message   = message
        self.spun_once      = True

        # Clamp credit to zero minimum (can't go below zero)
        if self.credit < 0:
            self.credit = 0

        return delta, message  # Return values so main loop can react if needed

    # -------------------------------------------------------------------------
    def deduct_spin_cost(self):
        """Deduct the cost of one spin from credit. Call this before rolling."""
        self.credit -= COST_PER_SPIN  # Take the spin fee from the player's credit

    # -------------------------------------------------------------------------
    def can_spin(self):
        """Return True if the player has enough credit to spin."""
        return self.credit >= COST_PER_SPIN  # Must have at least 20p to play

    # -------------------------------------------------------------------------
    def is_game_over(self):
        """Return True if the player has run out of credit."""
        return self.credit <= 0  # Game ends when credit drops to zero or below

    # -------------------------------------------------------------------------
    def credit_string(self):
        """Return the credit as a formatted pound-sterling string, e.g. '£0.80'."""
        # Integer division (//) gives whole pounds; modulo (%) gives remaining pence
        pounds = self.credit // 100
        pence  = self.credit %  100
        return f"£{pounds}.{pence:02d}"  # :02d pads pence with a leading zero if needed


# =============================================================================
# SECTION 3 — Button CLASS
# =============================================================================
# Reusable button widget. Draws itself and detects mouse clicks.
# Keeping drawing logic inside the class is good encapsulation.

class Button:
    """A clickable on-screen button with hover and disabled states."""

    def __init__(self, x, y, width, height, label,
                 colour_normal, colour_hover, colour_text=COLOUR_BTN_TEXT,
                 font=None, corner_radius=14):
        """
        Initialise the button.

        Parameters:
            x, y          — top-left position of the button
            width, height — dimensions in pixels
            label         — text displayed on the button
            colour_normal — background colour when not hovered
            colour_hover  — background colour when mouse is over it
            colour_text   — text colour (default white)
            font          — pygame.Font object (uses default if None)
            corner_radius — roundness of corners in pixels
        """
        self.rect          = pygame.Rect(x, y, width, height)  # Defines position & size
        self.label         = label
        self.colour_normal = colour_normal
        self.colour_hover  = colour_hover
        self.colour_text   = colour_text
        self.font          = font or pygame.font.SysFont("arial", 26, bold=True)
        self.corner_radius = corner_radius
        self.enabled       = True   # When False the button is greyed out and unclickable
        self.hovered       = False  # Tracks whether the mouse is currently over this button

    # -------------------------------------------------------------------------
    def draw(self, surface):
        """
        Draw the button onto the given surface.
        Changes appearance depending on enabled/hovered state.
        """
        if self.enabled:
            # Pick normal or hover colour depending on mouse position
            bg_colour = self.colour_hover if self.hovered else self.colour_normal
            text_col  = self.colour_text
        else:
            # Disabled: flat dull colour, dimmed text
            bg_colour = COLOUR_SPIN_DISABLED
            text_col  = COLOUR_GOLD_DARK

        # Draw the rounded rectangle background
        pygame.draw.rect(surface, bg_colour, self.rect,
                         border_radius=self.corner_radius)

        # Draw a gold border around the button
        pygame.draw.rect(surface, COLOUR_GOLD, self.rect,
                         width=2, border_radius=self.corner_radius)

        # Render the label text and centre it on the button
        text_surf = self.font.render(self.label, True, text_col)
        text_rect = text_surf.get_rect(center=self.rect.center)  # Centre-align
        surface.blit(text_surf, text_rect)  # blit = draw one surface onto another

    # -------------------------------------------------------------------------
    def is_clicked(self, mouse_pos):
        """
        Return True if the button is enabled AND the given mouse position
        is inside the button's rectangle.

        mouse_pos — a (x, y) tuple, typically from pygame.mouse.get_pos()
        """
        if not self.enabled:
            return False  # Disabled buttons cannot be clicked
        return self.rect.collidepoint(mouse_pos)  # collidepoint checks if point is inside rect

    # -------------------------------------------------------------------------
    def update_hover(self, mouse_pos):
        """Update self.hovered based on current mouse position. Call each frame."""
        self.hovered = self.rect.collidepoint(mouse_pos)


# =============================================================================
# SECTION 4 — HELPER / DRAWING FUNCTIONS
# =============================================================================
# Standalone functions that handle specific drawing tasks.
# Breaking the drawing into small functions keeps main() readable.

def draw_rounded_rect_with_shadow(surface, colour, rect, radius=18,
                                  shadow_offset=5):
    """
    Draw a rounded rectangle with a simple drop-shadow beneath it.
    This gives the reel boxes a 3-D casino feel.
    """
    # Draw shadow first (so it appears behind the main box)
    shadow_rect = rect.move(shadow_offset, shadow_offset)  # Offset to bottom-right
    pygame.draw.rect(surface, COLOUR_BLACK, shadow_rect, border_radius=radius)

    # Draw the main coloured box on top
    pygame.draw.rect(surface, colour, rect, border_radius=radius)


def draw_background(surface):
    """Fill the background with the deep purple and draw decorative gold lines."""
    surface.fill(COLOUR_BG)  # Fill entire window with background colour

    # Draw subtle horizontal grid lines for a retro Vegas feel
    for y in range(0, WINDOW_HEIGHT, 60):          # Every 60 pixels vertically
        pygame.draw.line(surface, (220, 215, 200), # Subtle warm grey lines
                         (0, y), (WINDOW_WIDTH, y), 1)


def draw_title(surface, font_large):
    """Render the game title at the top of the screen."""
    title_surf = font_large.render("LUCKY REELS - Fruit Machine", True, COLOUR_GOLD)
    # Centre the title horizontally at y=28
    title_rect = title_surf.get_rect(centerx=WINDOW_WIDTH // 2, top=28)
    surface.blit(title_surf, title_rect)

    # Gold underline beneath the title
    line_y = title_rect.bottom + 8
    pygame.draw.line(surface, COLOUR_GOLD,
                     (60, line_y), (WINDOW_WIDTH - 60, line_y), 2)


def draw_reels(surface, symbols, font_symbol, font_name, reel_y=185):
    """
    Draw the three reel boxes side by side, each showing one symbol.

    symbols    — list of three symbol strings (e.g. ["🍒", "💀", "🔔"])
    font_symbol — large font used to render the emoji character
    font_name   — smaller font used to render the symbol name underneath
    reel_y      — vertical position of the top of the reel boxes
    """
    reel_width   = 140   # Width of each individual reel box
    reel_height  = 150   # Height of each reel box
    reel_gap     = 24    # Gap between adjacent reel boxes
    total_width  = 3 * reel_width + 2 * reel_gap        # Total width of all three reels
    start_x      = (WINDOW_WIDTH - total_width) // 2    # X position of first reel (centred)

    # Draw the decorative panel behind all three reels
    panel_padding = 22
    panel_rect = pygame.Rect(
        start_x - panel_padding,
        reel_y  - panel_padding,
        total_width  + 2 * panel_padding,
        reel_height  + 2 * panel_padding + 34  # +34 for name label below symbol
    )
    pygame.draw.rect(surface, COLOUR_PANEL, panel_rect, border_radius=22)
    pygame.draw.rect(surface, COLOUR_REEL_OUTLINE, panel_rect,
                     width=3, border_radius=22)  # Gold border around panel

    for i, symbol in enumerate(symbols):
        # Calculate the left edge of this particular reel box
        box_x = start_x + i * (reel_width + reel_gap)
        box_rect = pygame.Rect(box_x, reel_y, reel_width, reel_height)

        # Draw shadow + cream background box
        draw_rounded_rect_with_shadow(surface, COLOUR_REEL_BG, box_rect, radius=16)

        # Gold outline around reel box
        pygame.draw.rect(surface, COLOUR_REEL_OUTLINE, box_rect,
                         width=3, border_radius=16)

        # Render the symbol text — centred horizontally and vertically in the box
        sym_surf = font_symbol.render(symbol, True, COLOUR_TEXT_DARK)
        sym_rect = sym_surf.get_rect(center=(box_x + reel_width // 2,
                                             reel_y  + reel_height // 2 - 10))
        surface.blit(sym_surf, sym_rect)

        # Render the symbol's human-readable name below the symbol
        name      = SYMBOL_NAMES.get(symbol, symbol)        # Look up name, fallback to symbol
        name_surf = font_name.render(name, True, COLOUR_TEXT_DARK)
        name_rect = name_surf.get_rect(
            centerx=box_x + reel_width // 2,
            top=reel_y + reel_height + 6             # Just below the reel box
        )
        surface.blit(name_surf, name_rect)


def draw_credit(surface, machine, font_credit, font_label):
    """Display the player's current credit balance prominently."""
    label_surf = font_label.render("CREDIT", True, COLOUR_GOLD_DARK)
    label_rect = label_surf.get_rect(centerx=WINDOW_WIDTH // 2, top=108)
    surface.blit(label_surf, label_rect)

    credit_surf = font_credit.render(machine.credit_string(), True, COLOUR_GOLD)
    credit_rect = credit_surf.get_rect(centerx=WINDOW_WIDTH // 2, top=126)
    surface.blit(credit_surf, credit_rect)


def draw_result_message(surface, message, winnings, font_result):
    """
    Show the result of the last spin in colour-coded text.

    winnings > 0  -> green (win)
    winnings < 0  -> red   (loss)
    winnings == 0 -> pale lavender (neutral)
    """
    if winnings > 0:
        colour = COLOUR_RESULT_WIN
    elif winnings < 0:
        colour = COLOUR_RESULT_LOSS
    else:
        colour = COLOUR_RESULT_NEUT

    msg_surf = font_result.render(message, True, colour)
    msg_rect = msg_surf.get_rect(centerx=WINDOW_WIDTH // 2, top=405)
    surface.blit(msg_surf, msg_rect)


def draw_game_over_screen(surface, machine, font_large, font_medium, font_small):
    """
    Overlay a semi-transparent game-over panel in the centre of the screen.
    Shown when the player has run out of credit.
    """
    # Semi-transparent dark overlay covering the whole window
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((30, 20, 10, 210))   # RGBA — last value is alpha (0=clear, 255=solid)
    surface.blit(overlay, (0, 0))

    # Central panel
    panel_rect = pygame.Rect(120, 130, 460, 300)
    pygame.draw.rect(surface, COLOUR_PANEL, panel_rect, border_radius=24)
    pygame.draw.rect(surface, COLOUR_GOLD, panel_rect, width=3, border_radius=24)

    # "GAME OVER" heading
    go_surf = font_large.render("GAME OVER", True, COLOUR_RESULT_LOSS)
    go_rect = go_surf.get_rect(centerx=WINDOW_WIDTH // 2, top=150)
    surface.blit(go_surf, go_rect)

    # Skull decoration
    skull_surf = font_medium.render("💀  💀  💀", True, COLOUR_RESULT_LOSS)
    skull_rect = skull_surf.get_rect(centerx=WINDOW_WIDTH // 2, top=210)
    surface.blit(skull_surf, skull_rect)

    # Broke message
    broke_surf = font_medium.render("You've run out of credit!", True, COLOUR_WHITE)
    broke_rect = broke_surf.get_rect(centerx=WINDOW_WIDTH // 2, top=262)
    surface.blit(broke_surf, broke_rect)

    # Instruction to quit
    quit_surf = font_small.render("Press QUIT to exit", True, COLOUR_GOLD_DARK)
    quit_rect = quit_surf.get_rect(centerx=WINDOW_WIDTH // 2, top=310)
    surface.blit(quit_surf, quit_rect)


# =============================================================================
# SECTION 5 — MAIN FUNCTION (Bootstrap + Game Loop)
# =============================================================================
# main() is the entry point. It sets up pygame, creates objects, then runs
# the game loop: Process Events -> Update State -> Draw -> Flip

def main():
    """Initialise pygame and run the main game loop."""

    # --- Bootstrap pygame ---
    pygame.init()                                          # Start all pygame modules
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # Create window
    pygame.display.set_caption("Lucky Reels - Fruit Machine")        # Window title bar
    clock = pygame.time.Clock()                            # Used to cap frame rate

    # --- Load fonts ---
    # pygame.font.SysFont(name, size, bold, italic)
    # "segoeuiemoji" is a Windows font that renders emoji well.
    # Providing "arial" as a fallback ensures it works on other platforms.
    font_title   = pygame.font.SysFont("arial", 34, bold=True)
    font_symbol  = pygame.font.SysFont("segoeuiemoji,arial", 70, bold=False)  # Big reel symbols
    font_name    = pygame.font.SysFont("arial", 17, bold=True)    # Symbol name label
    font_credit  = pygame.font.SysFont("arial", 40, bold=True)    # Credit amount
    font_label   = pygame.font.SysFont("arial", 15, bold=False)   # "CREDIT" label
    font_result  = pygame.font.SysFont("segoeuiemoji,arial", 20, bold=True)  # Result message
    font_medium  = pygame.font.SysFont("segoeuiemoji,arial", 26, bold=True)
    font_small   = pygame.font.SysFont("arial", 18)
    font_btn     = pygame.font.SysFont("arial", 28, bold=True)    # Button labels

    # --- Create game objects ---
    machine = FruitMachine()  # Create a new fruit machine (sets credit to 100p = £1.00)

    # SPIN button — left of centre at the bottom
    btn_spin = Button(
        x=175, y=458,
        width=160, height=56,
        label="  SPIN  ",
        colour_normal=COLOUR_SPIN_ACTIVE,
        colour_hover=COLOUR_SPIN_HOVER,
        font=font_btn
    )

    # QUIT button — right of centre at the bottom
    btn_quit = Button(
        x=365, y=458,
        width=160, height=56,
        label="  QUIT  ",
        colour_normal=COLOUR_QUIT_ACTIVE,
        colour_hover=COLOUR_QUIT_HOVER,
        font=font_btn
    )

    # --- State variables used inside the game loop ---
    game_over    = False   # Becomes True when the player runs out of credit
    spin_result  = 0       # Winnings delta from the last spin (for colour-coding)

    # ==========================================================================
    # GAME LOOP — runs once per frame until the user quits
    # Standard structure: Events -> Update -> Draw -> Flip
    # ==========================================================================
    running = True
    while running:

        # ---- PHASE 1: Process Events -----------------------------------------
        # pygame.event.get() returns a list of all events that occurred since last frame
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                # User clicked the red X on the window's title bar
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Left mouse button was pressed — check which UI button was clicked
                mouse_pos = pygame.mouse.get_pos()  # (x, y) tuple of click position

                if btn_quit.is_clicked(mouse_pos):
                    running = False   # Exit the game loop

                if btn_spin.is_clicked(mouse_pos) and not game_over:
                    # --- Perform one full spin ---
                    machine.deduct_spin_cost()               # 1. Deduct spin cost (20p)
                    machine.roll()                           # 2. Randomly choose symbols
                    spin_result, _ = machine.calculate_winnings()  # 3. Calculate prize

                    # 4. Check if player has now run out of credit
                    if machine.is_game_over():
                        game_over = True

        # ---- PHASE 2: Update State -------------------------------------------
        # Get current mouse position each frame to drive hover effects
        mouse_pos = pygame.mouse.get_pos()
        btn_spin.update_hover(mouse_pos)   # Update spin button hover state
        btn_quit.update_hover(mouse_pos)   # Update quit button hover state

        # Disable the spin button if player can't afford another spin
        btn_spin.enabled = machine.can_spin() and not game_over

        # ---- PHASE 3: Draw Everything ----------------------------------------
        # Draw order matters — things drawn later appear in front of earlier things

        draw_background(screen)                           # 1. Background + decorative lines
        draw_title(screen, font_title)                    # 2. Title banner + gold underline
        draw_credit(screen, machine, font_credit, font_label)  # 3. Credit display

        draw_reels(screen, machine.reels,                # 4. Three reel boxes with symbols
                   font_symbol, font_name)

        # 5. Result message (colour-coded win/loss/neutral)
        if machine.spun_once:
            draw_result_message(screen, machine.last_message,
                                spin_result, font_result)
        else:
            # Before first spin — show a welcoming prompt instead
            hint_surf = font_result.render("Press SPIN to play!", True, COLOUR_RESULT_NEUT)
            hint_rect = hint_surf.get_rect(centerx=WINDOW_WIDTH // 2, top=405)
            screen.blit(hint_surf, hint_rect)

        # 6. Draw quick-reference prize table at the very bottom
        prize_lines = [
            "3x Bell=+£4.80  |  3x same=+£0.80  |  2x same=+£0.40  |  Spin costs £0.20",
            "3x Skull=LOSE ALL  |  2x Skull=-£0.80 extra",
        ]
        for idx, line in enumerate(prize_lines):
            ps = font_small.render(line, True, COLOUR_GOLD_DARK)
            pr = ps.get_rect(centerx=WINDOW_WIDTH // 2, top=544 + idx * 22)
            screen.blit(ps, pr)

        # 7. Buttons (drawn last so they appear on top of everything else)
        btn_spin.draw(screen)
        btn_quit.draw(screen)

        # 8. Game-over overlay (drawn on very top when active)
        if game_over:
            draw_game_over_screen(screen, machine,
                                  font_title, font_medium, font_small)
            btn_quit.draw(screen)   # Still show quit button above the overlay

        # ---- PHASE 4: Flip the display buffer --------------------------------
        # pygame uses double-buffering: we draw to a hidden surface, then
        # flip it onto the visible screen all at once to prevent flickering.
        pygame.display.flip()

        # Cap the loop to FPS frames per second to avoid using 100% CPU
        clock.tick(FPS)

    # --- Cleanup ---
    pygame.quit()   # Shut down all pygame modules cleanly
    sys.exit()      # Exit the Python process with no error code


# =============================================================================
# SECTION 6 — ENTRY POINT
# =============================================================================
# This block only runs when this script is executed directly (not imported).
# It is standard Python practice to guard the entry point this way.
# If another script did: import main — this block would NOT run.

if __name__ == "__main__":
    main()
