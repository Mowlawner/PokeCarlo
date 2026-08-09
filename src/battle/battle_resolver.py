from battle.action import Action
from battle.battle_context import BattleContext
from move.move import MoveExecutionResult


class BattleResolver:
    def __init__(self, context: BattleContext):
        self.context = context

    def resolve_turn(
        self,
        actions: tuple[Action, ...],
    ) -> tuple[tuple[Action, MoveExecutionResult | None], ...]:
        """
        Resolve all actions for a single battle turn.

        Actions are executed in priority order, with speed used as a
        tiebreaker. Fainted Pokémon are marked for replacement after each
        action and again after all actions complete.

        Pending forced switches are detected after resolution, but actual
        replacement selection is handled elsewhere.

        Returns:
            Action/result pairs in the order the actions were resolved. Actions
            that do not produce a move execution result return ``None``.
        """
        remaining_actions = list(actions)
        execution_results: list[tuple[Action, MoveExecutionResult | None]] = []

        while remaining_actions:
            action = self.get_next_action(remaining_actions)
            remaining_actions.remove(action)

            execution_results.append((action, action.apply(self.context)))

            self.handle_faints()

        self.handle_faints()
        self.handle_pending_switches()

        return tuple(execution_results)

    def get_next_action(
        self,
        actions: list[Action],
    ) -> Action:
        """
        Return the next action to execute.

        Actions are ordered first by priority, then by the acting Pokémon's
        speed.
        """
        return max(
            actions,
            key=lambda action: (
                action.priority,
                action.speed_tiebreaker(),
            ),
        )

    def handle_faints(self) -> None:
        """
        Add newly fainted active Pokémon to the pending switch queue.

        Pending switches are not immediately resolved because replacement
        selection is a separate decision made after action resolution.
        """
        for pokemon in (
            *self.context.state.player_active,
            *self.context.state.opponent_active,
        ):
            if pokemon.is_fainted and not self.context.state.has_pending_switch(
                pokemon
            ):
                self.context.state.add_pending_switch(pokemon)

    def handle_pending_switches(self) -> None:
        """
        Process Pokémon waiting for replacement.

        Replacement selection is handled outside the resolver. This method exists
        as the resolution point after a turn completes.
        """
        return
