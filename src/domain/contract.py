from dataclasses import dataclass


@dataclass(slots=True)
class ContractSpecification:

    symbol: str

    contract_size: float

    lot_size: float

    tick_size: float

    tick_value: float

    digits: int

    max_spread: float