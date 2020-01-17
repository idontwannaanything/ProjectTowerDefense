import pygame

START = "s"
END = "e"
ROAD = "r"
PLACE_TOWER = "t"

all_sprites = pygame.sprite.Group()
group_bullet = pygame.sprite.Group()
group_enemy = pygame.sprite.Group()
group_tower = pygame.sprite.Group()

size = (800, 600)
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color("black"))
running = True
pygame.init()

CELL_SIZE = 50

class Board:
    def __init__(self, map_game):
        self.map_game = map_game
        self.left = 10
        self.top = 10
        self.cell_size = 50

    def render(self):
        for i in range(len(self.map_game)):
            for j in range(len(self.map_game[i])):
                if self.map_game[i][j] == "s":
                    pygame.draw.rect(screen, pygame.Color("blue"), (
                    self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size, self.cell_size))

                if self.map_game[i][j] == "e":
                    pygame.draw.rect(screen, pygame.Color("yellow"), (
                        self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size, self.cell_size))

                if self.map_game[i][j] == "r":
                    pygame.draw.rect(screen, pygame.Color("brown"), (
                        self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size, self.cell_size))



class Bullet(pygame.sprite.Sprite):
    def __init__(self, x_bullet, y_bullet, speed_of_the_bullet, damage):
        super.__init__(all_sprites, group_bullet)
        self.speed_of_the_bullet = speed_of_the_bullet

        self.image = pygame.Surface((6, 6), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"), (3, 3), 3)
        self.x_bullet = x_bullet
        self.y_bullet = y_bullet


        for enemy in group_enemy:    #sprytecollide принимает
            if

    def update(self):
        for enemy in group_enemy:






class Tower(pygame.sprite.Sprite):
    def __init__(self, x_cell, y_cell):
        super.__init__(all_sprites, group_tower)
        self.x_cell = x_cell
        self.y_cell = y_cell

        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA, 32)







    def killer(self):
        self.kill()


class MachineGun(Tower):
    def __init__(self, x_kletki_razmechenia, y_kletki_razmechenia, group, level, rate_of_fire, radius_of_the_fire,
                 speed_of_the_bullet, type_of_amunition="base"):
        super.__init__(x_kletki_razmechenia, y_kletki_razmechenia)     # нужно окрасить холст


class Enemy(pygame.sprite.Sprite):
    pass









