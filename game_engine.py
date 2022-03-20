import time

import config
from space_object import SpaceObject

class Engine:
    def __init__(self, game_state_filename, player_class, gui_class):
        self.asteroid_ls = []
        self.bullet_ls = []
        self.upcoming_asteroid_ls = []
        self.begin_fuel = 0
        self.warning_fuel_75 = True
        self.warning_fuel_50 = True
        self.warning_fuel_25 = True
        self.log = []

        self.import_state(game_state_filename)
        self.player = player_class()
        self.GUI = gui_class(self.width, self.height)

    def import_state(self, game_state_filename):
        try:
            with open(game_state_filename) as file:
                line_number = 1
                for line in file.readlines():
                    line = line.strip()
                    if line == '':
                        print('Error: expecting a key and value in line ' + str(line_number))
                        exit(1)
                    elif line.split(' ')[0] == 'width':
                        self.width = int(line.split(' ')[1])
                    elif line.split(' ')[0] == 'height':
                        self.height = int(line.split(' ')[1])
                    elif line.split(' ')[0] == 'score':
                        self.score = int(line.split(' ')[1])
                    elif line.split(' ')[0] == 'spaceship':
                        split_data = line.split(' ')[1].split(',')
                        self.spaceship = SpaceObject(split_data[0], split_data[1], config.radius['spaceship'],
                                                     config.radius['spaceship']
                                                     , split_data[2], 'spaceship', split_data[3])
                    elif line.split(' ')[0] == 'fuel':
                        self.fuel = int(line.split(' ')[1])
                        self.begin_fuel = int(line.split(' ')[1])
                    elif line.split(' ')[0] == 'asteroids_count':
                        self.asteroids_count = int(line.split(' ')[1])
                    elif line.split(' ')[0] == 'asteroid_small':
                        split_data = line.split(' ')[1].split(',')
                        asteroid_small = SpaceObject(split_data[0], split_data[1], config.radius['asteroid_small'],
                                                     config.radius['asteroid_small']
                                                     , split_data[2], 'asteroid_small', split_data[3])
                        self.asteroid_ls.append(asteroid_small)
                    elif line.split(' ')[0] == 'asteroid_large':
                        split_data = line.split(' ')[1].split(',')
                        asteroid_large = SpaceObject(split_data[0], split_data[1], config.radius['asteroid_large'],
                                                     config.radius['asteroid_large']
                                                     , split_data[2], 'asteroid_large', split_data[3])
                        self.asteroid_ls.append(asteroid_large)
                    elif line.split(' ')[0] == 'bullets_count':
                        self.bullets_count = line.split(' ')[1]
                    elif line.split(' ')[0] == 'upcoming_asteroids_count':
                        self.upcoming_asteroids_count = line.split(' ')[1]
                    elif line.split(' ')[0] == 'upcoming_asteroid_large':
                        split_data = line.split(' ')[1].split(',')
                        upcoming_asteroid_large = SpaceObject(split_data[0], split_data[1],
                                                              config.radius['asteroid_large'],
                                                              config.radius['asteroid_large']
                                                              , split_data[2], 'asteroid_large', split_data[3])
                        self.upcoming_asteroid_ls.append(upcoming_asteroid_large)
                    elif line.split(' ')[0] == 'upcoming_asteroid_small':
                        split_data = line.split(' ')[1].split(',')
                        upcoming_asteroid_small = SpaceObject(split_data[0], split_data[1],
                                                              config.radius['asteroid_small'],
                                                              config.radius['asteroid_small']
                                                              , split_data[2], 'asteroid_small', split_data[3])
                        self.upcoming_asteroid_ls.append(upcoming_asteroid_small)
                    else:
                        print("Error: unexpected key: " + line + " in line " + str(line_number))
                        exit(1)
                    line_number += 1

        except Exception as ex:
            if ex.args[0] == 'list index out of range':
                print('Error: Incomplete file, please check the input file again! Please check data in line: ' + str(line_number))
            elif 'No such file or directory' in ex.args[1]:
                print('FileNotFoundError(Error: unable to open ' + ex.filename +')')
            else:
                print('Error:', ex)
            exit(1)

    def export_state(self, game_state_filename):
        # Enter your code here
        f = open(game_state_filename, "w")
        f.write("Frame <id> :: spaceship_pos :: asteroid_pos_ls :: bullet_pos_ls :: fuel :: score")
        for item in self.log:
            f.write(item +'\n')
        f.close()

    def run_game(self):
        bullet_ID = 0
        frame_ID = 0
        while True:
            time.sleep(config.frame_delay)
            # 1. Receive player input
            current_player_action = self.player.action(self.spaceship, self.asteroid_ls, self.bullet_ls, self.fuel,
                                                       self.score)
            # 2. Process game logic
            self.log.append('Frame ' + str(frame_ID) + ' :: ' +
                            str(self.spaceship) + ' :: ' + str(self.asteroid_ls) + ' :: ' + str(self.bullet_ls) + ' :: ' + str(self.fuel) + ' :: ' + str(self.score))

            self.fuel -= config.spaceship_fuel_consumption

            # Turing handle - High priority than thruster
            if current_player_action[1] == True and current_player_action[2] == True:
                pass
            else:
                if current_player_action[1] == True:
                    self.spaceship.turn_left()
                elif current_player_action[2] == True:
                    self.spaceship.turn_right()

            # Thruster handle
            if current_player_action[0] == True:
                self.spaceship.move_forward()

            # Bullet shoot handle
            if current_player_action[3] == True:
                if self.fuel >= config.shoot_fuel_threshold:
                    bullet = SpaceObject(self.spaceship.x, self.spaceship.y, config.radius['bullet'],
                                         config.radius['bullet'], self.spaceship.angle, 'bullet', bullet_ID)
                    self.bullet_ls.append(bullet)
                    self.fuel -= config.bullet_fuel_consumption
                    bullet_ID += 1
                else:
                    print('Cannot shoot due to low fuel')
                    self.log.append('Cannot shoot due to low fuel')

            # Asteroid list handle
            for asteroid in self.asteroid_ls:
                asteroid.move_forward()

            # Bullet list handle
            for bullet in self.bullet_ls:
                # Bullet live 5 Frame
                if bullet.range < config.bullet_move_count:
                    bullet.move_forward()
                    bullet.range += 1
                else:
                    self.bullet_ls.remove(bullet)

            # Collide handle
            # Bullet collide Asteroid
            for asteroid in self.asteroid_ls:
                for bullet in self.bullet_ls:
                    if bullet.collide_with(asteroid) and asteroid.collide_with(bullet):
                        if asteroid.obj_type == 'asteroid_small':
                            self.score += int(config.shoot_small_ast_score)
                        if asteroid.obj_type == 'asteroid_large':
                            self.score += int(config.shoot_large_ast_score)
                        self.bullet_ls.remove(bullet)
                        self.asteroid_ls.remove(asteroid)
                        if len(self.upcoming_asteroid_ls) > 0:
                            upcoming_asteroid = self.upcoming_asteroid_ls.pop(0)
                            self.asteroid_ls.append(upcoming_asteroid)
                            print('Added asteroid ' + str(upcoming_asteroid.id))
                            self.log.append('Added asteroid ' + str(upcoming_asteroid.id))
                        else:
                            print('Error: no more asteroids available and end the game.')
                            self.log.append('Error: no more asteroids available and end the game.')
                        print('Score: ' + str(self.score) + '\t [Bullet ' + str(bullet.id) +
                              ' has shot ateroid ' + str(asteroid.id) +']')
                        break



            # Asteroid collide Spaceship
            for asteroid in self.asteroid_ls:
                if self.spaceship.collide_with(asteroid) and asteroid.collide_with(self.spaceship):
                    self.score += config.collide_score
                    self.asteroid_ls.remove(asteroid)
                    if len(self.upcoming_asteroid_ls) > 0:
                        upcoming_asteroid = self.upcoming_asteroid_ls.pop(0)
                        self.asteroid_ls.append(upcoming_asteroid)
                        print('Added asteroid ' + str(upcoming_asteroid.id))
                        self.log.append('Added asteroid ' + str(upcoming_asteroid.id))
                    else:
                        print('Error: no more asteroids available and end the game.')
                        self.log.append('Error: no more asteroids available and end the game.')
                    print('Score: ' + str(self.score) + '\t [Spaceship collided with asteroid ' + str(asteroid.id) + ']')
                    self.log.append('Score: ' + str(self.score) + '\t [Spaceship collided with asteroid ' + str(asteroid.id) + ']')

            # Warning Fuel 75% 50% 25%
            if self.fuel / self.begin_fuel <= 0.75 and self.warning_fuel_75 == True:
                print('75% fuel warning: ' + str(self.fuel) + ' remaining')
                self.log.append('75% fuel warning: ' + str(self.fuel) + ' remaining')
                self.warning_fuel_75 = False
            if self.fuel / self.begin_fuel <= 0.5 and self.warning_fuel_50 == True:
                print('50% fuel warning: ' + str(self.fuel) + ' remaining')
                self.log.append('50% fuel warning: ' + str(self.fuel) + ' remaining')
                self.warning_fuel_50 = False
            if self.fuel / self.begin_fuel <= 0.25 and self.warning_fuel_25 == True:
                print('25% fuel warning: ' + str(self.fuel) + ' remaining')
                self.log.append('25% fuel warning: ' + str(self.fuel) + ' remaining')
                self.warning_fuel_25 = False

            frame_ID += 1
            # 3. Draw the game state on screen using the GUI class
            self.GUI.update_frame(self.spaceship,self.asteroid_ls,self.bullet_ls,self.score,self.fuel)

            # Game loop should stop when:
            # - the spaceship runs out of fuel, or
            if self.fuel <= 0:
                print('You lose')
                self.export_state('output.out')
                self.GUI.finish(self.score)
                break
            # - no more asteroids are available
            if len(self.asteroid_ls) <= 0:
                print('You win')
                print('Fuel left: ' + str(self.fuel))
                self.export_state('output.out')
                self.GUI.finish(self.score)
                break

        # Display final score
        self.GUI.finish(self.score)


    # You can add additional methods if required
