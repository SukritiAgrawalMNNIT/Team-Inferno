import random
from barrier import Barrier
from time_stone import TimeStone
from settings import *


class BarrierSpawner:
    def __init__(self):
        self.pool = []
        for _ in range(POOL_SIZE):
            self.pool.append(Barrier())
        self.stone = TimeStone()
        self.last_gap_y = None        # height of the previous gap, so the next one stays reachable

    def reset(self):
        for barrier in self.pool:
            barrier.active = False
        self.stone.active = False
        self.last_gap_y = None

    def active_barriers(self):
        result = []
        for barrier in self.pool:
            if barrier.active:
                result.append(barrier)
        return result

    def spawn(self, gap, speed=250):
        # The faster the barriers, the less time to climb, so the smaller the allowed shift
        max_shift = int(CLIMB_RATE * BARRIER_SPACING / max(speed, 1))
        for barrier in self.pool:
            if not barrier.active:
                barrier.spawn(gap, self.last_gap_y, max_shift)
                self.last_gap_y = barrier.gap_y
                if not self.stone.active and random.random() < STONE_CHANCE:
                    self.stone.spawn(WIDTH + BARRIER_SPACING // 2)
                return

    def update(self, dt, speed, gap):
        active = self.active_barriers()
        if len(active) == 0:
            self.spawn(gap, speed)
        else:
            newest_x = max(b.x for b in active)
            if newest_x <= WIDTH - BARRIER_SPACING:
                self.spawn(gap, speed)

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
        """True once, at the moment the Cloak grabs the Time Stone."""
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