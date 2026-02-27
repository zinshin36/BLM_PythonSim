CURRENT_EXPANSION = "Dawntrail"

EXPANSION_CONSTANTS = {
    "Dawntrail": {
        "BASE_MAIN": 390,
        "BASE_SUB": 400,
        "BASE_DIV": 1900
    }
}


def set_expansion(name):
    global CURRENT_EXPANSION
    CURRENT_EXPANSION = name


def simulate_blm_dps(gear_set):
    const = EXPANSION_CONSTANTS.get(
        CURRENT_EXPANSION,
        EXPANSION_CONSTANTS["Dawntrail"]
    )

    BASE_MAIN = const["BASE_MAIN"]
    BASE_SUB = const["BASE_SUB"]
    BASE_DIV = const["BASE_DIV"]

    total = {}
    for item in gear_set.values():
        for stat, val in item["stats"].items():
            total[stat] = total.get(stat, 0) + val

    main = total.get("Intelligence", 3000)
    crit = total.get("CriticalHit", BASE_SUB)
    det = total.get("Determination", BASE_SUB)

    main_mod = 1 + (main - BASE_MAIN) / BASE_DIV
    det_mod = 1 + (det - BASE_MAIN) / BASE_DIV
    crit_mod = 1 + (crit - BASE_SUB) / BASE_DIV

    return main_mod * det_mod * crit_mod * 100000
