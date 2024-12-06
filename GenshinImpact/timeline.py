from enum import Enum
import heapq


class EventType(Enum):
    ATTACK = 1
    REACTION = 2
    OTHER = 3


class Event:

    def __init__(self, type: EventType, time: int, **kwargs) -> None:
        self.type = type
        self.time = time
        self.kwargs = kwargs

    def __lt__(self, other):
        return self.time < other.time

    def callback(self, timeline):
        pass


class Timeline:
    def __init__(self) -> None:
        self.events = []
        self.current_time = 0

    # Note that time_ds is the time in deciseconds
    def start_emulate(self, time_ds):
        # TODO: Performance optimization can be done here
        for timestamp in range(time_ds):
            self.current_time = timestamp
            while self.events and self.events[0].time == timestamp:
                event = heapq.heappop(self.events)
                event.callback(self)

    def push_event(self, event: Event):
        heapq.heappush(self.events, event)
