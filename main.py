import pygame
import math
import random
from pygame import mixer
import time
# main.py




pygame.init()

button_click_sound = pygame.mixer.Sound('click.mp3')  # sound when clicking

road_runner_image = pygame.image.load('beep.png')
jump_sound = pygame.mixer.Sound('cartoon_jump.mp3')

start_time = 0



# Initialize font
font = pygame.font.Font('freesansbold.ttf', 20)

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 400







#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Road Runner Game")

button_font = pygame.font.Font('freesansbold.ttf', 32)
# Function to display start screen
def show_start_screen():
    start_image = pygame.image.load("start.png")
    start_image = pygame.transform.scale(start_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(start_image, (0, 0))

    # Draw "Road Runner" text on the start screen
    font = pygame.font.Font(None, 100)
    text = font.render("Road Runner", True, (255, 0, 0))  # Red color
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(text, text_rect)

    start_button = pygame.Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 50, 160, 50)
    hover_color = (0, 200, 0)  # Color when the mouse is over the button
    default_color = (0, 255, 0)  # Default color
    current_color = default_color

    pygame.draw.rect(screen, current_color, start_button)
    start_text = button_font.render('Start', True, (0, 0, 0))
    start_text_rect = start_text.get_rect(center=start_button.center)
    screen.blit(start_text, start_text_rect)
    pygame.display.update()

    # Wait for the user to click the "Start" button
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_x, mouse_y):
                    button_click_sound.play()  # Play the sound when the start button is clicked
                    return

        # Check if the mouse is over the button
        if start_button.collidepoint(pygame.mouse.get_pos()):
            current_color = hover_color
        else:
            current_color = default_color

        pygame.draw.rect(screen, current_color, start_button)
        screen.blit(start_text, start_text_rect)
        pygame.display.update()

        pygame.time.Clock().tick(FPS)




# Display the start screen
show_start_screen()


#load image
bg = pygame.image.load("desert.png").convert()
bg_width = bg.get_width()
bg_rect = bg.get_rect()


scroll = 0
tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1

# Set up the player character
player_width, player_height = 80, 80
player_x, player_y = SCREEN_WIDTH // 2 - player_width // 2, SCREEN_HEIGHT - 2 * player_height
beep = pygame.transform.scale(road_runner_image, (player_width, player_height))
# beep = player.image
player_speed = 10
jump_height = 10
is_jumping = False
jump_count = 10
obstacle_speed = 5
brown = (139, 69, 19)

#obstacle
class Obstacle:
    def __init__(self, id,x, y, width, height):
        self.id = id
        self.rect = pygame.Rect(x, y, width, height)
        self.passed = False

    def move(self):
        self.rect.x -= obstacle_speed

    def draw(self):
        pygame.draw.rect(screen, (0, 100, 0), self.rect)  # Dark green rectangle representing the obstacle

#level
class Level:
    def __init__(self, bg_image, obstacle_speed):
        self.bg = pygame.image.load(bg_image).convert()
        self.obstacle_speed = obstacle_speed


#levels
level1 = Level("desert.png", 5)
level2 = Level("des.jpg", 7)
level3 = Level("forest.png", 10)

obstacles = []
score = 0  # Initialize the score variable
heart_loss_sound = pygame.mixer.Sound('heart.wav')


lives = 3 # starting lives of beep
previous_lives = 0

# Function to display remaining lives
def display_lives():
    global previous_lives
    heart_image = pygame.image.load("heart.png")
    heart_image = pygame.transform.scale(heart_image, (30, 30))

    total_width = lives * (heart_image.get_width() + 5)  # Adjust the spacing between hearts
    start_x = (SCREEN_WIDTH - total_width) // 2

    for i in range(lives):
        screen.blit(heart_image, (start_x + i * (heart_image.get_width() + 5), 10))
    if lives < previous_lives:
        heart_loss_sound.play()


    previous_lives = lives


current_level = level1

def display_elapsed_time(elapsed_time):
    font = pygame.font.Font('freesansbold.ttf', 20)
    time_text = font.render(f'Time: {elapsed_time} seconds', True, (255, 255, 255))
    screen.blit(time_text, (10, 40))

def game_over():
    show_game_over()
    font = pygame.font.Font('freesansbold.ttf', 32)
    pygame.display.flip()
    pygame.mixer.Sound('game_over.mp3').play()


    # Handle player's choice
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if start_over_button.collidepoint(mouse_x, mouse_y):
                    global current_level
                    current_level = level1
                    return True  # Start Over
                elif quit_button.collidepoint(mouse_x, mouse_y):
                    return False  # Quit

def spawn_obstacle():
    id = len(obstacles) + 1
    x = SCREEN_WIDTH
    height = 40
    y = 320 - height
    width = 20
    obstacles.append(Obstacle(id,x, y, width, height))

