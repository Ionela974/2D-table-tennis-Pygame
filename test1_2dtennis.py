import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Table Tennis")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

# Paddle settings
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 5

# Ball settings
BALL_SIZE = 15
BALL_SPEED_X, BALL_SPEED_Y = 5, 5

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont(None, 50)
small_font = pygame.font.SysFont(None, 30)

# Game states
MENU = 0
PLAYING = 1
PAUSED = 2
game_state = MENU

# Initialize scores
left_score, right_score = 0, 0

# Initialize game objects
left_paddle = None
right_paddle = None
ball = None

# Menu buttons
single_player_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
multiplayer_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)

# Game mode
SINGLE_PLAYER = 1
MULTIPLAYER = 2
game_mode = None

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, dy):
        if self.rect.top + dy > 0 and self.rect.bottom + dy < HEIGHT:
            self.rect.y += dy

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce off top and bottom edges
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

    def draw(self):
        pygame.draw.ellipse(screen, RED, self.rect)

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x *= random.choice((1, -1))
        self.speed_y *= random.choice((1, -1))

def handle_paddle_movement(keys, left_paddle, right_paddle):
    # Left paddle (W and S keys)
    if keys[pygame.K_w]:
        left_paddle.move(-PADDLE_SPEED)
    if keys[pygame.K_s]:
        left_paddle.move(PADDLE_SPEED)

    # Right paddle (Up and Down arrows)
    if game_mode == MULTIPLAYER:
        if keys[pygame.K_UP]:
            right_paddle.move(-PADDLE_SPEED)
        if keys[pygame.K_DOWN]:
            right_paddle.move(PADDLE_SPEED)

def check_ball_collision(ball, left_paddle, right_paddle):
    if ball.rect.colliderect(left_paddle.rect) or ball.rect.colliderect(right_paddle.rect):
        ball.speed_x *= -1  # Reverse horizontal direction

def ai_movement(ball, ai_paddle):
    if ball.rect.centery < ai_paddle.rect.centery:
        ai_paddle.move(-PADDLE_SPEED)
    elif ball.rect.centery > ai_paddle.rect.centery:
        ai_paddle.move(PADDLE_SPEED)

def display_score(left_score, right_score):
    score_text = font.render(f"{left_score} - {right_score}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - 50, 10))

def draw_menu():
    screen.fill(BLACK)
    title_text = font.render("Table Tennis", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - 100, HEIGHT // 2 - 100))

    pygame.draw.rect(screen, GRAY, single_player_button)
    single_player_text = small_font.render("Single Player", True, BLACK)
    screen.blit(single_player_text, (single_player_button.x + 30, single_player_button.y + 15))

    pygame.draw.rect(screen, GRAY, multiplayer_button)
    multiplayer_text = small_font.render("Multiplayer", True, BLACK)
    screen.blit(multiplayer_text, (multiplayer_button.x + 40, multiplayer_button.y + 15))

def reset_game():
    global left_score, right_score, left_paddle, right_paddle, ball
    left_score, right_score = 0, 0
    left_paddle = Paddle(20, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    right_paddle = Paddle(WIDTH - 30, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ball = Ball(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2)

def main():
    global game_state, left_score, right_score, left_paddle, right_paddle, ball, game_mode

    reset_game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == MENU:
                    if single_player_button.collidepoint(event.pos):
                        game_mode = SINGLE_PLAYER
                        game_state = PLAYING
                    elif multiplayer_button.collidepoint(event.pos):
                        game_mode = MULTIPLAYER
                        game_state = PLAYING

        if game_state == MENU:
            draw_menu()
        elif game_state == PLAYING:
            # Handle paddle movement
            keys = pygame.key.get_pressed()
            handle_paddle_movement(keys, left_paddle, right_paddle)

            # AI movement (for single-player mode)
            if game_mode == SINGLE_PLAYER:
                ai_movement(ball, right_paddle)

            # Move the ball
            ball.move()

            # Check for collisions
            check_ball_collision(ball, left_paddle, right_paddle)

            # Check for scoring
            if ball.rect.left <= 0:
                right_score += 1
                ball.reset()
            elif ball.rect.right >= WIDTH:
                left_score += 1
                ball.reset()

            # Check for win condition
            if left_score >= 11 and left_score >= right_score + 2:
                print("Left Player Wins!")
                reset_game()
                game_state = MENU
            elif right_score >= 11 and right_score >= left_score + 2:
                print("Right Player Wins!")
                reset_game()
                game_state = MENU

            # Clear the screen
            screen.fill(BLACK)

            # Draw paddles and ball
            left_paddle.draw()
            right_paddle.draw()
            ball.draw()

            # Display the score
            display_score(left_score, right_score)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()