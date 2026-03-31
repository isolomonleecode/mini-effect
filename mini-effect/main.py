import pygame
from constants import *
from logger import log_state

print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
print(f"Screen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    dt = 0

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        dt = clock.tick(60) / 1000     
        screen.fill("red")
        pygame.display.flip()
        

if __name__ == "__main__":
    main()
