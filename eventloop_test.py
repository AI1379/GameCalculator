from GenshinImpact.timeline import *

timeline = Timeline()


def interval_event_callback(event, timeline):
    print(timeline.current_time, event.stats["name"])
    timeline.push_event(event.reset_time(timeline.current_time + 10))


simple_event = Event(timeline, 0, {"name": "simple_event"})
scheduled_event1 = Event(timeline, 10, {
    "name": "event1"}, interval_event_callback)


def scheduled_event2_callback(event, timeline):
    print(timeline.current_time, event.stats["name"])
    timeline.push_event(scheduled_event1.reset_time(timeline.current_time + 5))
    timeline.push_event(simple_event.reset_time())


scheduled_event2 = Event(
    timeline, 20, {"name": "event2"}, scheduled_event2_callback)

listener1 = Listener(timeline)
listener1.listen(simple_event, lambda event, timeline: print(
    f"Listener1: {event.stats['name']}"))
listener1.listen(scheduled_event1, lambda event, timeline: print(
    f"Listener1: {event.stats['name']}"))

timeline.push_event(scheduled_event2)
timeline.start_emulate(100)
