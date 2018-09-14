import sys
import pygame
import random
from pygame.locals import *


class SkierClass(pygame.sprite.Sprite):
    pass


def main():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("./music/bg_music.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

    screen = pygame.display.set_mode([640, 640])
    pygame.display.set_caption("Skier-2018/08/22")

    clock = pygame.time.Clock()
    skier = SkierClass()


if __name__ == '__main__':
    main()