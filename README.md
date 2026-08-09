# PokeCarlo

PokeCarlo is an early-stage Python battle simulator for Pokémon Champions. It
contains runtime models for Pokémon builds and combatants, move resolution,
damage calculation, stats, status conditions, battle actions, and battle AI.

The project is not yet a complete Pokémon Champions rules implementation.
Held-item behavior, item legality, and several other game mechanics are still
planned work.

## Runtime architecture

PokéAPI data is converted into generated JSON and loaded into immutable runtime
definitions:

```text
PokéAPI
  ↓
importers and generated JSON
  ↓
SpeciesDatabase  → Species ───────┐
AbilityDatabase  → Ability ───────┤
MoveDatabase     → Move ──────────┤→ PokemonSet → Pokemon
ItemDatabase     → Item ──────────┤
LearnsetDatabase → frozenset[str] ┘
```

`Species`, `Ability`, `Move`, and `Item` are immutable static definitions.
Databases load those definitions from generated JSON and provide normalized
name lookup. `LearnsetDatabase` provides canonical move-name sets for
construction-time legality checks.

`PokemonSet` is an immutable, fully configured loadout containing:

- a `Species` form;
- level, nature, IVs, and EVs;
- resolved `Move` objects;
- a resolved `Ability` object; and
- an optional resolved `Item` (`None` means the Pokémon holds nothing).

`PokemonSet.from_components()` receives these resolved objects and a learnset
for validation. The learnset is not stored on the resulting set. The set
validates the one-to-four move limit, duplicate moves, learnset legality, and
whether the selected ability is listed by the species.

`Pokemon` is the mutable combatant created by `Pokemon.from_set()`. It keeps
the original `PokemonSet`, calculates battle stats from its species and build
configuration, and owns mutable state such as current HP, stat stages, and
status. Static databases are not consulted while constructing a `Pokemon`.

There is not currently a production coordinator that resolves all database
names into a set. Callers are expected to load the databases and pass the
resolved values to `PokemonSet.from_components()`. The test fixtures are the
current complete example of that construction flow. `main.py` currently
demonstrates species loading only.

### Ability behavior note

The static `ability.Ability` model contains metadata loaded by
`AbilityDatabase`. The repository also has a separate `abilities` package with
behavior-oriented ability classes used by existing battle code. These are
currently overlapping boundaries: battle code invokes behavior methods on the
selected ability, while the static database model does not provide those
methods. This is documented for a future ability-runtime refactor and is not
changed by the current codebase.

## Database and generated data

The runtime databases are:

| Database | Runtime value | Source data |
| --- | --- | --- |
| `SpeciesDatabase` | `Species` | generated Pokémon/form JSON |
| `AbilityDatabase` | static `Ability` | generated ability JSON |
| `MoveDatabase` | `Move` | generated move JSON |
| `ItemDatabase` | static `Item` | generated item JSON |
| `LearnsetDatabase` | `frozenset[str]` | generated Champions learnset JSON |

The database loaders live under `src/database/` and use `load(directory)` as
their primary constructor. Lookups normalize common lowercase, hyphenated,
and underscored names while retaining canonical names in the loaded models.

Generated and raw API data are intentionally ignored by Git. A clean checkout
does not contain those directories until the data builder has been run.

The generation script is `src/data/scripts/build_database.py`. It uses the
PokéAPI cache/retry flow and supports individual or complete builds, including:

```bash
uv run python src/data/scripts/build_database.py --pokemon garchomp
uv run python src/data/scripts/build_database.py --move tackle
uv run python src/data/scripts/build_database.py --ability rough-skin
uv run python src/data/scripts/build_database.py --item leftovers
uv run python src/data/scripts/build_database.py --all-pokemon
uv run python src/data/scripts/build_database.py --all-moves
uv run python src/data/scripts/build_database.py --all-abilities
uv run python src/data/scripts/build_database.py --all-items
```

Pokémon learnsets are generated for the configured `champions` version-group
context. Item generation is currently a broad static catalog; it does not
claim to encode Pokémon Champions item availability or legality.

## Development

PokeCarlo requires Python 3.13 or newer. With `uv` installed, synchronize the
project environment with:

```bash
uv sync
```

Run the demonstration entry point after generated Pokémon data is available:

```bash
uv run python main.py
```

Run the complete test suite and lint check with:

```bash
uv run pytest
ruff check .
```

The tests use temporary JSON directories for database unit tests, so they do
not require ignored generated or raw data. They cover database parsing and
lookup, static model validation, set validation, stat calculation, move and
ability behavior, and battle flow.

## Planned work

Future work includes a cleaner application-level construction boundary for
resolving database names into a `PokemonSet`, a dedicated reconciliation of
static ability metadata with behavior-oriented ability classes, held-item
behavior and legality, and additional Pokémon Champions mechanics. Those
features are not implemented by the current runtime models.
