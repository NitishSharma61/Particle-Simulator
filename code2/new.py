import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Moving, Shrinking, and Expanding Rectangle")

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up rectangle parameters
rect_size = 100
rect_x = width // 2 - rect_size // 2           # centered horizontally
rect_y = height // 2 - rect_size // 2          # centered vertically
speed = 5
expansion_rate = 2

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move the rectangle left and right
    rect_x += speed
    if rect_x + rect_size > width or rect_x < 0:
        speed = -speed  # Reverse direction when reaching the screen edge

    # Shrink and expand the rectangle
    rect_size -= expansion_rate
    if rect_size < 10 or rect_size > 100:
        expansion_rate = -expansion_rate  # Reverse expansion direction

    # Clear the screen
    screen.fill(BLACK)

    # Draw the rectangle
    pygame.draw.rect(screen, WHITE, (rect_x, rect_y, rect_size, rect_size))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)