from logger import log

def simulate_dps(gear_set):
    """
    Full BLM DPS simulator for top-N gear evaluation
    """

    total = {}

    for item in gear_set.values():
        for stat, val in item["stats"].items():
            total[stat] = total.get(stat, 0) + val

    main = total.get("Intelligence", 3000)
    crit = total.get("CriticalHit", 400)
    det = total.get("Determination", 400)
    dh = total.get("DirectHit", 400)
    ss = total.get("SpellSpeed", 400)
    wd = total.get("WeaponDamage", 120)

    # Crit formula
    crit_mod = 1 + ((crit - 400) / 1900)
    # Direct Hit
    dh_mod = 1 + ((dh - 400) / 3300)
    # Determination
    det_mod = 1 + ((det - 400) / 1900)
    # SpellSpeed GCD
    ss_casts = 60 / (2.5 - ((ss - 400) / 1300))

    # Base potency per spell
    potency = 320

    # DPS calculation
    dps = wd * main * crit_mod * det_mod * dh_mod * potency * ss_casts

    return dps
