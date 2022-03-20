"""
This is the entry point to your game.

Launch the game by running `python3 launch_game.py`
"""

from game_engine import Engine
from gui import GUI
from player import Player

game = Engine('examples/game_state_good.txt', Player, GUI)

game.run_game()


# x1 = 30
# x2 = 50
# y1 = 60
# y2 = 90
# distance = math.sqrt(math.pow(x2-x1, 2) + (math.pow(y2-y1, 2)))
# print(str(distance))
# print(str((config.radius['spaceship'] + config.radius['asteroid_small'])))
# if distance <= config.radius['spaceship'] + config.radius['asteroid_small']:
#     print('True')
# else:
#     print('False')
#
#
# x1 = 30
# x2 = 74
# y1 = 60
# y2 = 60
# distance = math.sqrt(math.pow(x2-x1, 2) + (math.pow(y2-y1, 2)))
# print(str(distance))
# print(str((config.radius['spaceship'] + config.radius['asteroid_large'])))
# if distance <= config.radius['spaceship'] + config.radius['asteroid_large']:
#     print('True')
# else:
#     print('False')
#
# x1 = 190
# x2 = 14
# y1 = 35
# y2 = 10
# distance = math.sqrt(math.pow(x2-x1, 2) + (math.pow(y2-y1, 2)))
# print(str(distance))
# print(str((config.radius['bullet'] + config.radius['asteroid_large'])))
# if distance <= config.radius['bullet'] + config.radius['asteroid_large']:
#     print('True')
# else:
#     print('False')
