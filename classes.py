class Pole_Interfeic(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(group_interfeic)
        self.image = pygame.Surface((400, 800), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(800, 10, 400, 800)
        self.font = pygame.font.Font(None, 50)

        self.infa_coins_x = 200
        self.infa_coins_y = 50

        self.infa_heat_x = 25
        self.infa_heat_y = 50

        self.infa_frages_x = 100
        self.infa_frages_y = 10

        self.active_window = True

    def update(self, coins):
        self.image.fill(pygame.Color('black'))
        self.text_coins = self.font.render(f"Coins: {coins}", 1, (100, 255, 100))
        self.image.blit(self.text_coins, (self.infa_coins_x, self.infa_coins_y))
        self.text_heat = self.font.render(f"Heats: {heatpoints}", 1, (100, 255, 100))
        self.image.blit(self.text_heat, (self.infa_heat_x, self.infa_heat_y))

        self.text_frages = self.font.render(f"Frages: {FRAGES}", 1, (100, 255, 100))
        self.image.blit(self.text_frages, (self.infa_frages_x, self.infa_frages_y))
        
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites, group_enemy)
        if pos == 0:
            self.stat_heatpoints = 100
            self.heatpoints = 100
            self.poten_heatpoints = 100
            self.x_cell, self.y_cell = 2, 0
            self.vector = [[1, 0], [0, 1], [1, 0], [0, -1]]
            self.image = pygame.transform.scale(load_image('sasuke_enemy.png'), (50, 50))
            self.speed = 0.5 / fps
        if pos == 1:
            self.stat_heatpoints = 200
            self.heatpoints = 200
            self.poten_heatpoints = 200
            self.x_cell, self.y_cell = 2, 11
            self.vector = [[0, -1], [1, 0], [0, -1]]
            self.image = pygame.transform.scale(load_image('ff.png'), (50, 50))
            self.speed = 0.2 / fps
        if pos == 2:
            self.stat_heatpoints = 300
            self.heatpoints = 300
            self.poten_heatpoints = 300
            self.x_cell, self.y_cell = 13, 7
            self.vector = [[-1, 0], [0, -1], [1, 0], [0, -1]]
            self.image = pygame.transform.scale(load_image('hellsing_enemy_left.png'), (50, 50))
            self.speed = 0.1 / fps

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
        pygame.draw.rect(screen, (50, 150, 50), (self.rect[0], self.rect[1], int(self.heatpoints / self.stat_heatpoints * 50), 10))

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
            if self.x_cell == 13:
                self.image = pygame.transform.scale(load_image("hellsing_enemy_right.png"), (CELL_SIZE, CELL_SIZE))

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
            
            
while running:
    screen.fill((0, 0, 0))
    # screen.blit(image, (10, 10))
    if not heatpoints:
        pause = True
        for i in group_end_interfeic:
            i.draw()


    # screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                board.get_click(event.pos)
                if object_pay_interfeic.active_window == True and coordinates_click_tower != None:
                    if (object_pay_interfeic.object_button_yes.x < event.pos[
                        0] < object_pay_interfeic.object_button_yes.x + object_pay_interfeic.object_button_yes.size_width_but) and (
                            object_pay_interfeic.object_button_yes.y < event.pos[
                        1] < object_pay_interfeic.object_button_yes.y + object_pay_interfeic.object_button_yes.size_height_but):
                        board.map_game[coordinates_click_tower[1]][coordinates_click_tower[0]] = "t_zanyat"
                        a = MachineGun(coordinates_click_tower[0], coordinates_click_tower[1])
                        circle_of_tower = a.object_RadiusFire
                        for tower in group_tower:
                            tower.object_RadiusFire.draw_circle = False
                        circle_of_tower.draw_circle = True

                        # if circle_of_tower != None:
                        #     circle_of_tower.draw_circle = False
                        object_pay_interfeic.active_window = False

                if object_pay_interfeic.active_window == True and coordinates_click_tower != None:
                    if (object_pay_interfeic.object_button_no.x < event.pos[
                        0] < object_pay_interfeic.object_button_no.x + object_pay_interfeic.object_button_no.size_width_but) and (
                            object_pay_interfeic.object_button_no.y < event.pos[
                        1] < object_pay_interfeic.object_button_no.y + object_pay_interfeic.object_button_no.size_height_but):
                        object_pay_interfeic.active_window = False

                for tower in group_tower:
                    # if tower.rect.collidepoint(event.pos) and circle_of_tower == None:
                    #     tower.object_RadiusFire.draw_circle = True
                    #     print(tower.object_RadiusFire.draw_circle)
                    #     circle_of_tower = tower.object_RadiusFire
                    if tower.rect.collidepoint(event.pos) and circle_of_tower != tower.object_RadiusFire:
                        print(1)
                        circle_of_tower.draw_circle = False
                        tower.object_RadiusFire.draw_circle = True
                        circle_of_tower = tower.object_RadiusFire
                    if tower.rect.collidepoint(event.pos) and circle_of_tower == tower.object_RadiusFire:
                        circle_of_tower.draw_circle = False
        #         #
        # self.x, self.y = 500, 670
        # self.size_width = 200
        # self.size_height = 70
                if (500, 670) < event.pos < (700, 740):
                    Pain()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                if pause == False:
                    pause = True
                else:
                    pause = False

    if pause == False:
        for frages in group_frages_interfeic:
            frages.update()
            print('e')

        for tower in group_tower:
            tower.update()
            tower.object_RadiusFire.drawing()

        for bullet in group_bullet:
            bullet.update()
            bullet.check_collide_bullet_with_enemy()

        for enemy in group_enemy:
            enemy.update()

        # for btn in group_button_pain:
        #     btn.drawing()
        #
        # for pain in group_pain:
        #     pain.fill_pain()

        object_Base.check_na_visit_enemy()

        enemys.new_enemy_first()
        enemys.new_enemy_second()
        enemys.new_enemy_third()

    for inter in group_interfeic:
        inter.update(coins)

    # if perf_counter() > 7:
    #     FRAGES = 50

    # if perf_counter() > 10:
    #     FRAGES = 70

    # if perf_counter() > 15:
    #     FRAGES = 110

    # group_bullet.update(enemy)
    board.render()

    group_frages_interfeic.draw(screen)
    group_interfeic.draw(screen)
    group_button_pay_tower.draw(screen)
    group_enemy.draw(screen)
    all_sprites.draw(screen)
    clock.tick(60)
    pygame.display.flip()
