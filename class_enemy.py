class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites, group_enemy)
        if pos == 0:
            self.x_cell, self.y_cell = 2, 0
            self.vector = [[1, 0], [0, 1], [1, 0], [0, -1]]
        if pos == 1:
            self.x_cell, self.y_cell = 2, 11
            self.vector = [[0, -1], [1, 0], [0, -1]]
        if pos == 2:
            self.x_cell, self.y_cell = 13, 7
            self.vector = [[-1 ,0], [0, -1], [1, 0], [0, -1]]

        self.x = LEFT + self.x_cell * CELL_SIZE
        self.y = TOP + self.y_cell * CELL_SIZE
        self.senter_enemy = (self.x + CELL_SIZE * 0.5, self.y + CELL_SIZE * 0.5)

        self.poten_heatpoints = 10000

        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(self.x, self.y, CELL_SIZE, CELL_SIZE)
        pygame.draw.circle(self.image, pygame.Color("grey"), (CELL_SIZE // 2, CELL_SIZE // 2), CELL_SIZE // 2)

        self.speed = 1 / fps
        self.x_change = 0
        self.y_change = 0

        self.heatpoints = 100
        self.negative = False
        self.last_vector_x, self.last_vector_y = 0, 0

    def damage(self, damage):
        self.heatpoints -= damage

    def damage_poten(self, damage):
        self.poten_heatpoints -= damage

    def killer(self):
        self.kill()

    def update(self):
        if self.vector:
            # print(self.rect)
            self.x_change += self.vector[0][0] * self.speed
            self.y_change += self.vector[0][1] * self.speed
            
            self.check_in_board()

            if self.negative:
                self.rect = self.rect.move(-1 * self.last_vector_x * int(self.x_change), -1 * self.last_vector_y * int(self.y_change))
                self.x_change, self.y_change = 0, 0
            else:
                self.rect = self.rect.move(int(self.x_change), int(self.y_change))

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
            print(self.rect)
            if self.vector[0][0] == -1 or self.vector[0][1] == -1:
                print((self.rect[1] - TOP) % CELL_SIZE, (self.rect[0] - LEFT) % CELL_SIZE)
                self.x_change = (CELL_SIZE - (self.rect[0] - LEFT) % CELL_SIZE) % CELL_SIZE
                self.y_change = (CELL_SIZE - (self.rect[0] - LEFT) % CELL_SIZE) % CELL_SIZE
            else:
                self.x_change = (self.rect[0] + CELL_SIZE - LEFT) % CELL_SIZE
                self.y_change = (self.rect[1] + CELL_SIZE- TOP) % CELL_SIZE

            self.last_vector_x, self.last_vector_y = self.vector[0]
            self.negative = True
            print(self.x_change, self.y_change)
           
            del self.vector[0]

            print("DELETE", self.vector)
        else:
            self.negative = False
