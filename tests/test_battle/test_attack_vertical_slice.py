import json

from abilities.resolver import resolve_ability
from ability import Ability
from battle import BattleContext, BattleResolver, BattleState, StubRNG
from battle.action import MoveAction
from battle.decision.legal_actions import get_legal_actions
from database.ability_database import AbilityDatabase
from database.item_database import ItemDatabase
from database.learnset_database import LearnsetDatabase
from database.move_database import MoveDatabase
from database.species_database import SpeciesDatabase
from move_effects.damage_effect import DamageEffect
from pokemon import Pokemon
from pokemon_set_resolver import PokemonSetResolver
from stats.evs import EVs
from stats.ivs import IVs
from stats.nature import Nature


class SelectingAI:
    def __init__(self):
        self.selected_action = None

    def choose_action(self, *, battle_context, pokemon, legal_actions):
        self.selected_action = legal_actions[0]
        return self.selected_action


def test_database_resolved_tackle_executes_deterministically(
    tmp_path,
    garchomp_species,
):
    move_directory = tmp_path / "moves"
    move_directory.mkdir()
    (move_directory / "tackle.json").write_text(
        json.dumps(
            {
                "accuracy": 100,
                "category": "PHYSICAL",
                "display_name": "Tackle",
                "effects": [],
                "id": 33,
                "move_flags": [],
                "move_name": "TACKLE",
                "move_type": "NORMAL",
                "power": 40,
                "pp": 35,
                "priority": 0,
                "target": "SINGLE_TARGET",
            }
        ),
        encoding="utf-8",
    )

    resolver = PokemonSetResolver(
        species_database=SpeciesDatabase({garchomp_species.name: garchomp_species}),
        ability_database=AbilityDatabase(
            {
                "ROUGH_SKIN": Ability(
                    name="ROUGH_SKIN",
                    display_name="Rough Skin",
                    id=17,
                    generation="GENERATION_III",
                )
            }
        ),
        move_database=MoveDatabase.load(move_directory),
        item_database=ItemDatabase({}),
        learnset_database=LearnsetDatabase(
            {garchomp_species.name: frozenset({"TACKLE"})}
        ),
    )

    def resolve_pokemon():
        pokemon_set = resolver.resolve(
            species_name="GARCHOMP",
            ability_name="ROUGH_SKIN",
            move_names=("TACKLE",),
            level=50,
            nature=Nature.JOLLY,
            ivs=IVs(31, 31, 31, 31, 31, 31),
            evs=EVs(6, 252, 0, 0, 0, 252),
        )
        return Pokemon.from_set(pokemon_set)

    attacker = resolve_pokemon()
    target = resolve_pokemon()
    assert attacker.ability is resolve_ability("ROUGH_SKIN")
    assert len(attacker.pokemon_set.moves[0].effects) == 1

    # With these level 50 Garchomp builds, neutral Tackle at a fixed 1.0
    # damage roll deals 29 damage. Set exactly that much HP to verify the
    # lethal and pending-switch path as well as the ordinary damage result.
    target.current_hp = 29
    state = BattleState(
        player_active=(attacker,),
        opponent_active=(target,),
    )
    context = BattleContext(
        state=state,
        rng=StubRNG(
            accuracy_rolls=[0.0],
            critical_rolls=[1.0],
            damage_rolls=[1.0],
        ),
    )
    legal_actions = get_legal_actions(
        battle_context=context,
        pokemon=attacker,
    )
    move_actions = tuple(
        action for action in legal_actions if isinstance(action, MoveAction)
    )
    assert len(move_actions) == 1
    assert move_actions[0].move.name == "TACKLE"

    ai = SelectingAI()
    action = ai.choose_action(
        battle_context=context,
        pokemon=attacker,
        legal_actions=legal_actions,
    )
    assert action is ai.selected_action

    BattleResolver(context).resolve_turn(actions=(action,))

    assert target.current_hp == 0
    assert target.is_fainted
    assert state.pending_switches == (target,)


def test_database_resolved_swords_dance_executes_through_battle(
    tmp_path,
    garchomp,
    garchomp_species,
):
    move_directory = tmp_path / "moves"
    move_directory.mkdir()
    (move_directory / "swords-dance.json").write_text(
        json.dumps(
            {
                "accuracy": None,
                "category": "STATUS",
                "display_name": "Swords Dance",
                "effects": [{"type": "stat_change", "stat": "ATTACK", "stages": 2}],
                "id": 14,
                "move_flags": [],
                "move_name": "SWORDS_DANCE",
                "move_type": "NORMAL",
                "power": None,
                "pp": 20,
                "priority": 0,
                "target": "SELF",
            }
        ),
        encoding="utf-8",
    )

    resolver = PokemonSetResolver(
        species_database=SpeciesDatabase({garchomp_species.name: garchomp_species}),
        ability_database=AbilityDatabase(
            {garchomp.pokemon_set.ability.name: garchomp.pokemon_set.ability}
        ),
        move_database=MoveDatabase.load(move_directory),
        item_database=ItemDatabase({}),
        learnset_database=LearnsetDatabase(
            {garchomp_species.name: frozenset({"SWORDS_DANCE"})}
        ),
    )
    pokemon_set = garchomp.pokemon_set
    attacker = Pokemon.from_set(
        resolver.resolve(
            species_name=garchomp_species.name,
            ability_name=pokemon_set.ability.name,
            move_names=("SWORDS_DANCE",),
            level=pokemon_set.level,
            nature=pokemon_set.nature,
            ivs=pokemon_set.ivs,
            evs=pokemon_set.evs,
        )
    )
    target = Pokemon.from_set(pokemon_set)
    move = attacker.pokemon_set.moves[0]

    assert len(move.effects) == 1
    assert not isinstance(move.effects[0], DamageEffect)

    state = BattleState(player_active=(attacker,), opponent_active=(target,))
    context = BattleContext(state=state, rng=StubRNG())
    actions = get_legal_actions(battle_context=context, pokemon=attacker)
    action = next(action for action in actions if isinstance(action, MoveAction))

    BattleResolver(context).resolve_turn(actions=(action,))

    assert attacker.stat_stages.attack == 2
    assert attacker.current_hp == attacker.stats.hp
