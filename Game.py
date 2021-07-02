import pygame

bg_img = pygame.image.load("assets/Map.png")

win_width = 1900
win_heigth = 1000
backround = pygame.image.load("assets/Map.png")
WIN = pygame.display.set_mode((win_width, win_heigth))

class game():
    def __init__(self):
        pass

def run():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        window = WIN
        window.blit(backround, [0, 0])

        pygame.display.flip()
        clock.tick(0)

