import requests
from bs4 import BeautifulSoup

from load_django import *
from parser_app.models import Link


class LinkParser:
    def __init__(self):
        self.url = "https://aitoptools.com/"

    def parse(self):
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "en-US,en;q=0.9,ru;q=0.8,ru-RU;q=0.7,pl-PL;q=0.6,pl;q=0.5,uk-UA;q=0.4,uk;q=0.3",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest",
        }
        data = {
            "action": "jet_engine_ajax",
            "handler": "listing_load_more",
            "query[post_status][]": "publish",
            "query[post_type][]": "tool",
            "query[posts_per_page]": "12",
            "query[paged]": "1",
            "query[ignore_sticky_posts]": "1",
            "query[orderby]": "meta_value_num",
            "query[meta_key]": "popularity",
            "query[meta_type]": "NUMERIC",
            "query[suppress_filters]": "false",
            "query[jet_smart_filters]": "jet-engine/default",
            "widget_settings[lisitng_id]": "43",
            "widget_settings[posts_num]": "12",
            "widget_settings[columns]": "3",
            "widget_settings[columns_tablet]": "2",
            "widget_settings[columns_mobile]": "1",
            "widget_settings[is_archive_template]": "",
            "widget_settings[post_status][]": "publish",
            "widget_settings[use_random_posts_num]": "",
            "widget_settings[max_posts_num]": "9",
            "widget_settings[not_found_message]": "No data was found",
            "widget_settings[is_masonry]": "false",
            "widget_settings[equal_columns_height]": "yes",
            "widget_settings[use_load_more]": "yes",
            "widget_settings[load_more_id]": "",
            "widget_settings[load_more_type]": "scroll",
            "widget_settings[load_more_offset][unit]": "px",
            "widget_settings[load_more_offset][size]": "1000",
            "widget_settings[use_custom_post_types]": "yes",
            "widget_settings[custom_post_types][]": "tool",
            "widget_settings[hide_widget_if]": "",
            "widget_settings[carousel_enabled]": "",
            "widget_settings[slides_to_scroll]": "1",
            "widget_settings[arrows]": "true",
            "widget_settings[arrow_icon]": "fa fa-angle-left",
            "widget_settings[dots]": "",
            "widget_settings[autoplay]": "true",
            "widget_settings[autoplay_speed]": "5000",
            "widget_settings[infinite]": "true",
            "widget_settings[center_mode]": "",
            "widget_settings[effect]": "slide",
            "widget_settings[speed]": "500",
            "widget_settings[inject_alternative_items]": "",
            "widget_settings[scroll_slider_enabled]": "",
            "widget_settings[scroll_slider_on][]": "desktop",
            "widget_settings[scroll_slider_on][]": "tablet",
            "widget_settings[scroll_slider_on][]": "mobile",
            "widget_settings[custom_query]": "false",
            "widget_settings[custom_query_id]": "",
            "widget_settings[_element_id]": "",
            "page_settings[post_id]": "false",
            "page_settings[queried_id]": "false",
            "page_settings[element_id]": "false",
            "page_settings[page]": 1,
            "listing_type": "false",
            "isEditMode": "false",
            "addedPostCSS[]": "43",
            "jb_current_locale": "en_US",
        }
        page = 1
        while True:
            print(f"Parse page {page}")
            data["page_settings[page]"] = page
            response = requests.post(self.url, headers=headers, data=data)
            json_data = response.json()

            if response.status_code != 200 or json_data["success"] == False:
                print("Request error")
                break
            elif json_data["data"]["html"] == "":
                print("No more pages")
                break

            soup = BeautifulSoup(json_data["data"]["html"], "html.parser")

            aitools_links = [
                link.get("href")
                for link in soup.find_all("a", class_="elementor-icon")
                if link.get("href").startswith("https://aitoptools.com/")
            ]
            aitools_names = [
                element.text
                for element in soup.find_all(
                    "h2", class_="elementor-heading-title elementor-size-default"
                )
            ]

            for name, link in zip(aitools_names, aitools_links):
                Link.objects.get_or_create(name=name, url=link)

            page += 1


if __name__ == "__main__":
    parser = LinkParser()
    parser.parse()
