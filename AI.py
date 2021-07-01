import os

import neat


class AI():
    def __init__(self):
        local_dir = os.path.dirname(__file__)
        self.config_path = os.path.join(local_dir, 'config-feedforward.txt')
        self.neat_config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                              neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                              self.config_path)

        self.pop = neat.Population(self.neat_config)
