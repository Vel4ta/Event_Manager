from datetime import datetime
from crontab import CronTab
from events.lib.DateBuilder import DateBuilder
from events.lib.event_requests import create_officer
from events.lib.page_data import Officer
from events.lib.load_resources import ResourceLoader
from events.lib.AVL_Tree import avl_tree, avl_find
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

def build_officers(url, headers, officers):
    # create event pages
    for officer in officers:
        create_officer(url, headers, officer)

# def remove_events(events, headers):
#     # remove event pages
#     for event in events:
#         remove_event(event, headers)

def update(base_path):
    officers_path = "officers_path"
    officers_update_path = "officers_update_path"
    officers = "officers"
    officers_to_update = "officers_to_update"
    officer_url = "officer_url"
    create_officer_url = "create_officer_url"
    update_officer_url = "update_officer_url"
    headers = "headers"
    title = "title"
    should_update = "should_update"
    ZERO = 0
    
    resources = ResourceLoader(join(base_path, 'resources/resources.json'))
    resources.grab_put(base_path, officers_update_path, officers_to_update, officers)
    resources.grab_put(base_path, officers_path, officers, officers)

    if resources.resources[officers_to_update].len() > 0:
        (search_tree, t_root) = avl_tree(resources.resources[officers], title)
        for officer in resources.resources[officers_to_update]:
            officer_index = avl_find(search_tree, t_root, resources.resources[officers], officer, title)
            if officer_index < 0:
                if not create_officer(resources.resources[create_officer_url], resources.resources[headers], officer):
                    print("failed to update", officer)
                    return False
                resources.resources[officers].push(officer)
                continue

            for key in officer.keys():
                resources.resources[officers][officer_index][key] = officer[key]
            if not create_officer(resources.resources[update_officer_url] + Officer(resources.resources[officers][officer_index]).makeAlias(), resources.resources[headers], resources.resources[officers][officer_index]):
                print("failed to update", officer)
                return False
        
        resources.update(base_path, officers_update_path, officers_to_update, officers)
        resources.update(base_path, officers_path, officers, officers)
    
    return True
