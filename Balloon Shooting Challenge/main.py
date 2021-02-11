import pygame
import os
import random
pygame.font.init()

WIDTH, HEIGHT = 600, 500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Balloon Shooting Challenge")

LIGHT_BLUE = (0,120,255)
BLACK = (0,0,0)
WHITE = (255,255,255)

FPS = 60
VEL = 5

# Ensures that the bullet speed is 1.5 times that of the balloon speed
BALLOON_VEL = 3
BULLET_VEL = BALLOON_VEL * 1.5

# Used to ensure that only one bullet at a time can be fired
MAX_BULLETS = 1

MISSED_SHOTS = 0
END_FONT = pygame.font.SysFont('comicsans', 40)

CANNON_WIDTH, CANNON_HEIGHT = 100, 50
BALLOON_WIDTH, BALLOON_HEIGHT = 80,90

# Preload images for quicker use
CANNON_IMAGE = pygame.image.load(os.path.join('Assets', 'Cannon.png'))
CANNON = pygame.transform.scale(CANNON_IMAGE, (CANNON_WIDTH, CANNON_HEIGHT))

BALLOON_IMAGE = pygame.image.load(os.path.join('Assets', 'Balloon.png'))
BALLOON = pygame.transform.scale(BALLOON_IMAGE, (BALLOON_WIDTH, BALLOON_HEIGHT))

POP_IMAGE = pygame.image.load(os.path.join('Assets', 'Pop.png'))
POP = pygame.transform.scale(POP_IMAGE, (BALLOON_WIDTH + 50, BALLOON_HEIGHT + 50))

BALLOON_HIT = pygame.USEREVENT + 1

def draw_window(cannon, balloon, bullets):
    WIN.fill(LIGHT_BLUE)

    WIN.blit(CANNON, (cannon.x, cannon.y))
    WIN.blit(BALLOON, (balloon.x, balloon.y))

    for bullet in bullets:
        pygame.draw.rect(WIN, BLACK, bullet)

    pygame.display.update()

def handle_cannon_movement(keys_pressed, cannon):
    if keys_pressed[pygame.K_UP] and cannon.y - VEL > 0:
        cannon.y -= VEL
    if keys_pressed[pygame.K_DOWN] and cannon.y + VEL + cannon.height < HEIGHT:
        cannon.y += VEL

def handle_bullets(bullets, cannon, balloon):
    #global MISSED_SHOTS

    for bullet in bullets:
        global MISSED_SHOTS
        bullet.x -= BULLET_VEL
        if balloon.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BALLOON_HIT))
            bullets.remove(bullet)
        elif bullet.x < 0:
            bullets.remove(bullet)
            MISSED_SHOTS += 1

def handle_balloon_movement(balloon):
    global BALLOON_VEL

    balloon.y += BALLOON_VEL

    if balloon.y < 0:
        BALLOON_VEL = -BALLOON_VEL
    elif balloon.y + balloon.height > HEIGHT :
        BALLOON_VEL = -BALLOON_VEL
    else:
        # Randomises the direction the balloon travels
        n = random.randint(0,10)
        if n >= 9:
            BALLOON_VEL = -BALLOON_VEL

def draw_end(text):
    global MISSED_SHOTS
    draw_text = END_FONT.render(text,1,WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    # Resets missed shots for next playthrough
    MISSED_SHOTS = 0
    pygame.time.delay(5000)


def main():

    cannon = pygame.Rect(500,HEIGHT//2 - CANNON_HEIGHT//2, CANNON_WIDTH, CANNON_HEIGHT)
    balloon = pygame.Rect(0, HEIGHT//2 - BALLOON_HEIGHT//2, BALLOON_WIDTH, BALLOON_HEIGHT)

    bullets = []

    clock = pygame.time.Clock()

    end_text = ""

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(cannon.x, cannon.y + cannon.height//2 - 2, 10, 5)
                    bullets.append(bullet)

            if event.type == BALLOON_HIT:
                end_text = "GAME OVER, Missed Shots: " + str(MISSED_SHOTS) #Displays how many missed shots there were
                WIN.blit(POP, (balloon.x - 20,balloon.y - 20))
                draw_end(end_text)
                break

        keys_pressed = pygame.key.get_pressed()
        # Splits different requirements into seperate functions
        handle_cannon_movement(keys_pressed, cannon)
        handle_bullets(bullets, cannon, balloon)
        handle_balloon_movement(balloon)

        draw_window(cannon, balloon, bullets)

    main()

# Makes sure that this function is called directly from this file
# not if this file was imported from somwhere else
if __name__ == "__main__":
    main()