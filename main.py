from pokemon_species import PokemonSpecies
from utils import load_species_db


def main():
    species = load_species_db(path_to_json="./src/data/species.json")
    garchomp = PokemonSpecies.from_json(species["Garchomp"], name="Garchomp")
    rotom_heat = PokemonSpecies.from_json(species["Rotom-Heat"], name="Rotom-Heat")
    for pkmn in [garchomp, rotom_heat]:
        print(
            f"Loaded species {pkmn.name} with types {pkmn.types} and base stats:\nHP:\t{
                pkmn.base_stats.hp
            }\nAttack:\t{pkmn.base_stats.attack}\nDefense:\t{
                pkmn.base_stats.defense
            }\nSpecial Attack:\t{pkmn.base_stats.sp_attack}\nSpecial Defense:\t{
                pkmn.base_stats.sp_defense
            }\nSpeed:\t{pkmn.base_stats.speed}"
        )


if __name__ == "__main__":
    main()
