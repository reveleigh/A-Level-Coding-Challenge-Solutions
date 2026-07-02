# =============================================================================
# SPEED CAMERA / AVERAGE SPEED TRACKER — Pygame Educational Version
# =============================================================================
# A-Level Computer Science — Python / Pygame demonstration
#
# HOW IT WORKS (real-world context):
#   Two ANPR (Automatic Number Plate Recognition) cameras are placed exactly
#   1 mile apart on a motorway.  Camera 1 records the time a vehicle passes it;
#   Camera 2 records the time the same vehicle passes it.  Average speed is:
#
#       speed (mph) = distance (miles) / time (hours)
#                   = 1  /  ((time2 - time1) / 3600)
#
#   If that speed exceeds 70 mph the vehicle is flagged for a penalty notice.
#
# LEARNING OBJECTIVES:
#   * OOP — Vehicle class with validation and calculation methods
#   * GUI input handling — keyboard focus, Tab cycling, Enter to submit
#   * Conditional logic and string validation
#   * Accumulating a session log and rendering a scrollable list
# =============================================================================

import pygame   # the only graphics / event library we need
import sys      # used for sys.exit() to close the window cleanly

# =============================================================================
# CONSTANTS — colours, dimensions, fonts sizes, game rules
# =============================================================================

# --- Motorway / road-sign colour palette ---
C_BG           = (18,  38,  46)   # very dark teal — main background
C_PANEL        = (26,  54,  64)   # slightly lighter panel background
C_BORDER       = (52, 100, 112)   # muted teal border for boxes
C_BORDER_FOCUS = (255, 210,   0)  # highway yellow — active input field
C_TEXT         = (230, 240, 245)  # near-white general text
C_LABEL        = (160, 200, 210)  # pale teal for field labels
C_HEADING      = (255, 210,   0)  # bright yellow — section headings
C_BTN_IDLE     = ( 34,  85,  85)  # dark green-teal button normal state
C_BTN_HOVER    = ( 46, 120, 120)  # lighter teal button hover state
C_BTN_TEXT     = (255, 255, 255)  # white text on button
C_SAFE         = ( 60, 200, 100)  # motorway green — not speeding
C_WARN         = (255, 160,  30)  # amber — borderline / warning
C_DANGER       = (220,  50,  50)  # red — speeding
C_LOG_ROW_A    = ( 22,  46,  56)  # alternating log row colour A
C_LOG_ROW_B    = ( 28,  58,  70)  # alternating log row colour B
C_DIVIDER      = ( 52,  90, 100)  # thin horizontal rule colour
C_SCROLL_TRACK = ( 36,  66,  78)  # scrollbar track
C_SCROLL_THUMB = ( 80, 140, 160)  # scrollbar thumb

# --- Layout dimensions (all in pixels) ---
WINDOW_W       = 820    # total window width
WINDOW_H       = 700    # total window height
PADDING        = 20     # standard inner padding
INPUT_H        = 44     # height of each text input box
BTN_W          = 160    # width of the Check / Submit button
BTN_H          = 44     # height of the Check / Submit button
LOG_X          = PADDING                      # log panel left edge
LOG_Y          = 390                          # log panel top edge
LOG_W          = WINDOW_W - PADDING * 2       # log panel width
LOG_H          = WINDOW_H - LOG_Y - PADDING  # log panel height
LOG_ROW_H      = 28     # height of a single log entry row
SCROLL_W       = 12     # width of the scrollbar strip

# --- Speed camera rules ---
CAMERA_DISTANCE_MILES = 1    # cameras are exactly 1 mile apart
SPEED_LIMIT_MPH       = 70   # UK motorway speed limit

# --- Font sizes ---
FS_LARGE  = 22   # section headings / result verdict
FS_NORMAL = 18   # labels, input text, button text
FS_SMALL  = 15   # log rows and secondary info

