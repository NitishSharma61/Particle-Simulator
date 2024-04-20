import pygame
import random
import math

# Particle 1
x1 = 125
vx1 = -50
r1 = 10
m1 = 1
c1 = (255, 255, 0)

# Particle 2
x2 = 375
vx2 = -50
r2 = 40
m2 = 100
c2 = (255, 0, 0)

# Particle 3
x3 = 250
vx3 = 50
r3 = 20
m3 = 5
c3 = (0, 0, 255)

# List of particles
particles = [(x1, vx1, r1, m1, c1), (x2, vx2, r2, m2, c2), (x3, vx3, r3, m3, c3)]

# Simulation parameters
rate = 60  # frames per second
dt = 1 / rate  # Time step between frames
space_size = 500

# Import and initialize the pygame library
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([space_size, space_size])

clock = pygame.time.Clock()

font = pygame.font.Font(None, 24)

# Sparkle parameters
sparkle_duration = 0.2  # seconds
sparkle_timer = 0

# Import and initialize the pygame.mixer module
pygame.mixer.init()

# Load collision sound effect
collision_sound = pygame.mixer.Sound('projector-button-push-6258.mp3')  

# Function to draw a star
def draw_star(surface, color, pos, size):
    angle = -math.pi / 2  # Start drawing from the top
    angle_increment = 2 * math.pi / 5  # Angle between star points
    outer_radius = size
    inner_radius = size / 2

    star_points = []
    for _ in range(5):
        outer_point = (pos[0] + outer_radius * math.cos(angle), pos[1] + outer_radius * math.sin(angle))
        inner_point = (pos[0] + inner_radius * math.cos(angle + angle_increment / 2), pos[1] + inner_radius * math.sin(angle + angle_increment / 2))
        star_points.extend([outer_point, inner_point])
        angle += angle_increment

    pygame.draw.polygon(surface, color, star_points)

# Define states
INITIAL_STATE = 0
RUNNING_STATE = 1
PAUSED_STATE = 2

# Initial state
current_state = INITIAL_STATE

# Run until the user asks to quit
running = True

# Simulation state
simulation_active = False

# Collision count
collision_count = 0

while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                if current_state == INITIAL_STATE:
                    # Start the simulation
                    current_state = RUNNING_STATE
                    simulation_active = True
                elif current_state == RUNNING_STATE:
                    # Pause the simulation
                    current_state = PAUSED_STATE
                    simulation_active = False
                elif current_state == PAUSED_STATE:
                    # Resume the simulation
                    current_state = RUNNING_STATE
                    simulation_active = True

    # Fill the background with black
    screen.fill((0, 0, 0))

    # Display FPS on the top left corner
    fps_text = font.render(f'FPS: {int(clock.get_fps())}', True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))

    if simulation_active:
        for i in range(len(particles)):
            for j in range(i + 1, len(particles)):
                x_i, vx_i, r_i, m_i, c_i = particles[i]
                x_j, vx_j, r_j, m_j, c_j = particles[j]

                # Handling particle-to-particle collisions (elastic collision)
                if abs(x_j - x_i) < (r_i + r_j):
                    v1_final = ((m_i - m_j) * vx_i + 2 * m_j * vx_j) / (m_i + m_j)
                    v2_final = (2 * m_i * vx_i + (m_j - m_i) * vx_j) / (m_i + m_j)

                    particles[i] = (x_i, v1_final, r_i, m_i, c_i)
                    particles[j] = (x_j, v2_final, r_j, m_j, c_j)

                    # Reset sparkle timer
                    sparkle_timer = sparkle_duration

                    # Increment collision count
                    collision_count += 1

                    # Play collision sound effect
                    collision_sound.play()

        for particle in particles:
            x, vx, r, _, color = particle
            pygame.draw.circle(screen, color, (int(x), 250), r)

            # Display velocity next to the particle
            velocity_text = font.render(f'{vx:.2f}', True, (255, 255, 255))
            screen.blit(velocity_text, (int(x) - r, 250 + r))

        if sparkle_timer > 0:
            # Draw sparkles during the sparkle duration
            for i in range(len(particles)):
                for j in range(i + 1, len(particles)):
                    x_i, _, r_i, _, _ = particles[i]
                    x_j, _, r_j, _, _ = particles[j]

                    # Draw star-shaped sparkle at the collision point
                    if abs(x_j - x_i) < (r_i + r_j):
                        sparkle_size = 10
                        sparkle_color = (255, 255, 255)
                        sparkle_pos = ((x_i + x_j) / 2, 250)
                        draw_star(screen, sparkle_color, sparkle_pos, sparkle_size)

            # Decrement the sparkle timer
            sparkle_timer -= dt

        # Display collision count in the top right corner
        collision_text = font.render(f'Collisions: {collision_count}', True, (255, 255, 255))
        screen.blit(collision_text, (space_size - 150, 10))

        for i in range(len(particles)):
            x, vx, _, _, _ = particles[i]

            # Handling wall collisions for particles
            if (x - particles[i][2]) < 0 or (x + particles[i][2]) > space_size:
                particles[i] = (x, -vx, particles[i][2], particles[i][3], particles[i][4])

        # Dynamics for particles
        for i in range(len(particles)):
            x, vx, _, _, _ = particles[i]
            particles[i] = (x + vx * dt, vx, particles[i][2], particles[i][3], particles[i][4])

    # Display different messages based on the current state
    if current_state == INITIAL_STATE:
        message_text = font.render('Press SPACE to Start', True, (255, 255, 255))
        screen.blit(message_text, (space_size // 2 - 100, space_size // 2))
    elif current_state == PAUSED_STATE:
        message_text = font.render('PAUSED - Press SPACE to Resume', True, (255, 255, 255))
        screen.blit(message_text, (space_size // 2 - 200, space_size // 2))

    # Flip the display
    pygame.display.flip()

    # Limit frame rate to the desired number of frames per second
    clock.tick(rate)

# Done! Time to quit.
pygame.quit()
