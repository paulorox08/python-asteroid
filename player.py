import math
import config

class Player:
    def __init__(self):
        # Enter your code here
        self.target = None
        self.closest_distance = 0
        self.shoot_count = 0

    def action(self, spaceship, asteroid_ls, bullet_ls, fuel, score):
        # Enter your code here
        thrust = False
        bullet = False
        left = False
        right = False

        self.closest_distance = 950
        self.shoot_count += 1

        # Find the closest object
        for asteroid in asteroid_ls:
            distance = math.sqrt(math.pow(spaceship.x - asteroid.x, 2) + (math.pow(spaceship.y - asteroid.y, 2)))
            if distance < self.closest_distance:
                self.closest_distance = distance
                self.target = asteroid


        # Target angle Calculate
        delta_y = self.target.y - spaceship.y
        delta_x = self.target.x - spaceship.x
        if delta_x > 0 and delta_y < 0:
            target_angle = math.degrees(abs(math.atan(delta_y/delta_x)))
        if delta_x < 0 and delta_y < 0:
            target_angle = 180 - math.degrees(abs(math.atan(delta_y/delta_x)))
        if delta_x < 0 and delta_y > 0:
            target_angle = 180 + math.degrees(abs(math.atan(delta_y/delta_x)))
        if delta_x > 0 and delta_y > 0:
            target_angle = 360 - math.degrees(abs(math.atan(delta_y/delta_x)))
        if delta_x == 0 and delta_y < 0:
            target_angle = 90
        if delta_x < 0 and delta_y == 0:
            target_angle = 180
        if delta_x == 0 and delta_y > 0:
            target_angle = 270
        if delta_x > 0 and delta_y == 0:
            target_angle = 0

        #rotate spaceship AI
        if spaceship.angle < target_angle:
            if (target_angle - spaceship.angle) < (spaceship.angle + abs(target_angle - 360)):
                left = True
                right = False
            else:
                left = False
                right = True
        if spaceship.angle > target_angle:
            if (spaceship.angle - target_angle) < (abs(spaceship.angle - 360) + target_angle):
                right = True
                left = False
            else:
                right = False
                left = True

        # not turning if facing to the target already
        if abs(spaceship.angle - target_angle) < 10:
            right = False
            left = False

        # if distance < 120, shoot AI
        if self.closest_distance < 120:
            if abs(spaceship.angle - abs(target_angle)) < 20:
                if self.shoot_count > 3:
                    bullet = True
                    self.shoot_count = 0
            else:
                bullet = False
            thrust = False
        if self.closest_distance < 50:
            if abs(spaceship.angle - abs(target_angle)) < 90:
                bullet = True

        # if distance > 120, thurst AI
        if self.closest_distance > 120:
            bullet = False
            thrust = True


        return (thrust, left, right, bullet)

    # You can add additional methods if required