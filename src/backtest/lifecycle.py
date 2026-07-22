from enum import Enum, auto


class TradeState(Enum):
    """
    Trade lifecycle states.
    """

    WAIT = auto()

    ENTRY = auto()

    OPEN = auto()

    MANAGE = auto()

    EXIT = auto()

    CLOSED = auto()


class TradeLifecycle:
    """
    Controls trade state transitions.
    """

    def __init__(self):

        self.state = TradeState.WAIT

    def reset(self):

        self.state = TradeState.WAIT

    def entry(self):

        if self.state == TradeState.WAIT:

            self.state = TradeState.ENTRY

    def open(self):

        if self.state == TradeState.ENTRY:

            self.state = TradeState.OPEN

    def manage(self):

        if self.state == TradeState.OPEN:

            self.state = TradeState.MANAGE

    def exit(self):

        if self.state in (

            TradeState.OPEN,

            TradeState.MANAGE,

        ):

            self.state = TradeState.EXIT

    def close(self):

        if self.state == TradeState.EXIT:

            self.state = TradeState.CLOSED

    @property
    def is_waiting(self):

        return self.state == TradeState.WAIT

    @property
    def is_open(self):

        return self.state in (

            TradeState.OPEN,

            TradeState.MANAGE,

        )

    @property
    def is_closed(self):

        return self.state == TradeState.CLOSED

    def __repr__(self):

        return f"TradeLifecycle(state={self.state.name})"