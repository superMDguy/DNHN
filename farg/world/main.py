import random

import pygame
from pygame.locals import *


class Interaction:

    def __init__(self, size=(1280, 820)):
        (self.width, self.height) = size
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(
            'Deep Neural Hofstadter Networks | Interact!')
        self.screen.fill((255, 255, 255))

        self.clock = pygame.time.Clock()

        self.FONT_SIZE = 50
        self.textArea = pygame.Rect(
            0, self.height - self.FONT_SIZE, self.width, self.FONT_SIZE)
        self.buffer = ""  # Text buffer

        pygame.display.flip()

    def loop(self):
        pygame.init()
        self.buffer = ""
        font = pygame.font.Font(None, self.FONT_SIZE)
        while True:
            self.clock.tick(20)  # set max fps to 20
            for evt in pygame.event.get():
                if evt.type == KEYDOWN:
                    if evt.unicode.isprintable():
                        self.buffer += evt.unicode
                    elif evt.key == K_BACKSPACE:
                        self.buffer = self.buffer[:-1]
                    elif evt.key == K_RETURN:
                        # TODO: Send current buffer up to bot
                        print(self.buffer)
                        self.buffer = ""
                elif evt.type == QUIT:
                    return
            self.screen.fill((0, 0, 0), self.textArea)
            block = font.render(self.buffer, True, (150, 150, 150))
            rect = block.get_rect()
            rect.center = self.screen.get_rect().center
            self.screen.blit(block, self.textArea)
            pygame.display.flip()

    def addCircle(self, color, center, radius):
        color = pygame.color.THECOLORS[color]  # color is a string this way
        pygame.draw.circle(self.screen, color, center,
                           radius)
        pygame.display.flip()

    def addPolygon(self, color, pointlist):
        color = pygame.color.THECOLORS[color]
        pygame.draw.polygon(self.screen, color, pointlist)

    def addRandomPolygons(self, number=5, MAX_SIDES=6):
        for i in range(number):
            pointlist = []
            color = (random.randrange(256), random.randrange(
                256), random.randrange(256))
            sides = random.randint(3, MAX_SIDES)
            for j in range(sides):
                pointlist.append((random.randrange(self.width),
                                  random.randrange(self.textArea.top)))
            print(pointlist)
            pygame.draw.polygon(self.screen, color, pointlist)

    def getPixelMatrix(self):
        return pygame.surfarray.array2d(self.screen)

if __name__ == "__main__":
    interact = Interaction()
    interact.addCircle('red', (400, 400), 100)
    interact.addRandomPolygons()
    interact.loop()
