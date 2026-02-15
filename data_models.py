from dataclasses import dataclass

@dataclass
class CharacterStats:
    main_stat: int
    crit: int
    direct_hit: int
    determination: int
    skill_speed: int
    weapon_damage: int
