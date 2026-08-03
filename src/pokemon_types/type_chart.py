from .type import Type

TYPE_EFFECTIVENESS = {
    # Normal
    (Type.NORMAL, Type.ROCK): 0.5,
    (Type.NORMAL, Type.STEEL): 0.5,
    (Type.NORMAL, Type.GHOST): 0,
    # Fire
    (Type.FIRE, Type.ROCK): 0.5,
    (Type.FIRE, Type.BUG): 2,
    (Type.FIRE, Type.STEEL): 2,
    (Type.FIRE, Type.FIRE): 0.5,
    (Type.FIRE, Type.WATER): 0.5,
    (Type.FIRE, Type.GRASS): 2,
    (Type.FIRE, Type.ICE): 2,
    (Type.FIRE, Type.DRAGON): 0.5,
    # Water
    (Type.WATER, Type.GROUND): 2,
    (Type.WATER, Type.ROCK): 2,
    (Type.WATER, Type.FIRE): 2,
    (Type.WATER, Type.WATER): 0.5,
    (Type.WATER, Type.GRASS): 0.5,
    (Type.WATER, Type.DRAGON): 0.5,
    # Electric
    (Type.ELECTRIC, Type.FLYING): 2,
    (Type.ELECTRIC, Type.GROUND): 0,
    (Type.ELECTRIC, Type.WATER): 2,
    (Type.ELECTRIC, Type.GRASS): 0.5,
    (Type.ELECTRIC, Type.ELECTRIC): 0.5,
    (Type.ELECTRIC, Type.DRAGON): 0.5,
    # Grass
    (Type.GRASS, Type.FLYING): 0.5,
    (Type.GRASS, Type.POISON): 0.5,
    (Type.GRASS, Type.GROUND): 2,
    (Type.GRASS, Type.ROCK): 2,
    (Type.GRASS, Type.BUG): 0.5,
    (Type.GRASS, Type.STEEL): 0.5,
    (Type.GRASS, Type.FIRE): 0.5,
    (Type.GRASS, Type.WATER): 2,
    (Type.GRASS, Type.GRASS): 0.5,
    (Type.GRASS, Type.DRAGON): 0.5,
    # Ice
    (Type.ICE, Type.FLYING): 2,
    (Type.ICE, Type.GROUND): 2,
    (Type.ICE, Type.STEEL): 0.5,
    (Type.ICE, Type.FIRE): 0.5,
    (Type.ICE, Type.WATER): 0.5,
    (Type.ICE, Type.GRASS): 2,
    (Type.ICE, Type.ICE): 0.5,
    (Type.ICE, Type.DRAGON): 2,
    # Fighting
    (Type.FIGHTING, Type.NORMAL): 2,
    (Type.FIGHTING, Type.FLYING): 0.5,
    (Type.FIGHTING, Type.POISON): 0.5,
    (Type.FIGHTING, Type.ROCK): 2,
    (Type.FIGHTING, Type.BUG): 0.5,
    (Type.FIGHTING, Type.GHOST): 0,
    (Type.FIGHTING, Type.STEEL): 2,
    (Type.FIGHTING, Type.PSYCHIC): 0.5,
    (Type.FIGHTING, Type.ICE): 2,
    (Type.FIGHTING, Type.DARK): 2,
    (Type.FIGHTING, Type.FAIRY): 0.5,
    # Poison
    (Type.POISON, Type.POISON): 0.5,
    (Type.POISON, Type.GROUND): 0.5,
    (Type.POISON, Type.ROCK): 0.5,
    (Type.POISON, Type.GHOST): 0.5,
    (Type.POISON, Type.STEEL): 0,
    (Type.POISON, Type.GRASS): 2,
    (Type.POISON, Type.FAIRY): 2,
    # Ground
    (Type.GROUND, Type.FLYING): 0,
    (Type.GROUND, Type.POISON): 2,
    (Type.GROUND, Type.ROCK): 2,
    (Type.GROUND, Type.BUG): 0.5,
    (Type.GROUND, Type.STEEL): 2,
    (Type.GROUND, Type.FIRE): 2,
    (Type.GROUND, Type.GRASS): 0.5,
    (Type.GROUND, Type.ELECTRIC): 2,
    # Flying
    (Type.FLYING, Type.FIGHTING): 2,
    (Type.FLYING, Type.ROCK): 0.5,
    (Type.FLYING, Type.BUG): 2,
    (Type.FLYING, Type.STEEL): 0.5,
    (Type.FLYING, Type.GRASS): 2,
    (Type.FLYING, Type.ELECTRIC): 0.5,
    # Psychic
    (Type.PSYCHIC, Type.FIGHTING): 2,
    (Type.PSYCHIC, Type.POISON): 2,
    (Type.PSYCHIC, Type.STEEL): 0.5,
    (Type.PSYCHIC, Type.PSYCHIC): 0.5,
    (Type.PSYCHIC, Type.DARK): 0,
    # Bug
    (Type.BUG, Type.FIGHTING): 0.5,
    (Type.BUG, Type.FLYING): 0.5,
    (Type.BUG, Type.POISON): 0.5,
    (Type.BUG, Type.GHOST): 0.5,
    (Type.BUG, Type.STEEL): 0.5,
    (Type.BUG, Type.FIRE): 0.5,
    (Type.BUG, Type.GRASS): 2,
    (Type.BUG, Type.PSYCHIC): 2,
    (Type.BUG, Type.DARK): 2,
    (Type.BUG, Type.FAIRY): 0.5,
    # Rock
    (Type.ROCK, Type.FIGHTING): 0.5,
    (Type.ROCK, Type.FLYING): 2,
    (Type.ROCK, Type.GROUND): 0.5,
    (Type.ROCK, Type.BUG): 2,
    (Type.ROCK, Type.STEEL): 0.5,
    (Type.ROCK, Type.FIRE): 2,
    (Type.ROCK, Type.ICE): 2,
    # Ghost
    (Type.GHOST, Type.NORMAL): 0,
    (Type.GHOST, Type.GHOST): 2,
    (Type.GHOST, Type.PSYCHIC): 2,
    (Type.GHOST, Type.DARK): 0.5,
    # Dragon
    (Type.DRAGON, Type.STEEL): 0.5,
    (Type.DRAGON, Type.DRAGON): 2,
    (Type.DRAGON, Type.FAIRY): 0,
    # Dark
    (Type.DARK, Type.FIGHTING): 0.5,
    (Type.DARK, Type.GHOST): 2,
    (Type.DARK, Type.PSYCHIC): 2,
    (Type.DARK, Type.DARK): 0.5,
    (Type.DARK, Type.FAIRY): 0.5,
    # Steel
    (Type.STEEL, Type.ROCK): 2,
    (Type.STEEL, Type.STEEL): 0.5,
    (Type.STEEL, Type.FIRE): 0.5,
    (Type.STEEL, Type.WATER): 0.5,
    (Type.STEEL, Type.ELECTRIC): 0.5,
    (Type.STEEL, Type.ICE): 2,
    (Type.STEEL, Type.FAIRY): 2,
    # Fairy
    (Type.FAIRY, Type.FIGHTING): 2,
    (Type.FAIRY, Type.POISON): 0.5,
    (Type.FAIRY, Type.STEEL): 0.5,
    (Type.FAIRY, Type.FIRE): 0.5,
    (Type.FAIRY, Type.DRAGON): 2,
    (Type.FAIRY, Type.DARK): 2,
}


def single_type_effectiveness(
    attacking: Type,
    defending: Type,
) -> float:
    return TYPE_EFFECTIVENESS.get((attacking, defending), 1.0)


def effectiveness(
    attacking: Type,
    defending_types: tuple[Type, ...],
) -> float:
    multiplier = 1.0

    for defender_type in defending_types:
        multiplier *= single_type_effectiveness(
            attacking,
            defender_type,
        )

    return multiplier
