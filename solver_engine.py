import logging
from data_models import Spell, PlayerState

class BLMSolver:

    def __init__(self, fight_duration: float):
        self.fight_duration = fight_duration
        self.state = PlayerState()
        self.rotation_log = []

        self.fire = Spell("Fire", 300, 2000, 2.5)
        self.blizzard = Spell("Blizzard", 200, -3000, 2.5)

    def log(self, message):
        logging.info(message)
        self.rotation_log.append(message)

    def cast_spell(self, spell: Spell):
        self.state.time_elapsed += spell.cast_time
        self.state.mp -= spell.mp_cost

        if self.state.mp <= 0:
            self.state.mp = 0

        self.log(f"{round(self.state.time_elapsed,2)}s: Cast {spell.name} | MP: {self.state.mp}")

    def simulate(self):
        self.log("Starting simulation")

        while self.state.time_elapsed < self.fight_duration:

            if self.state.mp > 3000:
                self.cast_spell(self.fire)
                self.state.in_astral_fire = True
                self.state.in_umbral_ice = False
            else:
                self.cast_spell(self.blizzard)
                self.state.in_astral_fire = False
                self.state.in_umbral_ice = True
                self.state.mp = 10000  # simulate MP refresh in ice

        self.log("Simulation complete")
        return self.rotation_log
