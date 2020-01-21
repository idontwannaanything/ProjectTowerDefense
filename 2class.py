class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites, group_enemy)
        if pos == 0:
            self.heatpoints = 100
            self.poten_heatpoints = 100
            self.x_cell, self.y_cell = 2, 0
            self.vector = [[1, 0], [0, 1], [1, 0], [0, -1]]
            self.image = pygame.transform.scale(load_image('sasuke_enemy.png'), (50, 50))
            self.speed = 0.5 / fps
        if pos == 1:
            self.heatpoints = 200
            self.poten_heatpoints = 200
            self.x_cell, self.y_cell = 2, 11
            self.vector = [[0, -1], [1, 0], [0, -1]]
            self.image = pygame.transform.scale(load_image('ff.png'), (50, 50))
            self.speed = 0.2 / fps
        if pos == 2:
            self.heatpoints = 300
            self.poten_heatpoints = 300
            self.x_cell, self.y_cell = 13, 7
            self.vector = [[-1, 0], [0, -1], [1, 0], [0, -1]]
            self.image = pygame.transform.scale(load_image('hellsing_enemy.png'), (50, 50))
            self.speed = 0.07 / fps

        self.x = LEFT + self.x_cell * CELL_SIZE
        self.y = TOP + self.y_cell * CELL_SIZE
        self.senter_enemy = [self.x + CELL_SIZE * 0.5, self.y + CELL_SIZE * 0.5]

        # self.image = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA, 32)

        self.rect = pygame.Rect(self.x, self.y, CELL_SIZE, CELL_SIZE)
        # pygame.draw.circle(self.image, pygame.Color("grey"), (CELL_SIZE // 2, CELL_SIZE // 2), CELL_SIZE // 2)


        self.x_change = 0
        self.y_change = 0

        self.negative = False
        self.last_vector_x, self.last_vector_y = 0, 0

    def damage(self, damage):
        self.heatpoints -= damage

    def damage_poten(self, damage):
        self.poten_heatpoints -= damage

    def killer(self):
        global coins
        coins += 10
        self.kill()
        global FRAGES
        FRAGES += 1
        print(FRAGES)

    def update(self):
        if self.vector:
            # print(self.rect)
            self.x_change += self.vector[0][0] * self.speed
            self.y_change += self.vector[0][1] * self.speed

            self.check_in_board()

            if self.negative:
                self.rect = self.rect.move(-1 * self.last_vector_x * int(self.x_change),
                                           -1 * self.last_vector_y * int(self.y_change))
                self.senter_enemy[0] += -1 * self.last_vector_x * int(self.x_change)
                self.senter_enemy[1] += -1 * self.last_vector_y * int(self.y_change)
                self.x_change, self.y_change = 0, 0
            else:
                self.rect = self.rect.move(int(self.x_change), int(self.y_change))

                self.senter_enemy[0] += int(self.x_change)
                self.senter_enemy[1] += int(self.y_change)

        if self.heatpoints <= 0:
            self.killer()

    def check_in_board(self):
        if self.vector[0][0] == -1 or self.vector[0][1] == -1:
            j, i = (self.rect[0] - LEFT) // CELL_SIZE, (self.rect[1] - TOP) // CELL_SIZE
        else:
            j, i = (self.rect[0] + CELL_SIZE - LEFT - 1) // CELL_SIZE, (self.rect[1] + CELL_SIZE - 1 - TOP) // CELL_SIZE
        # print(i, j)
        # print(map_tower_defense[i][j])

        if map_tower_defense[i][j] == "e":
            self.vector.clear()

        elif map_tower_defense[i][j] != 'r':
            # print(self.rect)
            if self.vector[0][0] == -1 or self.vector[0][1] == -1:
                # print((self.rect[1] - TOP) % CELL_SIZE, (self.rect[0] - LEFT) % CELL_SIZE)
                self.x_change = (CELL_SIZE - (self.rect[0] - LEFT) % CELL_SIZE) % CELL_SIZE
                self.y_change = (CELL_SIZE - (self.rect[0] - LEFT) % CELL_SIZE) % CELL_SIZE

            else:
                self.x_change = (self.rect[0] + CELL_SIZE - LEFT) % CELL_SIZE
                self.y_change = (self.rect[1] + CELL_SIZE - TOP) % CELL_SIZE

            self.last_vector_x, self.last_vector_y = self.vector[0]
            self.negative = True
            # print(self.x_change, self.y_change)
            del self.vector[0]

            # print("DELETE", self.vector)
        else:
            self.negative = False


class AllEnemys:
    def __init__(self):
        self.time_last_first_enemy = perf_counter()
        self.time_last_second_enemy = perf_counter()
        self.time_last_third_enemy = perf_counter()

        self.time_to_next_first = 5.0
        self.time_to_next_second = 5.0
        self.time_to_next_third = 5.0

        self.time_now_first = 0
        self.time_now_second = 0
        self.time_now_third = 0

    def new_enemy_first(self):
        self.time_now_first = perf_counter()

        if (self.time_now_first - self.time_last_first_enemy) >= self.time_to_next_first:
            self.time_last_first_enemy = perf_counter()
            return Enemy(0)
        if FRAGES > 7:
            self.time_to_next_first = 4.0
        if FRAGES > 15:
            self.time_to_next_first = 3.0

    def new_enemy_second(self):
        self.time_now_second = perf_counter()

        if FRAGES > 20 and (self.time_now_second - self.time_last_second_enemy) >= self.time_to_next_second:
            self.time_last_second_enemy = perf_counter()
            return Enemy(1)
        if FRAGES > 30:
            self.time_to_next_second = 4.0

    def new_enemy_third(self):
        self.time_now_third = perf_counter()

        if FRAGES > 50 and (self.time_now_third - self.time_last_third_enemy) >= self.time_to_next_third:
            self.time_last_third_enemy = perf_counter()
            return Enemy(2)
        if FRAGES > 75:
            self.time_to_next_first = 2.0
            self.time_to_next_second = 3.0
            self.time_to_next_third = 4.0

        if FRAGES > 100:
            self.time_to_next_second = 2.0
            self.time_to_next_third = 2.0

        if FRAGES > 120:
            self.speed = 10 / fps