def draw_obstacles():
    global score
    for obstacle in obstacles:
        obstacle.move()
        obstacle.draw()
        # Check if the player has passed the obstacle and update the score
        if not obstacle.passed and obstacle.rect.x + obstacle.rect.width < player_x:
            obstacle.passed = True
            score += 1  # Increment the score when the player passes the obstacle

def draw_player(x, y):
    screen.blit(beep, (int(x), int(y)))

def show_game_over():
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('GAME OVER', True, (255, 255, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(text, text_rect)

    # Draw Start Over button
    global start_over_button
    start_over_button = pygame.Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 20, 160, 50)
    pygame.draw.rect(screen, (0, 255, 0), start_over_button)
    start_over_text = font.render('Start Over', True, (0, 0, 0))
    start_over_text_rect = start_over_text.get_rect(center=start_over_button.center)
    screen.blit(start_over_text, start_over_text_rect)

    # Draw Quit button
    global quit_button
    quit_button = pygame.Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 80, 160, 50)
    pygame.draw.rect(screen, (255, 0, 0), quit_button)
    quit_text = font.render('Quit', True, (0, 0, 0))
    quit_text_rect = quit_text.get_rect(center=quit_button.center)
    screen.blit(quit_text, quit_text_rect)
    display_lives()

def display_score():
    font = pygame.font.Font('freesansbold.ttf', 20)
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))












# game loop
run = True

# background music initialize
mixer.init()
mixer.music.load('Road_Runner_Theme_Song.mp3')
mixer.music.play(-1)

white = (255, 255, 255)
dark_green = (0, 100, 0)

# Initialize button rectangles outside the game loop
start_over_button = pygame.Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 20, 160, 50)
quit_button = pygame.Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 80, 160, 50)
pause_button = pygame.Rect(SCREEN_WIDTH - 60, 10, 50, 30)  # Pause button in the top-right corner






colliding_with_obstacle = False
paused = False
start_time = time.time()  # Record the start time

while run:
    elapsed_time = round(time.time() - start_time)  # Calculate the elapsed time in seconds
    clock.tick(FPS)

    # Check for mouse clicks
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    if pause_button.collidepoint(mouse_x, mouse_y) and mouse_click[0]:  # Left mouse button click
        paused = not paused
        pygame.mixer.music.pause() if paused else pygame.mixer.music.unpause()

    # Check if the game is paused
    if not paused:
        # draw scrolling background
        for i in range(0, tiles):
            # screen.blit(bg, (i * bg_width + scroll, 0))
            screen.blit(current_level.bg, (i * bg_width + scroll, 0))
            # current_level.bg = pygame.transform.scale(current_level.bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
            bg_rect.x = i * bg_width + scroll

        floor = pygame.draw.rect(screen, brown, [0, 320, SCREEN_WIDTH, 5])

        obstacle_speed = current_level.obstacle_speed

        # scroll background
        scroll -= 2

        # reset scroll
        if abs(scroll) > bg_width:
            scroll = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
            player_x += player_speed

        if not is_jumping:
            if keys[pygame.K_UP]:
                is_jumping = True
                jump_sound.play()
        else:
            if jump_count >= -10:
                neg = 1
                if jump_count < 0:
                    neg = -1
                player_y -= (jump_count ** 2) * 0.5 * neg
                jump_count -= 1
            else:
                is_jumping = False
                jump_count = 10

        if random.randint(0, 1000) < 10:
            spawn_obstacle()

        # draw obstacles
        draw_obstacles()

        # draw player
        draw_player(player_x, player_y)

        # Draw pause button in the top-right corner
        pygame.draw.rect(screen, (255, 0, 0), pause_button)
        pause_text = font.render('Pause', True, (255, 255, 255))
        pause_text_rect = pause_text.get_rect(center=pause_button.center)
        screen.blit(pause_text, pause_text_rect)

        # collision detection
        for obstacle in obstacles:
            if player_x < obstacle.rect.x + obstacle.rect.width and \
                    player_x + player_width > obstacle.rect.x and \
                    player_y < obstacle.rect.y + obstacle.rect.height and \
                    player_y + player_height > obstacle.rect.y:
                if not obstacle.passed:  # Check if this is a new collision with an obstacle not passed yet
                    obstacle.passed = True
                    lives -= 1  # Decrease lives only once per collision
                    if lives == 0:  # Check if lives are exhausted
                        if game_over():
                            obstacles.clear()
                            player_x, player_y = SCREEN_WIDTH // 2 - player_width // 2, SCREEN_HEIGHT - 2 * player_height
                            jump_count = 10
                            lives = 3
                            start_time = time.time()
                            elapsed_time = 0
                            score = 0  # Reset the score on game over
                            paused = False  # Reset pause state on game over
                            pygame.mixer.music.unpause()  # Unpause the music on game over
                        else:
                            run = False
        else:
            Obstacle.passed = False  # Reset the passed flag if not colliding with any obstacle

            # display score
        display_score()
        display_lives()
        display_elapsed_time(elapsed_time)

        # Update obstacle speed based on the score
        if score > 5:
            current_level = level2
        if score > 10:
            current_level = level3


    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
