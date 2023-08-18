from bs4 import BeautifulSoup

def makeAlias(og):
    info = og
    return "/as/events/" + info.replace("(", "").replace(")", "").replace("-", "").replace(":", "").replace("&", "").replace("  ", " ").replace(" ", "-").replace('"', '\"')
def makeLink(link, text):
    return "<a href=\"" + link + "\">" + text + "</a>"
def makeTitle(info):
    return "<h2>" + makeLink(makeAlias(info), info) + "</h2>\n"
def makeDate(info):
    return "<h3>" + info.split(",12:00am", 1)[0] + "</h3>\n"
def makeLocation(info):
    if not ("" is info):
        return "<h4>" + info + "</h4>\n"
    else:
        return info
def makeCost(info):
    if not (0 == info):
        return "<h5>cost: $" + str(info) + "</h5>\n"
    else:
        return ""
def makeRegistration(info):
    if not ("" is info):
        return "<p>" + makeLink(info, "Registration") + "</p>\n"
    else:
        return info
def makeLede(info):
    return "<p>" + info + "</p>\n"
def makeReadMore(info):
    return makeLink(makeAlias(info), "Read more\n\n")
def makeBody(info):
    return "<p>" + info + "</p>\n"


class Builder:
    
    def __init__(self, event: dict):
        self.event = event
    
    def display(self) -> str:
        ops = {
            "title": makeTitle,
            "date": makeDate,
            "lede": makeLede
        }
        o = ""
        for key in ops.keys():
            o += ops[key](self.event[key])
        o += makeReadMore(self.event["title"])
        return o

    def full_display(self) -> str:
        ops = {
            "title": makeTitle,
            "date": makeDate,
            "location": makeLocation,
            "cost": makeCost,
            "registration": makeRegistration,
            "body": makeBody
        }
        o = ""
        for key in ops.keys():
            o += ops[key](self.event[key])
        return o

def get_value(item):
    try:
        value = item["value"]
    except:
        return get_innertext(item)
    else:
        return value

def get_innertext(item):
    try:
        text = ""
        for word in item.contents:
            text += word
        return text
    except:
        t = list(item.children) if not (item.children == None) else []
        if len(t) > 0:
            return get_value(t[0])
        else:
            return ""

def new_events(events):
    def add_content(_):
        out = ""
        for event in events:
            out += Builder(event).display()
        return out
    return add_content

