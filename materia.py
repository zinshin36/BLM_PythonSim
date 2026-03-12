from logger import log
from materia_engine import apply_optimal_materia

def apply_materia_logic(gear_set):
    optimized = []

    for item in gear_set:
        apply_optimal_materia(item)
        optimized.append(item)

    log("Materia logic applied")
    return optimized
