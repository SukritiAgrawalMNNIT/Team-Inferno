import random
from barrier import Barrier
from time_stone import TimeStone
from settings import *


MIN_HORIZONTAL_GAP = 280
MAX_HORIZONTAL_GAP = 420


class BarrierSpawner:
    def __init__(self):
        self.pool = []

        for _ in range(POOL_SIZE):
            self.pool.append(Barrier())

        self.stone = TimeStone()
        self.next_spawn_distance = self.random_horizontal_gap()

    def random_horizontal_gap(self):
        return random.randint(
            MIN_HORIZONTAL_GAP,
            MAX_HORIZONTAL_GAP
        )

    def reset(self):
        for barrier in self.pool:
            barrier.active = False

        self.stone.active = False
        self.next_spawn_distance = self.random_horizontal_gap()

    def active_barriers(self):
        return [
            barrier for barrier in self.pool
            if barrier.active
        ]

    def spawn(self, gap):
        for barrier in self.pool:
            if not barrier.active:
                barrier.spawn(gap)

                if (
                    not self.stone.active
                    and random.random() < STONE_CHANCE
                ):
                    self.stone.spawn(
                        WIDTH + self.next_spawn_distance // 2
                    )

                self.next_spawn_distance = (
                    self.random_horizontal_gap()
                )
                return

    def update(self, dt, speed, gap):
        active = self.active_barriers()

        if not active:
            self.spawn(gap)
        else:
            newest = max(active, key=lambda b: b.x)

            if newest.x <= WIDTH - self.next_spawn_distance:
                self.spawn(gap)

        for barrier in self.pool:
            if barrier.active:
                barrier.update(dt, speed)

        self.stone.update(dt, speed)

    def hits_player(self, player_rect):
        for barrier in self.pool:
            if barrier.active and barrier.collides(player_rect):
                return True
        return False

    def stone_collected(self, player_rect):
        if self.stone.collected(player_rect):
            self.stone.active = False
            return True
        return False

    def count_passed(self, player_rect):
        count = 0

        for barrier in self.pool:
            if barrier.active and not barrier.passed:
                if barrier.x + BARRIER_WIDTH < player_rect.left:
                    barrier.passed = True
                    count += 1

        return count

    def draw(self, screen):
        for barrier in self.pool:
            if barrier.active:
                barrier.draw(screen)

        self.stone.draw(screen)