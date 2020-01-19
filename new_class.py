class AllEnemys(pygame.sprite.Sprite):
    def __init__(self):
        super.__init__(self)
        self.time_last_enemy = perf_counter()
        self.time_next_enemy = 4
        self.time_to_next_second = 4
        self.time_to_next_third = 4

    def new_enemy(self):
        if (perf_counter() - self.time_last_enemy) % self.time_next_enemy == self.time_next_enemy:
            Enemy(0)
        if FRAGES > 20:
            self.time_next_enemy = 2
        if FRAGES > 40 and (perf_counter() - self.time_last_enemy) % self.time_to_next_second == self.time_to_next_second:
            Enemy(1)
        if FRAGES > 60:
            self.time_to_next_second = 2
        if FRAGES > 80 and (perf_counter() - self.time_last_enemy) % self.time_to_next_third == self.time_to_next_third:
            Enemy(2)
        if FRAGES > 100 and (perf_counter() - self.time_last_enemy) % self.time_to_next_third == self.time_to_next_third:
            self.time_to_next_third = 2