def form_update(text, events):
    # the calendar/events page
    if text == None:
        return text
    full_page_form_data = {
    "changed": get_value,
    "title[0][value]": get_value,
    "form_build_id": get_value,
    "form_token": get_value,
    "form_id": get_value,
    "field_heading[0][value]": get_value,
    "field_fw_hero_bg_image[selection][0][target_id]": get_value,
    "field_fw_hero_bg_image[media_library_selection]": get_value,
    "field_fw_hero_video[media_library_selection]": get_value,
    "field_hero_modal_title[0][value]": get_value,
    "field_hero_modal_content[0][value]": get_value,
    "field_fw_section_nav[0][uri]": get_value,
    "field_fw_section_nav[0][title]": get_value,
    "field_fw_section_nav[0][_weight]": get_value,
    "body[0][value]": new_events(events),
    "body[0][format]": lambda _: "basic_html",
    "field_full_width_modules[add_more][add_more_delta]": get_value,
    "revision_log[0][value]": get_innertext,
    "menu[enabled]": get_value, 
    "menu[menu_parent]": lambda _: "group-navigation:menu_link_content:bbee995f-95a1-4f48-85c7-d5d705c20d9d",
    "menu[title]": get_value,
    "menu[description]": get_value,
    "menu[weight]": get_value,
    "field_meta_tags[0][basic][title]": get_value,
    "field_meta_tags[0][basic][description]": get_value,
    "field_meta_tags[0][basic][abstract]": get_value,
    "field_meta_tags[0][basic][keywords]": get_value,
    "field_meta_tags[0][open_graph][og_determiner]": get_value,
    "field_meta_tags[0][open_graph][og_site_name]": get_value,
    "field_meta_tags[0][open_graph][og_type]": get_value,
    "field_meta_tags[0][open_graph][og_url]": get_value,
    "field_meta_tags[0][open_graph][og_title]": get_value,
    "field_meta_tags[0][open_graph][og_description]": get_value,
    "field_meta_tags[0][open_graph][og_image]": get_value,
    "field_meta_tags[0][open_graph][og_video]": get_value,
    "field_meta_tags[0][open_graph][og_image_url]": get_value,
    "field_meta_tags[0][open_graph][og_image_secure_url]": get_value,
    "field_meta_tags[0][open_graph][og_video_secure_url]": get_value,
    "field_meta_tags[0][open_graph][og_image_type]": get_value,
    "field_meta_tags[0][open_graph][og_video_type]": get_value,
    "field_meta_tags[0][open_graph][og_image_width]": get_value,
    "field_meta_tags[0][open_graph][og_video_width]": get_value,
    "field_meta_tags[0][open_graph][og_image_height]": get_value,
    "field_meta_tags[0][open_graph][og_video_height]": get_value,
    "field_meta_tags[0][open_graph][og_image_alt]": get_value,
    "field_meta_tags[0][open_graph][og_updated_time]": get_value,
    "field_meta_tags[0][open_graph][og_video_duration]": get_value,
    "field_meta_tags[0][open_graph][og_latitude]": get_value,
    "field_meta_tags[0][open_graph][og_longitude]": get_value,
    "field_meta_tags[0][open_graph][og_see_also]": get_value,
    "field_meta_tags[0][open_graph][og_street_address]": get_value,
    "field_meta_tags[0][open_graph][og_locality]": get_value,
    "field_meta_tags[0][open_graph][og_region]": get_value,
    "field_meta_tags[0][open_graph][og_postal_code]": get_value,
    "field_meta_tags[0][open_graph][og_country_name]": get_value,
    "field_meta_tags[0][open_graph][og_email]": get_value,
    "field_meta_tags[0][open_graph][og_phone_number]": get_value,
    "field_meta_tags[0][open_graph][og_fax_number]": get_value,
    "field_meta_tags[0][open_graph][og_locale]": get_value,
    "field_meta_tags[0][open_graph][og_locale_alternative]": get_value,
    "field_meta_tags[0][open_graph][article_author]": get_value,
    "field_meta_tags[0][open_graph][article_publisher]": get_value,
    "field_meta_tags[0][open_graph][article_section]": get_value,
    "field_meta_tags[0][open_graph][article_tag]": get_value,
    "field_meta_tags[0][open_graph][article_published_time]": get_value,
    "field_meta_tags[0][open_graph][article_modified_time]": get_value,
    "field_meta_tags[0][open_graph][article_expiration_time]": get_value,
    "field_meta_tags[0][open_graph][book_author]": get_value,
    "field_meta_tags[0][open_graph][book_isbn]": get_value,
    "field_meta_tags[0][open_graph][book_release_date]": get_value,
    "field_meta_tags[0][open_graph][book_tag]": get_value,
    "field_meta_tags[0][open_graph][og_audio]": get_value,
    "field_meta_tags[0][open_graph][og_audio_secure_url]": get_value,
    "field_meta_tags[0][open_graph][og_audio_type]": get_value,
    "field_meta_tags[0][open_graph][profile_first_name]": get_value,
    "field_meta_tags[0][open_graph][profile_last_name]": get_value,
    "field_meta_tags[0][open_graph][profile_gender]": get_value,
    "field_meta_tags[0][open_graph][profile_username]": get_value,
    "field_meta_tags[0][open_graph][video_actor]": get_value,
    "field_meta_tags[0][open_graph][video_actor_role]": get_value,
    "field_meta_tags[0][open_graph][video_director]": get_value,
    "field_meta_tags[0][open_graph][video_release_date]": get_value,
    "field_meta_tags[0][open_graph][video_series]": get_value,
    "field_meta_tags[0][open_graph][video_tag]": get_value,
    "field_meta_tags[0][open_graph][video_writer]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_type]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_description]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_site]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_title]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_site_id]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_creator]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_creator_id]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_donottrack]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_page_url]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_image]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_image_alt]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_image_height]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_image_width]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_gallery_image0]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_gallery_image1]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_gallery_image2]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_gallery_image3]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_app_store_country]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_app_name_iphone]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_app_id_iphone]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_app_url_iphone]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_app_name_ipad]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_app_id_ipad]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_app_url_ipad]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_app_name_googleplay]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_app_id_googleplay]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_app_url_googleplay]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_player]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_player_width]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_player_height]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_player_stream]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_player_stream_content_type]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_label1]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_data1]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_label2]": get_value,
    "field_meta_tags[0][twitter_cards][twitter_cards_data2]": get_value,
    "path[0][pathauto]": lambda _: "/as/events",
    "moderation_state[0][state]": lambda _: "published",
    "op": lambda _: "Save"
    }
    
    soup = BeautifulSoup(text, "lxml")
    for key in full_page_form_data.keys():
        full_page_form_data[key] = full_page_form_data[key](soup.select_one('[name="' + key + '"]'))
    return full_page_form_data


def build_event(event):
    def add_content(_):
        return Builder(event).full_display()
    return add_content

def event_form(text, event):
    # an event page
    if text == None:
        return text
    form_data = {
        "title[0][value]": lambda _: event["title"],
        "changed": get_value,
        "form_build_id": get_value,
        "form_token": get_value,
        "form_id": get_value,
        "field_prg_content[0][value]": build_event(event),
        "field_prg_content[0][format]": lambda _: "basic_html",
        "revision_log[0][value]": get_innertext,
        "path[0][alias]": lambda _: makeAlias(event["title"]),
        "op": lambda _: "Save"
    }
    soup = BeautifulSoup(text, "lxml")
    for key in form_data.keys():
        form_data[key] = form_data[key](soup.select_one('[name="' + key + '"]'))
    return form_data


def get_page_url(event):
    return "https://live-csu-northridge.pantheonsite.io" + makeAlias(event["title"])

def get_delete_url(text):
    soup = BeautifulSoup(text, "lxml")
    return "https://live-csu-northridge.pantheonsite.io" + soup.select_one('[data-drupal-link-system-path*="/delete"]')["href"]

def delete_event(text):
    if text == None:
        return text
    form_data = {
        "confirm": lambda _: "1",
        "form_build_id": get_value,
        "form_token": get_value,
        "form_id": get_value,
        "op": lambda _: "Delete"
    }
    soup = BeautifulSoup(text, "lxml")
    for key in form_data.keys():
        form_data[key] = form_data[key](soup.select_one('[name="' + key + '"]'))
    return form_data