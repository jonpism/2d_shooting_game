import pygame
import os  # defines a path to the content we want to use in the game (such as images)
import random

pygame.mixer.init()
pygame.font.init()

WIDTH, HEIGHT = 1600, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # WIN = WINDOW
pygame.display.set_caption("2d shooting game")  # names the popup game window (up left)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (211, 211, 211)

BORDER_LINE = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('woo', 40)
WINNER_FONT = pygame.font.SysFont('woo', 100)

FPS = 60
VELOCITY = 5
BULLET_VELOCITY = 8
MAX_BULLETS = 10

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'hit_sound.mp3'))
BULLET_HIT_SOUND2 = pygame.mixer.Sound(os.path.join('Assets', 'hit_sound2.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'fire_shot.mp3'))

CHARACTER_WIDTH = 85
CHARACTER_HEIGHT = 85

# unique events
BOB_HIT = pygame.USEREVENT + 1
RIO_HIT = pygame.USEREVENT + 2

HUNTER_IMAGE = pygame.image.load(os.path.join('Assets', 'hunter.png'))
# scaling (width ,length)
HUNTER = pygame.transform.scale(HUNTER_IMAGE, (CHARACTER_WIDTH, CHARACTER_HEIGHT))

GUNSLINGER_IMAGE = pygame.image.load(os.path.join('Assets', 'gunslinger.png'))
GUNSLINGER = pygame.transform.scale(GUNSLINGER_IMAGE, (CHARACTER_WIDTH, CHARACTER_HEIGHT))


def draw_window(bob, rio, bob_bullets, rio_bullets, rio_health, bob_health):
    WIN.fill(WHITE)  # fills the window with a specific color (RGB and values are: from 0 to 255)
    pygame.draw.rect(WIN, GREY, BORDER_LINE)

    rio_health_appear = HEALTH_FONT.render("Health: " + str(rio_health), 1, BLACK)
    bob_health_appear = HEALTH_FONT.render("Health: " + str(bob_health), 1, BLACK)
    WIN.blit(rio_health_appear, (WIDTH - rio_health_appear.get_width() - 10, 10))  # 10 = pixels
    WIN.blit(bob_health_appear, (10, 10))

    WIN.blit(HUNTER, (rio.x, rio.y))  # blit to put sth on the window (x,y) = coordinates
    WIN.blit(GUNSLINGER, (bob.x, bob.y))

    for bullet in rio_bullets:
        pygame.draw.rect(WIN, BLACK, bullet)

    for bullet in bob_bullets:
        pygame.draw.rect(WIN, BLACK, bullet)

    pygame.display.update()  # updates the window


def bob_movement(keys_pressed, bob):
    if keys_pressed[pygame.K_a] and bob.x - VELOCITY > 0:  # moves left, in rectangle range of course
        bob.x -= VELOCITY
    if keys_pressed[pygame.K_d] and bob.x + VELOCITY + bob.width < BORDER_LINE.x:  # moves right, --||--
        bob.x += VELOCITY
    if keys_pressed[pygame.K_w] and bob.y - VELOCITY > 0:  # moves up, --||--
        bob.y -= VELOCITY
    if keys_pressed[pygame.K_s] and bob.y + VELOCITY + bob.height < HEIGHT:  # moves down, --||--
        bob.y += VELOCITY


def rio_movement(keys_pressed, rio):
    if keys_pressed[pygame.K_LEFT] and rio.x - VELOCITY > BORDER_LINE.x + 5:  # moves left, in rectangle range of course
        rio.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and rio.x + VELOCITY + rio.width < WIDTH:  # moves right, --||--
        rio.x += VELOCITY
    if keys_pressed[pygame.K_UP] and rio.y - VELOCITY > 0:  # moves up, --||--
        rio.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and rio.y + VELOCITY + rio.height < HEIGHT:  # moves down, --||--
        rio.y += VELOCITY


def handle_bullets(bob_bullets, rio_bullets, bob, rio):
    for bullet in bob_bullets:
        bullet.x += BULLET_VELOCITY
        if rio.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RIO_HIT))
            bob_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            bob_bullets.remove(bullet)

    for bullet in rio_bullets:
        bullet.x -= BULLET_VELOCITY
        if bob.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BOB_HIT))
            rio_bullets.remove(bullet)
        elif bullet.x < 0:
            rio_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, BLACK)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    bob = pygame.Rect(random.randint(0, 700), random.randint(0, 700)
                      , CHARACTER_WIDTH, CHARACTER_HEIGHT)  # bob == GUNSLINGER
    rio = pygame.Rect(random.randint(820, 1450), random.randint(0, 700)
                      , CHARACTER_WIDTH, CHARACTER_HEIGHT)  # rio == HUNTER

    bob_bullets = []
    rio_bullets = []

    bob_health = 10
    rio_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:  # quit event (quits the game)
        clock.tick(FPS)  # 60 frames per second, makes the game controllable
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(bob_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(bob.x + bob.width, bob.y + bob.height // 2 - 2, 10, 5)
                    bob_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(rio_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(rio.x, rio.y + rio.height // 2 - 2, 10, 5)
                    rio_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RIO_HIT:
                rio_health -= 1
                BULLET_HIT_SOUND2.play()
            if event.type == BOB_HIT:
                bob_health -= 1
                BULLET_HIT_SOUND.play()

        winner = ""
        if rio_health <= 0:
            winner = "BOB WINS!!!"

        if bob_health <= 0:
            winner = "RIO WINS!!!"

        if winner != "":
            draw_winner(winner)  # someone won
            break

        keys_pressed = pygame.key.get_pressed()
        bob_movement(keys_pressed, bob)
        rio_movement(keys_pressed, rio)

        handle_bullets(bob_bullets, rio_bullets, bob, rio)

        draw_window(bob, rio, rio_bullets, bob_bullets, rio_health, bob_health)
    main()


if __name__ == "__main__":
    main()
