from datetime import datetime
from crontab import CronTab
from events.lib.DateBuilder import DateBuilder
from events.lib.event_requests import send_events, create_event, remove_event
from events.lib.load_resources import ResourceLoader
from os.path import join

def partition(array, low, high, cmp_items):
    pivot = cmp_items[high]
    i = low - 1
    for j in range(low, high):
        if cmp_items[j].less_than_equal(pivot):
            i = i + 1
            (cmp_items[i], cmp_items[j]) = (cmp_items[j], cmp_items[i])
            (array[i], array[j]) = (array[j], array[i])
    (cmp_items[i + 1], cmp_items[high]) = (cmp_items[high], cmp_items[i + 1])
    (array[i + 1], array[high]) = (array[high], array[i + 1])
    return i + 1

def quickSort(array, low, high, cmp_items):
    if low < high:
        pi = partition(array, low, high, cmp_items)
        quickSort(array, low, pi - 1, cmp_items)
        quickSort(array, pi + 1, high, cmp_items)

def sort_by(items: list, cmp_items: str):
    quickSort(items, 0, len(items) - 1, cmp_items)

def remove_expired(events, dates, expired_events):
    # sort then find youngest of oldest
    # cut at youngest
    sort_by(events, dates)
    # does not account for timezones
    # super lazy and incomplete method for switching from edt to pst
    # only implimented on csunas.org server
    # didn't feel like I needed to impliment a full solution
    # since this entire program is only a temporary fill in solution
    # use package pytz or build a subclass of tzinfo for a real solution
    # t= date.hour + (date.minute/100.0) - 3.0
    date = datetime.now()
    t= date.hour + (date.minute/100.0)
    i, n = 0, len(dates)
    while i < n and dates[i].get_year() <= date.year and (dates[i].get_month() < date.month or (dates[i].get_month() == date.month and (dates[i].get_day() < date.day or (dates[i].get_day() == date.day and dates[i].get_time()[-1] < t)))):
        i += 1
    if i > 0 and i < n:
        expired_events += events[:i]
        events = events[i:]
    elif i is n:
        expired_events += events
        events = []
    return events

def build_events(url, headers, events):
    # create event pages
    for event in events:
        create_event(url, headers, event)

def remove_events(events, headers):
    # remove event pages
    for event in events:
        remove_event(event, headers)

def schedule_next_run(date, command, id, user):
    # schedules the next time main.py will run
    with CronTab(user=user) as cron:
        for job in cron.find_comment(comment=id):
            cron.remove(job)
        job = cron.new(command=command, comment=id)
        _, time = date.get_time()
        # super bad and lazy and incomplete way of converting from edt to pst
        # these are school events so most of the time events will end before a rollover is necessary
        # if a rollover SHOULD happen just ignore it and let the remove_expired func handle it
        # not a universal solution
        # only implimented on csunas.org server
        # if time < 21.0:
        #     time += 3.0
        hr = int(time)
        min = int((time - float(hr)) * 100)
        job.setall(datetime(date.get_year(), date.get_month(), date.get_day(), hr, min))
        if job.is_valid():
            job.enable()
    return

def update(base_path):
    new_events_path = "new_events_path"
    events_path = "events_path"
    events = "events"
    new_events = "new_events"
    date = "date"
    should_update = "should_update"
    event_url = "event_url"
    create_event_url = "create_event_url"
    headers = "headers"
    expired_events = "expired_events"
    ZERO = 0
    
    # load new events into new events
    # load events we already know about into events
    resources = ResourceLoader(join(base_path, 'resources/resources.json'))
    resources.grab_put(base_path, new_events_path, new_events, events)
    resources.grab_put(base_path, events_path, events, events)
    
    # check if there are new events so we can added them to our list of know events
    resources.resources[should_update] = len(resources.resources[new_events]) > ZERO
    if resources.resources[should_update]:
        # remove new events that have already expired before adding them
        # to current event list
        # prevents us from building then immediatly deleting
        # new but expired page events
        dates = [DateBuilder(event[date]) for event in resources.resources[new_events]]
        resources.resources[new_events] = remove_expired(resources.resources[new_events], dates, [])
        # merge new and current events
        # still needs to be sorted
        resources.resources[events] = resources.resources[new_events] + resources.resources[events]

    # collecting dates as keys to sort events
    dates = [DateBuilder(event[date]) for event in resources.resources[events]]
    # sorts then removes expired events
    resources.resources[events] = remove_expired(resources.resources[events], dates, resources.resources[expired_events])

    # if there are still events make sure to schedule the newest
    # needs back up plan to check for new events when the
    # event list runs out
    # E.g. schedule it to run once every _hrs to check for new events
    # if len(resources.resources[events]) > ZERO:
    #     schedule_next_run(DateBuilder(resources.resources[events][ZERO][date]), "python3.7 ~/../home/Event_Manager/main.py", "next scheduled event", "root")

    # if there are new events or events that expired
    # then update the calendar/events page
    resources.resources[should_update] = resources.resources[should_update] or len(resources.resources[expired_events]) > ZERO
    if resources.resources[should_update]:
        resources.resources[should_update] = send_events(resources.resources[event_url], resources.resources[headers], resources.resources[events])
        # if the page was updated procced to
        # build new event pages,
        # remove expired event pages,
        # and update resources.json with current events then "new events" to be []
        # We do this to prevent loss of data when send_events fails
        if resources.resources[should_update]:
            build_events(resources.resources[create_event_url], resources.resources[headers], resources.resources[new_events])
            remove_events(resources.resources[expired_events], resources.resources[headers])
            resources.update(base_path, events_path, events, events)
            resources.resources[new_events] = []
            resources.update(base_path, new_events_path, new_events, events)
    return resources.resources[should_update]
