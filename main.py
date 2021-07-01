import os

import Game



if __name__ == '__main__':
   local_dir = os.path.dirname(__file__)
   config_path = os.path.join(local_dir, 'config_feedforward.txt')
   Game.run(config_path)