# =============================================================================
# VEHICLE CLASS — encapsulates one recorded vehicle journey between cameras
# =============================================================================

class Vehicle:
    """
    Represents a single vehicle that has been captured by both cameras.

    Attributes:
        plate (str)  : The number plate string entered by the operator.
        time1 (float): Time in seconds when vehicle passed Camera 1.
        time2 (float): Time in seconds when vehicle passed Camera 2.
    """

    def __init__(self, plate: str, time1: float, time2: float):
        """
        Constructor — called when we create a new Vehicle object.
        Stores the three raw data values as instance attributes.
        """
        self.plate = plate.strip().upper()  # normalise plate to upper-case
        self.time1 = time1                  # seconds at camera 1
        self.time2 = time2                  # seconds at camera 2

    # ------------------------------------------------------------------
    def is_plate_valid(self) -> bool:
        """
        Validates the UK number plate format: AB12 ERT (8 characters).

        Rules:
            chars 0-1  : two alphabetic letters   (e.g. 'AB')
            chars 2-3  : two numeric digits        (e.g. '12')
            char  4    : a single space            (e.g. ' ')
            chars 5-7  : three alphabetic letters  (e.g. 'ERT')

        Returns True if the plate matches all rules, False otherwise.
        """
        if len(self.plate) != 8:             # must be exactly 8 characters
            return False
        if not self.plate[:2].isalpha():     # first two must be letters
            return False
        if not self.plate[2:4].isdigit():    # next two must be digits
            return False
        if self.plate[4] != ' ':             # fifth character must be a space
            return False
        if not self.plate[5:8].isalpha():    # last three must be letters
            return False
        return True                          # all checks passed

    # ------------------------------------------------------------------
    def calculate_speed(self) -> float:
        """
        Calculates average speed in miles per hour using:

            speed = distance / time
                  = 1 mile / ((time2 - time1) seconds / 3600)

        Returns the speed as a float, or -1.0 if the time difference is
        zero or negative (which would be physically impossible / bad data).
        """
        time_diff_seconds = self.time2 - self.time1   # elapsed seconds between cameras
        if time_diff_seconds <= 0:                    # guard: time must be positive
            return -1.0                               # sentinel value for invalid data
        time_diff_hours = time_diff_seconds / 3600    # convert seconds to hours
        speed = CAMERA_DISTANCE_MILES / time_diff_hours  # speed = distance / time
        return round(speed, 2)                        # round to 2 decimal places

    # ------------------------------------------------------------------
    def is_speeding(self) -> bool:
        """
        Returns True if the calculated speed exceeds the speed limit.
        Returns False if speed is within the limit or data is invalid.
        """
        speed = self.calculate_speed()
        if speed < 0:          # invalid data — don't flag as speeding
            return False
        return speed > SPEED_LIMIT_MPH   # True if over the limit


# =============================================================================
# HELPER FUNCTIONS — drawing utilities used by the main loop
# =============================================================================

def draw_text(surface, text, font, colour, x, y, align="left"):
    """
    Renders a single string onto the surface at (x, y).
    align='left'   -> x is the left edge   (default)
    align='centre' -> x is the centre point
    align='right'  -> x is the right edge
    """
    rendered = font.render(text, True, colour)   # create the text surface
    rect = rendered.get_rect()                   # get its bounding rectangle

    if align == "centre":
        rect.centerx = x     # centre the text horizontally around x
        rect.top = y
    elif align == "right":
        rect.right = x       # pin the right edge to x
        rect.top = y
    else:
        rect.left = x        # default: left edge at x
        rect.top = y

    surface.blit(rendered, rect)    # draw the text onto the surface


# ------------------------------------------------------------------
def draw_panel(surface, x, y, w, h, colour=C_PANEL, radius=8):
    """
    Draws a rounded-rectangle panel — used for input areas, result box, log.
    """
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(surface, colour, rect, border_radius=radius)


