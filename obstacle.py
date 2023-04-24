import pygame
import random

class Obstacle:
    def __init__(self, position, upper_height, lower_height, hole_size, width):
        self.position = position
        self.upper_height = upper_height
        self.lower_height = lower_height
        self.hole_size = hole_size
        self.width = width
        self.color = (0, 128, 0)
    
    @classmethod
    def make_random(cls, screen_width, screen_height):
        width = screen_width / 8
        hole_size = random.randint(int(screen_height * 0.22), int(screen_height * 0.70))
        h2 = random.randint(int(screen_height * 0.15), int(screen_height * 0.75))
        h1 = screen_height - h2 - hole_size
        return cls(upper_height=h1, lower_height=h2, hole_size=hole_size, position=screen_width, width=width)
    
    def move(self, speed):
        self.position -= speed

    def is_visible(self):
        return self.position + self.width >= 0
    
    def collides_with_circle(self, center, radius):
        (x, y) = center
        y1 = self.upper_height
        y2 = self.upper_height + self.hole_size
        p = self.position
        q = self.position + self.width

        if x - radius > q or x + radius < p:
            return False
        
        if y1 > y - radius or y2 < y + radius:
            return True
        
        return False
    
    def render(self, screen):
        x = self.position
        uy = 0
        uh = self.upper_height
        pygame.draw.rect(screen, self.color, (x, uy, self.width, uh))
        ly = screen.get_height() - self.lower_height
        lh = self.lower_height
        pygame.draw.rect(screen, self.color, (x, ly, self.width, lh))