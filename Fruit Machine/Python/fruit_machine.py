## TO FIX ##
# Buttons flicker

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 400, 300
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 24

# Define symbols
SYMBOLS = ['Cherry', 'Bell', 'Lemon', 'Orange', 'Star', 'Skull']

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.hovered = False

    def update(self, mouse_pos):
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
            self.hovered = True
        else:
            self.hovered = False

    def draw(self, screen, font):
        if self.hovered:
            pygame.draw.rect(screen, self.hover_color, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        screen.blit(text_surface, text_rect)

class FruitMachine:
    def __init__(self):
        self.credit = 1.0  # Starting credit (£1)
        self.bet_amount = 0.2  # Cost per play (£0.20)
        self.symbols = []
        self.winnings = 0

    def roll(self):
        self.credit -= self.bet_amount
        self.symbols = [random.choice(SYMBOLS) for _ in range(3)]
        self.calculate_winnings()

    def calculate_winnings(self):
        if self.symbols.count('Skull') == 3:
            self.credit = 0  # Lose all money if three skulls are rolled
        elif self.symbols.count('Skull') == 2:
            self.credit -= 0.8  # Lose £0.80 if two skulls are rolled
        elif len(set(self.symbols)) == 1:
            if self.symbols[0] == 'Bell':
                self.credit += 4.8  # Win £4.80 for three bells
            else:
                self.credit += 0.8  # Win £0.80 for three of the same symbol
        elif self.symbols[0] == self.symbols[1] or self.symbols[0] == self.symbols[2] or self.symbols[1] == self.symbols[2]:
            self.credit += 0.4  # Win £0.40 if two of the same symbol

    def display(self, screen, font):
        screen.fill(WHITE)
        for i, symbol in enumerate(self.symbols):
            text = font.render(symbol, True, BLACK)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3 + i * FONT_SIZE))
        credit_text = font.render("Balance: £{:.2f}".format(self.credit), True, BLACK)
        screen.blit(credit_text, (10, 10))
        pygame.display.flip()

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fruit Machine")

    font = pygame.font.SysFont(None, FONT_SIZE)
    fruit_machine = FruitMachine()

    spin_button = Button("Spin", 50, 200, 100, 50, (0, 255, 0), (0, 200, 0), fruit_machine.roll)
    quit_button = Button("Quit", 250, 200, 100, 50, (255, 0, 0), (200, 0, 0))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if spin_button.x < mouse_pos[0] < spin_button.x + spin_button.width and spin_button.y < mouse_pos[1] < spin_button.y + spin_button.height:
                    fruit_machine.roll()
                elif quit_button.x < mouse_pos[0] < quit_button.x + quit_button.width and quit_button.y < mouse_pos[1] < quit_button.y + quit_button.height:
                    running = False
                    pygame.quit()
                    sys.exit()

        fruit_machine.display(screen, font)

        if fruit_machine.credit <= 0:
            running = False
            pygame.quit()
            sys.exit()

        spin_button.draw(screen, font)
        quit_button.draw(screen, font)

        pygame.display.update()

if __name__ == "__main__":
    main()
