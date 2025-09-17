import pygame
import random
import time

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
DARK_GRAY = (40, 40, 40)
YELLOW = (255, 255, 0)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Snake Game")

# Clock
clock = pygame.time.Clock()
FPS = 15

# Fonts
font_large = pygame.font.SysFont("comicsansms", 60)
font_small = pygame.font.SysFont("comicsansms", 35)


def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, DARK_GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, DARK_GRAY, (0, y), (WIDTH, y))


def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, BLUE, (*segment, CELL_SIZE, CELL_SIZE), 2)  # Border


def draw_food(food):
    pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))


def show_score(score):
    text = font_small.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))


def countdown():
    for i in range(3, 0, -1):
        screen.fill(BLACK)
        text = font_large.render(f"{i}", True, YELLOW)
        screen.blit(text, (WIDTH // 2 - 30, HEIGHT // 2 - 50))
        pygame.display.update()
        time.sleep(1)


def game_loop():
    snake = [(WIDTH // 2, HEIGHT // 2)]
    snake_dir = (0, -CELL_SIZE)
    food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
    score = 0
    running = True

    while running:
        screen.fill(BLACK)
        draw_grid()
        draw_snake(snake)
        draw_food(food)
        show_score(score)
        pygame.display.update()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_dir != (0, CELL_SIZE):
                    snake_dir = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and snake_dir != (0, -CELL_SIZE):
                    snake_dir = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and snake_dir != (CELL_SIZE, 0):
                    snake_dir = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and snake_dir != (-CELL_SIZE, 0):
                    snake_dir = (CELL_SIZE, 0)

        # Move snake
        new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
        snake.insert(0, new_head)

        # Check food collision
        if snake[0] == food:
            score += 1
            food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
        else:
            snake.pop()

        # Check collisions
        if (
            new_head[0] < 0 or new_head[0] >= WIDTH
            or new_head[1] < 0 or new_head[1] >= HEIGHT
            or new_head in snake[1:]
        ):
            running = False

        clock.tick(FPS)

    return score  # Return score when game ends


def end_menu(score):
    while True:
        screen.fill(BLACK)
        text_game_over = font_large.render("Game Over!", True, RED)
        text_score = font_small.render(f"Your Score: {score}", True, WHITE)
        text_play_again = font_small.render("Press P to Play Again", True, GREEN)
        text_quit = font_small.render("Press Q to Quit", True, RED)

        screen.blit(text_game_over, (WIDTH // 2 - 150, HEIGHT // 2 - 120))
        screen.blit(text_score, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        screen.blit(text_play_again, (WIDTH // 2 - 150, HEIGHT // 2 + 20))
        screen.blit(text_quit, (WIDTH // 2 - 100, HEIGHT // 2 + 70))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return True
                elif event.key == pygame.K_q:
                    return False


# Main program
while True:
    countdown()
    final_score = game_loop()
    play_again = end_menu(final_score)
    if not play_again:
        break

pygame.quit()
print("Thanks for playing! 🐍")