# ------------------------------------------------------------------
def draw_input_box(surface, rect, text, label, font_label, font_input,
                   focused=False, placeholder=""):
    """
    Draws a labelled text input box.

    rect        : pygame.Rect for the input field itself
    text        : current string content of the field
    label       : small label drawn above the box
    focused     : True when this field has keyboard focus (highlighted border)
    placeholder : greyed hint text shown when field is empty
    """
    # Draw the label above the box
    draw_text(surface, label, font_label, C_LABEL,
              rect.x, rect.y - 22)

    # Draw the box background
    pygame.draw.rect(surface, C_BG, rect, border_radius=6)

    # Draw the border — yellow if focused, teal otherwise
    border_col = C_BORDER_FOCUS if focused else C_BORDER
    pygame.draw.rect(surface, border_col, rect, width=2, border_radius=6)

    # Draw placeholder text if field is empty and not focused
    if text == "" and not focused:
        draw_text(surface, placeholder, font_input, C_BORDER,
                  rect.x + 10, rect.y + 10)
    else:
        # Draw the actual text content with a blinking cursor if focused
        display = text + ("|" if focused else "")   # append cursor character
        draw_text(surface, display, font_input, C_TEXT,
                  rect.x + 10, rect.y + 10)


# ------------------------------------------------------------------
def draw_button(surface, rect, label, font, mouse_pos):
    """
    Draws a rounded button and returns True if the mouse is hovering over it.
    """
    hovering = rect.collidepoint(mouse_pos)   # check if mouse is over button
    colour = C_BTN_HOVER if hovering else C_BTN_IDLE
    pygame.draw.rect(surface, colour, rect, border_radius=8)
    pygame.draw.rect(surface, C_BORDER, rect, width=2, border_radius=8)
    draw_text(surface, label, font, C_BTN_TEXT,
              rect.centerx, rect.centery - font.get_height() // 2, align="centre")
    return hovering   # caller can use this to check if hovering


# ------------------------------------------------------------------
def draw_divider(surface, y):
    """Draws a thin horizontal rule across the window."""
    pygame.draw.line(surface, C_DIVIDER,
                     (PADDING, y), (WINDOW_W - PADDING, y), 1)


# =============================================================================
# BOOTSTRAP — initialise Pygame, create the window, load fonts
# =============================================================================

pygame.init()                                     # start all Pygame modules

screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))   # create the window
pygame.display.set_caption("Speed Camera Tracker — A-Level CS")

clock = pygame.time.Clock()   # used to cap the frame rate to 60 fps

# Load fonts — pygame.font.SysFont uses fonts installed on the OS.
# We use a monospace face for the plate field so characters line up neatly.
font_heading = pygame.font.SysFont("Arial",       FS_LARGE,  bold=True)
font_label   = pygame.font.SysFont("Arial",       FS_SMALL,  bold=False)
font_normal  = pygame.font.SysFont("Arial",       FS_NORMAL, bold=False)
font_input   = pygame.font.SysFont("Courier New", FS_NORMAL, bold=True)
font_small   = pygame.font.SysFont("Arial",       FS_SMALL,  bold=False)
font_verdict = pygame.font.SysFont("Arial",       FS_LARGE,  bold=True)

# =============================================================================
# APPLICATION STATE — variables that change while the program is running
# =============================================================================

# --- Three input field strings ---
fields       = ["", "", ""]    # index 0=plate, 1=time1, 2=time2
focus_index  = 0               # which field currently has keyboard focus (0,1,2)

# --- Result state (shown after pressing Check) ---
result       = None            # None = no result yet; dict = last result
error_msg    = ""              # error string shown if inputs are bad

# --- Session log — list of dicts, one per vehicle checked ---
log_entries  = []              # each entry is a dict with plate, speed, speeding flag
log_scroll   = 0               # how many rows we have scrolled down
log_dragging = False           # True while user is dragging the scrollbar thumb

