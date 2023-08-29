from requests import get as rget, post as rpost
from events.lib.page_data import form_update, event_form, get_page_url, get_delete_url, delete_event

def get(url, headers) -> str or None:
    r = rget(url=url, headers=headers)
    if r.status_code == 200:
        return r.text
    else:
        return None

def post(url, headers, data) -> bool:
    if data:
        return rpost(url=url, headers=headers, data=data).status_code == 200
    return False

def send_events(url, headers, data) -> bool:
    # update calendar/events page
    text = get(url, headers)
    data = form_update(text, data)
    return post(url, headers, data)

def create_event(url, headers, data) -> bool:
    # make an event page
    text = get(url, headers)
    data = event_form(text, data)
    return post(url, headers, data)

def remove_event(event, headers) -> bool:
    # remove an event page
    url = get_delete_url(get(get_page_url(event), headers))
    if url == None:
        return False
    text = get(url, headers)
    data = delete_event(text)
    return post(url, headers, data)