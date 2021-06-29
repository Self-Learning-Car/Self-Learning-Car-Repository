
from GameEnv import GameEnv
import random

SCREEN_WIDTH = 1900
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Self Learning Car"

if __name__ == '__main__':
    #game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    env = GameEnv()
    #env.init_render()
    while not env.done:
        action=random.randrange(1,7)
        env.step(action)
        env.render()



