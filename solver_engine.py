import math
from data_models import CharacterStats

class SolverEngine:

    def __init__(self):
        self.level_mod = 1900
        self.base_main = 390

    def calculate_dps(self, stats: CharacterStats) -> float:
        """
        Deterministic placeholder formula.
        Phase 2 will replace with full FFXIV equation.
        """

        main_multiplier = (stats.main_stat - self.base_main) / self.base_main
        crit_rate = (stats.crit - 400) / self.level_mod
        dh_rate = (stats.direct_hit - 400) / self.level_mod
        det_multiplier = 1 + (stats.determination - 390) / self.level_mod

        base_damage = stats.weapon_damage * 10

        expected_crit = 1 + (crit_rate * 0.5)
        expected_dh = 1 + (dh_rate * 0.25)

        dps = base_damage * main_multiplier * det_multiplier * expected_crit * expected_dh

        return round(max(dps, 0), 2)
