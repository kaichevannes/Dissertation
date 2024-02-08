from swarm.swarm import Swarm

VISUALISATION_SLOW = 60
VISUALISATION_REAL_TIME = 0


class Visualiser:

    def __init__(self, slow: bool = False):
        if slow:
            self.interval = VISUALISATION_SLOW
        else:
            self.interval = VISUALISATION_REAL_TIME

    def set_swarm(self, swarm: Swarm):
        