import time


class GFX_Effect:
    # A generic graphical effect.
    # Time units are seconds.
    def __init__(self,
                 x,
                 y,
                 gfx_effect_tile=0x1000,
                 duration=0.3,
                 delay=0,
                 projectile=False):
        self.x = x
        self.y = y
        self.gfx_effect_tile = gfx_effect_tile
        self.duration = max(duration, 0)
        self.delay = max(delay, 0)
        self.projectile = projectile
        self.start_time = None
        self.render = True
        self.expired = False
        self.start_time = time.perf_counter() + delay

    def update(self):
        # Update gfx_effect states.
        # Check for delay

        if self.start_time > time.perf_counter():
            self.render = False
            return
        # Check for duration
        if time.perf_counter() - self.start_time > self.duration:
            self.expired = True
            return

        self.render = True