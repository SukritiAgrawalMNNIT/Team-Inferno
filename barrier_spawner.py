from barrier import Barrier
from settings import *


class BarrierSpawner:
    def __init__(self):
        # Make all the barriers once, at the start
        self.pool = []
        for _ in range(POOL_SIZE):
            self.pool.append(Barrier())

    def reset(self):
        """Start of a new run: put every barrier back in the pool."""
        for barrier in self.pool:
            barrier.active = False

    def active_barriers(self):
        result = []
        for barrier in self.pool:
            if barrier.active:
                result.append(barrier)
        return result

    def spawn(self, gap):
        """Take one unused barrier from the pool and send it in."""
        for barrier in self.pool:
            if not barrier.active:
                barrier.spawn(gap)
                return

    def update(self, dt, speed, gap):
        # 1. Is it time for a new barrier?
        active = self.active_barriers()
        if len(active) == 0:
            self.spawn(gap)
        else:
            newest_x = max(b.x for b in active)
            if newest_x <= WIDTH - BARRIER_SPACING:
                self.spawn(gap)

        # 2. Move all active barriers left
        for barrier in self.pool:
            if barrier.active:
                barrier.update(dt, speed)

    def hits_player(self, player_rect):
        for barrier in self.pool:
            if barrier.active and barrier.collides(player_rect):
                return True
        return False

    def count_passed(self, player_rect):
        """How many barriers did the Cloak just get past? (each counts once)"""
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