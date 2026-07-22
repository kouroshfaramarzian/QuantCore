from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Event:

    name: str

    timestamp: datetime

    payload: object