# --- Layout rectangles for the three input fields ---
# Placed in a row: plate on the left, times in the middle and right
field_rects = [
    pygame.Rect(PADDING,         130, 280, INPUT_H),   # number plate
    pygame.Rect(PADDING + 300,   130, 200, INPUT_H),   # camera 1 time
    pygame.Rect(PADDING + 520,   130, 200, INPUT_H),   # camera 2 time
]

# Button rectangle — sits to the right of the input row
btn_rect = pygame.Rect(WINDOW_W - PADDING - BTN_W, 130, BTN_W, BTN_H)

# Result panel rectangle — sits below the input row
result_rect = pygame.Rect(PADDING, 210, WINDOW_W - PADDING * 2, 155)

# Log clip rectangle — the visible area for the scrollable log
log_clip_rect = pygame.Rect(LOG_X, LOG_Y, LOG_W - SCROLL_W - 4, LOG_H)


# =============================================================================
# HELPER — process the Check button / Enter key press
# =============================================================================

def run_check():
    """
    Reads the three input fields, creates a Vehicle object, validates inputs,
    runs the speed calculation and appends the result to the session log.
    All output is stored in the global 'result' and 'error_msg' variables.
    """
    global result, error_msg, log_scroll

    plate_raw = fields[0].strip()   # raw plate string from field 0
    t1_raw    = fields[1].strip()   # raw time-1 string from field 1
    t2_raw    = fields[2].strip()   # raw time-2 string from field 2

    # ---- Validate that both time fields contain numbers ----
    try:
        t1 = float(t1_raw)   # convert cam1 time to a float
        t2 = float(t2_raw)   # convert cam2 time to a float
    except ValueError:
        # One or both time fields couldn't be converted — show an error
        error_msg = "Camera times must be numbers (e.g. 3600 or 3600.5)"
        result    = None
        return

    # ---- Build the Vehicle object and run its methods ----
    vehicle = Vehicle(plate_raw, t1, t2)

    plate_ok = vehicle.is_plate_valid()       # bool — plate format valid?
    speed    = vehicle.calculate_speed()      # float — mph, or -1 if bad
    speeding = vehicle.is_speeding()          # bool — over limit?

    # ---- Compose a result dictionary for the GUI to render ----
    result = {
        "plate"   : vehicle.plate,
        "plate_ok": plate_ok,
        "speed"   : speed,
        "speeding": speeding,
        "t1"      : t1,
        "t2"      : t2,
    }
    error_msg = ""   # clear any previous error

    # ---- Append a summary line to the session log ----
    log_entries.append({
        "plate"   : vehicle.plate if plate_ok else vehicle.plate + " [INVALID]",
        "speed"   : speed,
        "speeding": speeding,
        "plate_ok": plate_ok,
    })

    # Auto-scroll the log to show the newest entry at the bottom
    visible_rows = log_clip_rect.height // LOG_ROW_H   # how many rows fit in view
    max_scroll   = max(0, len(log_entries) - visible_rows)
    log_scroll   = max_scroll   # jump to end of log


# =============================================================================
# MAIN LOOP — event handling, update, draw — runs at 60 fps
# =============================================================================

running = True   # set to False to exit the loop

