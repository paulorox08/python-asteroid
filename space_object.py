import math
import config

class SpaceObject:
    def __init__(self, x, y, width, height, angle, obj_type, id):
        # Enter your code here
        self.x = float(x)
        self.y = float(y)
        self.width = int(width)
        self.height = int(height)
        self.angle = int(angle)
        self.obj_type = obj_type
        self.id = int(id)
        if obj_type == 'spaceship':
            self.radius = config.radius['spaceship']
            self.speed = config.speed['spaceship']
        if obj_type == 'bullet':
            self.radius = config.radius['bullet']
            self.speed = config.speed['bullet']
            self.range = 0
        if obj_type == 'asteroid_small':
            self.radius = config.radius['asteroid_small']
            self.speed = config.speed['asteroid_small']
        if obj_type == 'asteroid_large':
            self.radius = config.radius['asteroid_large']
            self.speed = config.speed['asteroid_large']
        pass

    def turn_left(self):
        # Enter your code here
        if self.obj_type == 'spaceship':
            self.angle += config.angle_increment
        if self.angle > 360:
            self.angle = 15

    def turn_right(self):
        # Enter your code here
        if self.obj_type == 'spaceship':
            self.angle -= config.angle_increment
        if self.angle < 0:
            self.angle = 345


    def move_forward(self):
        if self.obj_type == 'spaceship':
            self.x += config.speed['spaceship'] * math.cos(math.radians(self.angle ))
            self.y -= config.speed['spaceship'] * math.sin(math.radians(self.angle ))
        if self.obj_type == 'bullet':
            self.x += config.speed['bullet'] * math.cos(math.radians(self.angle ))
            self.y -= config.speed['bullet'] * math.sin(math.radians(self.angle ))
        if self.obj_type == 'asteroid_small':
            self.x += config.speed['asteroid_small'] * math.cos(math.radians(self.angle))
            self.y -= config.speed['asteroid_small'] * math.sin(math.radians(self.angle))
        if self.obj_type == 'asteroid_large':
            self.x += config.speed['asteroid_large'] * math.cos(math.radians(self.angle))
            self.y -= config.speed['asteroid_large'] * math.sin(math.radians(self.angle))
        if self.x < 0:
            self.y = self.y
            self.x = 900
        if self.x > 900:
            self.y = self.y
            self.x = 0
        if self.y < 0:
            self.x = self.x
            self.y = 600
        if self.y > 600:
            self.x = self.x
            self.y = 0

    def get_xy(self):
        # Enter your code here
        return (self.x,self.y)

    def collide_with(self, other):
        distance = math.sqrt(math.pow(self.x - other.x, 2) + (math.pow(self.y - other.y, 2)))
        if other.obj_type == 'asteroid_small':
            if distance <= (config.radius['asteroid_small'] + self.radius):
                return True
            else :
                return False
        if other.obj_type == 'asteroid_large':
            if distance <= (config.radius['asteroid_large'] + self.radius):
                return True
            else :
                return False
        if other.obj_type == 'bullet':
            if distance <= (config.radius['bullet'] + self.radius):
                return True
            else :
                return False
        if other.obj_type == 'spaceship':
            if distance <= (config.radius['spaceship'] + self.radius):
                return True
            else :
                return False

    def __repr__(self):
        # Enter your code here
        return self.obj_type + ' ' + str(round(self.x,1)) + ',' + str(round(self.y,1)) + ',' + str(self.angle) + ',' + str(self.id)

    # You can add additional methods if required
