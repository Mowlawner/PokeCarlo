import pytest

from battle.battle_state import BattleState


def test_player_party_must_contain_active_pokemon(garchomp, gyarados):
    with pytest.raises(ValueError):
        BattleState(
            player_active=(garchomp,),
            opponent_active=(gyarados,),
            player_party=(gyarados,),
            opponent_party=(gyarados,),
        )


def test_opponent_party_must_contain_active_pokemon(garchomp, gyarados):
    with pytest.raises(ValueError):
        BattleState(
            player_active=(garchomp,),
            opponent_active=(gyarados,),
            player_party=(garchomp,),
            opponent_party=(garchomp,),
        )


def test_player_party_cannot_contain_duplicates(garchomp):
    with pytest.raises(ValueError):
        BattleState(
            player_active=(garchomp,),
            opponent_active=(garchomp,),
            player_party=(garchomp, garchomp),
            opponent_party=(garchomp,),
        )


def test_opponent_party_cannot_contain_duplicates(garchomp):
    with pytest.raises(ValueError):
        BattleState(
            player_active=(garchomp,),
            opponent_active=(garchomp,),
            player_party=(garchomp,),
            opponent_party=(garchomp, garchomp),
        )


def test_player_active_must_be_member_of_party(garchomp, gyarados):
    state = BattleState(
        player_active=(garchomp,),
        opponent_active=(gyarados,),
        player_party=(garchomp, gyarados),
        opponent_party=(gyarados,),
    )

    assert garchomp in state.player_party


def test_opponent_active_must_be_member_of_party(garchomp, gyarados):
    state = BattleState(
        player_active=(garchomp,),
        opponent_active=(gyarados,),
        player_party=(garchomp,),
        opponent_party=(gyarados, garchomp),
    )

    assert gyarados in state.opponent_party


def test_switching_does_not_modify_player_party(garchomp, gyarados, opponent_garchomp):
    state = BattleState(
        player_active=(garchomp,),
        opponent_active=(opponent_garchomp,),
        player_party=(garchomp, gyarados),
        opponent_party=(opponent_garchomp,),
    )

    original_party = state.player_party

    state.replace_active(
        outgoing=garchomp,
        incoming=gyarados,
    )

    assert state.player_party == original_party
    assert state.player_active == (gyarados,)


def test_switching_does_not_modify_opponent_party(
    garchomp, gyarados, opponent_garchomp
):
    state = BattleState(
        player_active=(garchomp,),
        opponent_active=(gyarados,),
        player_party=(garchomp,),
        opponent_party=(gyarados, opponent_garchomp),
    )

    original_party = state.opponent_party

    state.replace_active(
        outgoing=gyarados,
        incoming=opponent_garchomp,
    )

    assert state.opponent_party == original_party
    assert state.opponent_active == (opponent_garchomp,)