while running:

    # ---- Step 1: Handle events ----------------------------------------
    mouse_pos = pygame.mouse.get_pos()   # current mouse (x, y) every frame

    for event in pygame.event.get():

        # ---- Window close button ----
        if event.type == pygame.QUIT:
            running = False   # exit the main loop on next iteration

        # ---- Mouse button down ----
        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:   # left mouse button only

                # Check which input field (if any) was clicked
                for i, rect in enumerate(field_rects):
                    if rect.collidepoint(mouse_pos):
                        focus_index = i   # give focus to clicked field

                # Check if the Check button was clicked
                if btn_rect.collidepoint(mouse_pos):
                    run_check()

                # Check if the scrollbar track was clicked
                scrollbar_x    = LOG_X + LOG_W - SCROLL_W   # left edge of scrollbar
                scrollbar_rect = pygame.Rect(scrollbar_x, LOG_Y, SCROLL_W, LOG_H)
                if scrollbar_rect.collidepoint(mouse_pos):
                    log_dragging = True   # start dragging the scroll thumb

            # Mouse wheel scrolls the log
            if event.button == 4:   # scroll wheel up
                log_scroll = max(0, log_scroll - 1)
            if event.button == 5:   # scroll wheel down
                visible_rows = log_clip_rect.height // LOG_ROW_H
                max_scroll   = max(0, len(log_entries) - visible_rows)
                log_scroll   = min(max_scroll, log_scroll + 1)

        # ---- Mouse button release ----
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                log_dragging = False   # stop dragging scrollbar

        # ---- Mouse motion — update scroll position while dragging ----
        elif event.type == pygame.MOUSEMOTION:
            if log_dragging and len(log_entries) > 0:
                # Map the mouse Y position within the log panel to a scroll value
                relative_y = mouse_pos[1] - LOG_Y          # y relative to log top
                fraction   = relative_y / LOG_H            # 0.0 to 1.0
                fraction   = max(0.0, min(1.0, fraction))  # clamp to valid range
                visible_rows = log_clip_rect.height // LOG_ROW_H
                max_scroll   = max(0, len(log_entries) - visible_rows)
                log_scroll   = int(fraction * max_scroll)   # convert to row index

        # ---- Keyboard events ----
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_TAB:
                # Tab cycles focus: 0 -> 1 -> 2 -> 0 -> ...
                focus_index = (focus_index + 1) % len(fields)

            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                # Enter key triggers the check from any field
                run_check()

            elif event.key == pygame.K_BACKSPACE:
                # Delete the last character from the focused field
                fields[focus_index] = fields[focus_index][:-1]

            else:
                # Append the typed character to the focused field
                char = event.unicode   # the printable character (may be empty)
                if char:               # ignore non-printable keys
                    # Enforce a sensible maximum length per field
                    max_lengths = [9, 12, 12]   # plate buffer, two time fields
                    if len(fields[focus_index]) < max_lengths[focus_index]:
                        fields[focus_index] += char

    # ---- Step 2: Draw everything ---------------------------------------

    screen.fill(C_BG)   # clear the screen with the dark background colour

    # ---- App title bar ----
    draw_text(screen, "AVERAGE SPEED CAMERA SYSTEM", font_heading,
              C_HEADING, WINDOW_W // 2, 18, align="centre")
    draw_text(screen, "Cameras are 1 mile apart  |  Speed limit: 70 mph",
              font_small, C_LABEL, WINDOW_W // 2, 48, align="centre")
    draw_divider(screen, 72)

    # ---- Input section heading ----
    draw_text(screen, "VEHICLE ENTRY", font_label, C_HEADING, PADDING, 85)

    # ---- Draw the three input fields ----
    labels       = ["Number Plate (e.g. AB12 ERT)",
                    "Camera 1 Time (seconds)",
                    "Camera 2 Time (seconds)"]
    placeholders = ["AB12 ERT", "e.g. 3600", "e.g. 3720"]

    for i, rect in enumerate(field_rects):
        draw_input_box(
            surface     = screen,
            rect        = rect,
            text        = fields[i],
            label       = labels[i],
            font_label  = font_small,
            font_input  = font_input,
            focused     = (focus_index == i),
            placeholder = placeholders[i],
        )

    # ---- Tab hint ----
    draw_text(screen, "Tab = next field  |  Enter = Check",
              font_small, C_LABEL, PADDING, 185)

    # ---- Draw the Check button ----
    draw_button(screen, btn_rect, "CHECK  >", font_normal, mouse_pos)

    draw_divider(screen, 200)

    # ---- Result panel ----
    if error_msg:
        # Show an error message if inputs were invalid
        draw_panel(screen, result_rect.x, result_rect.y,
                   result_rect.w, result_rect.h, colour=(60, 20, 20))
        pygame.draw.rect(screen, C_DANGER, result_rect, width=2, border_radius=8)
        draw_text(screen, "INPUT ERROR", font_verdict, C_DANGER,
                  result_rect.x + PADDING, result_rect.y + 14)
        draw_text(screen, error_msg, font_normal, C_TEXT,
                  result_rect.x + PADDING, result_rect.y + 50)

    elif result is not None:
        # Determine the border colour based on verdict
        if not result["plate_ok"]:
            panel_border = C_WARN        # amber — plate issue
        elif result["speeding"]:
            panel_border = C_DANGER      # red — speeding
        else:
            panel_border = C_SAFE        # green — all good

        draw_panel(screen, result_rect.x, result_rect.y,
                   result_rect.w, result_rect.h)
        pygame.draw.rect(screen, panel_border, result_rect, width=2, border_radius=8)

        # --- Plate validity line ---
        plate_valid_str = "VALID FORMAT" if result["plate_ok"] else "INVALID FORMAT"
        plate_col       = C_SAFE if result["plate_ok"] else C_WARN
        draw_text(screen, f"Plate: {result['plate']}", font_normal, C_TEXT,
                  result_rect.x + PADDING, result_rect.y + 14)
        draw_text(screen, plate_valid_str, font_normal, plate_col,
                  result_rect.x + 280, result_rect.y + 14)

        # --- Speed line ---
        if result["speed"] < 0:
            speed_str = "Speed: ERROR — Camera 2 time must be greater than Camera 1"
            speed_col = C_WARN
        else:
            speed_str = f"Speed: {result['speed']} mph"
            speed_col = C_DANGER if result["speeding"] else C_SAFE
        draw_text(screen, speed_str, font_normal, speed_col,
                  result_rect.x + PADDING, result_rect.y + 50)

        # --- Verdict banner ---
        if result["speed"] < 0:
            verdict_str = "INVALID TIME DATA"
            verdict_col = C_WARN
        elif result["speeding"]:
            over_by     = round(result["speed"] - SPEED_LIMIT_MPH, 2)
            verdict_str = f"SPEEDING — {over_by} mph over the limit — PENALTY NOTICE"
            verdict_col = C_DANGER
        else:
            under_by    = round(SPEED_LIMIT_MPH - result["speed"], 2)
            verdict_str = f"NOT SPEEDING — {under_by} mph under the limit"
            verdict_col = C_SAFE

        draw_text(screen, verdict_str, font_verdict, verdict_col,
                  result_rect.x + PADDING, result_rect.y + 90)

        # --- Time difference info line ---
        if result["speed"] >= 0:
            diff_s = round(result["t2"] - result["t1"], 2)   # seconds between cameras
            draw_text(screen,
                      f"Time between cameras: {diff_s} s  ({round(diff_s / 60, 2)} min)",
                      font_small, C_LABEL,
                      result_rect.x + PADDING, result_rect.y + 126)

    else:
        # No check run yet — show a prompt inside the result panel
        draw_panel(screen, result_rect.x, result_rect.y,
                   result_rect.w, result_rect.h)
        pygame.draw.rect(screen, C_BORDER, result_rect, width=2, border_radius=8)
        draw_text(screen,
                  "Enter vehicle details above and press Check to see results.",
                  font_normal, C_LABEL,
                  result_rect.x + PADDING, result_rect.y + 55)

    draw_divider(screen, LOG_Y - 10)

    # ---- Session log heading ----
    draw_text(screen, f"SESSION LOG  ({len(log_entries)} vehicles checked)",
              font_label, C_HEADING, PADDING, LOG_Y - 28)

    # ---- Draw the log panel background ----
    draw_panel(screen, LOG_X, LOG_Y, LOG_W, LOG_H, colour=C_PANEL, radius=6)

    # ---- Clip drawing to the log visible area so rows don't overflow ----
    screen.set_clip(log_clip_rect)

    visible_rows = log_clip_rect.height // LOG_ROW_H   # rows that fit in view

    if len(log_entries) == 0:
        # Nothing logged yet
        draw_text(screen, "No vehicles checked yet this session.",
                  font_small, C_LABEL, LOG_X + PADDING, LOG_Y + 10)
    else:
        # Render only the rows that are currently visible (efficiency)
        for i, entry in enumerate(log_entries[log_scroll:]):
            row_index = i   # visual row position (0 = top of log)
            if row_index >= visible_rows:
                break       # stop drawing once past the visible area

            # Alternating row background colours for readability
            row_col  = C_LOG_ROW_A if (log_scroll + i) % 2 == 0 else C_LOG_ROW_B
            row_rect = pygame.Rect(LOG_X, LOG_Y + row_index * LOG_ROW_H,
                                   LOG_W - SCROLL_W - 4, LOG_ROW_H)
            pygame.draw.rect(screen, row_col, row_rect)

            # Row number (overall position in full log, 1-indexed)
            row_num = log_scroll + i + 1
            text_y  = (LOG_Y + row_index * LOG_ROW_H
                        + (LOG_ROW_H - font_small.get_height()) // 2)

            # Plate column
            plate_col = C_TEXT if entry["plate_ok"] else C_WARN
            draw_text(screen, f"#{row_num:02d}  {entry['plate']}",
                      font_small, plate_col, LOG_X + 8, text_y)

            # Speed column
            if entry["speed"] < 0:
                speed_disp = "BAD DATA"
                s_col      = C_WARN
            else:
                speed_disp = f"{entry['speed']} mph"
                s_col      = C_DANGER if entry["speeding"] else C_SAFE
            draw_text(screen, speed_disp, font_small, s_col, LOG_X + 260, text_y)

            # Verdict column
            if entry["speed"] < 0:
                verdict_disp = "Invalid"
                v_col        = C_WARN
            elif entry["speeding"]:
                verdict_disp = "SPEEDING"
                v_col        = C_DANGER
            else:
                verdict_disp = "OK"
                v_col        = C_SAFE
            draw_text(screen, verdict_disp, font_small, v_col, LOG_X + 380, text_y)

    # ---- Remove the clip so we can draw the scrollbar outside it ----
    screen.set_clip(None)

    # ---- Draw the scrollbar ----
    scrollbar_x    = LOG_X + LOG_W - SCROLL_W        # right side of log
    scrollbar_rect = pygame.Rect(scrollbar_x, LOG_Y, SCROLL_W, LOG_H)
    pygame.draw.rect(screen, C_SCROLL_TRACK, scrollbar_rect, border_radius=4)

    if len(log_entries) > visible_rows:
        # Calculate thumb size and position proportionally
        total_rows  = len(log_entries)
        thumb_h     = max(20, int(LOG_H * visible_rows / total_rows))  # thumb height
        thumb_frac  = log_scroll / max(1, total_rows - visible_rows)   # 0 to 1
        thumb_y     = LOG_Y + int((LOG_H - thumb_h) * thumb_frac)
        thumb_rect  = pygame.Rect(scrollbar_x, thumb_y, SCROLL_W, thumb_h)
        pygame.draw.rect(screen, C_SCROLL_THUMB, thumb_rect, border_radius=4)

    # ---- Focus indicator — small dot below the active input field ----
    focused_rect = field_rects[focus_index]
    pygame.draw.circle(screen, C_BORDER_FOCUS,
                        (focused_rect.centerx, focused_rect.bottom + 6), 3)

    # ---- Flip the display buffer to screen ----
    pygame.display.flip()

    clock.tick(60)   # limit to 60 frames per second

# =============================================================================
# SHUTDOWN
# =============================================================================
pygame.quit()   # shut down all Pygame modules cleanly
sys.exit()      # exit the Python process
