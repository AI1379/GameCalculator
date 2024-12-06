from enum import Enum
from typing import Dict, List, Callable
import heapq
import copy


class Event:
    unique_id_counter = 0

    def __init__(self, timeline, time: int = 0,  stats: dict = {}, callback=None) -> None:
        Event.unique_id_counter += 1
        self.id = Event.unique_id_counter
        self.timeline = timeline
        self.time = time if time != 0 else timeline.current_time
        self.stats = stats
        self.callback = callback

    def __lt__(self, other):
        return self.time < other.time

    def reset_time(self, time: int = 0):
        cp = copy.deepcopy(self)
        cp.time = time if time != 0 else self.timeline.current_time
        return cp


# The listener listens to the event and pushes the event to the timeline


class Listener:
    def __init__(self, timeline) -> None:
        self.timeline = timeline
        timeline.listeners.append(self)
        self.listening = []

    def listen(self, event, callback):
        if isinstance(event, Event):
            self.listening.append((lambda x: x.id == event.id, callback))
        else:
            self.listening.append((event, callback))

    def emit(self, event):
        for condition, callback in self.listening:
            if condition(event):
                callback(event, self.timeline)


class Timeline:
    def __init__(self) -> None:
        self.events = []
        self.current_time = 0
        self.stats = {}
        self.listeners = []

    # Note that time_ds is the time in deciseconds
    def start_emulate(self, time_ds: int):
        # TODO: Performance optimization can be done here
        while self.events:
            event = heapq.heappop(self.events)
            if event.time < self.current_time:
                continue
            self.current_time = event.time
            if self.current_time > time_ds:
                break
            if event.callback:
                event.callback(event, self)
            for listener in self.listeners:
                listener.emit(event)

    def push_event(self, event: Event):
        heapq.heappush(self.events, event)

    def init_schedule(self, events: List[Event]):
        self.events = copy.deepcopy(events)
        heapq.heapify(self.events)
