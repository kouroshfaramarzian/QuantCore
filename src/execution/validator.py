from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ValidationResult:

    accepted: bool

    reason: str | None = None


class ExecutionValidator:

    """
    Validates an order before execution.
    """

    def validate(

        self,

        account,

        contract,

        risk,

        market,

    ) -> ValidationResult:

        if risk.volume <= 0:

            return ValidationResult(

                False,

                "Invalid volume",

            )

        if risk.entry is None:

            return ValidationResult(

                False,

                "Entry price missing",

            )

        if risk.stop_loss is None:

            return ValidationResult(

                False,

                "Stop loss missing",

            )

        if risk.take_profit is None:

            return ValidationResult(

                False,

                "Take profit missing",

            )

        if market.spread > contract.max_spread:

            return ValidationResult(

                False,

                "Spread too high",

            )

        if account.free_margin <= 0:

            return ValidationResult(

                False,

                "Insufficient margin",

            )

        return ValidationResult(True)