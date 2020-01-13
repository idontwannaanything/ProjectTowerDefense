import pygame
from math import sqrt
from time import perf_counter

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

X_Y_BASE = []

LEFT = 10
TOP = 10


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

                    X_Y_BASE = (
                        self.left + j * self.cell_size + self.cell_size, self.top + i * self.cell_size + self.cell_size)

                if self.map_game[i][j] == "r":
                    pygame.draw.rect(screen, pygame.Color("brown"), (
                        self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size, self.cell_size))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x_y_spawn, speed_of_the_bullet, enemy_tsel, damage):  # скорость пули в пикселях в секнуду
        super.__init__(all_sprites, group_bullet)
        self.speed_of_the_bullet = speed_of_the_bullet

        self.damage = damage

        self.image = pygame.Surface((6, 6), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, pygame.Color("red"), (3, 3), 3)
        self.x_bullet = x_y_spawn[0]
        self.y_bullet = x_y_spawn[1]
        self.enemy_tsel = enemy_tsel

        self.put_do_enemy = (self.x_enemy - self.x_bullet) ** 2 + (self.y_enemy - self.y_bullet) ** 2

        self.vector_x_bullet = (self.enemy_tsel.x_enemy - self.x_bullet) / self.put_do_enemy  # высчитываем на сколько
        # пуля должна сместится в условную единицу времени
        self.vector_y_bullet = (self.enemy_tsel.y_enemy - self.y_bullet) / self.put_do_enemy

        self.x_change = 0  # накапливаем в этих переменных вещественные числа сдвига по х и по у
        self.y_change = 0
        self.t1_puli = perf_counter()

    def update(self):
        t2_puli = perf_counter()

        self.rect = self.rect.move(self.vector_x_bullet * self.speed_of_the_bullet * (t2_puli - self.t1_puli),
                                   # нужно проверить как работает
                                   self.vector_y_bullet * self.speed_of_the_bullet * (t2_puli - self.t1_puli))
        self.t1_puli = t2_puli

    def killer(self):
        self.kill()

    def check_collide_bullet_with_enemy(self):
        if pygame.sprite.sprite.collide_rect(self.enemy_tsel, self):
            self.enemy_tsel.damage(self.damage)
            self.kill()




class Tower(pygame.sprite.Sprite):
    def __init__(self, x_cell, y_cell):
        super.__init__(all_sprites, group_tower)
        self.x_cell = x_cell
        self.y_cell = y_cell
        self.senter_cell_tower = (LEFT + self.x_cell * CELL_SIZE, TOP + self.y_cell * CELL_SIZE)

        self.image_tower = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA, 32)

    def killer(self):  # удаляем башню, если не нужна
        self.kill()


class MachineGun(Tower):
    def __init__(self, x_kletki_razmechenia, y_kletki_razmechenia, rate_of_fire, radius_of_the_fire,
                 speed_of_the_bullet, type_of_amunition="base"):
        super.__init__(x_kletki_razmechenia, y_kletki_razmechenia)  # нужно окрасить холст
        self.radius_of_the_fire = radius_of_the_fire
        self.rate_of_fire = rate_of_fire
        self.speed_of_the_bullet = speed_of_the_bullet

        self.damage = 2

        pygame.draw.rect(self.image_tower, pygame.Color("orange"), (0, 0, CELL_SIZE, CELL_SIZE))

        class RadiusFire(pygame.sprite.Sprite):
            def __init__(self, radius_of_the_fire):
                super.__init__(all_sprites)
                self.image_radius_of_fire = pygame.Surface((2 * self.radius_of_the_fire, 2 * self.radius_of_the_fire),
                                                           pygame.SRCALPHA, 32)
                pygame.draw.circle(self.image_radius_of_fire, pygame.Color("purple"),
                                   (self.radius_of_the_fire, self.radius_of_the_fire), self.radius_of_the_fire)

        self.object_RadiusFire = RadiusFire(self.radius_of_the_fire)

    def shot(self):
        self.spisok_vragov_na_change = pygame.sprite.spritecollide(self.object_RadiusFire.image_radius_of_fire,
                                                                   group_enemy)  # надо найти ближайшего к базе врага
        self.puti_do_base = list(map(
            lambda s: sqrt((s.x_enemy - self.senter_cell_tower[0]) ** 2 + (s.y_enemy - self.senter_cell_tower[1]) ** 2),
            self.spisok_vragov_na_change))
        self.enemy_tsel = self.spisok_vragov_na_change.index(min(self.puti_do_base))

        Bullet(self.senter_cell_tower, self.speed_of_the_bullet, self.enemy_tsel, self.damage)


class Enemy(pygame.sprite.Sprite):
    pass




