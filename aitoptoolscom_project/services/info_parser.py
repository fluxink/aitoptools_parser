import time

import requests
from bs4 import BeautifulSoup

from load_django import *
from parser_app.models import Info, Link


class InfoParser:
    def __init__(self):
        pass

    def parse(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Got {response.status_code} status code for {url}")
            return
        soup = BeautifulSoup(response.text, "html.parser")

        name = soup.find(
            "h1", class_="elementor-heading-title elementor-size-default"
        ).text

        url = soup.find("a", class_="jet-listing-dynamic-link__link").get("href")

        try:
            description = soup.find("div", attrs={"data-id": "b333eef"}).text
        except AttributeError:
            description = None

        try:
            summary = soup.find(
                "div",
                attrs={
                    "data-widget_type": "text-editor.default",
                },
            ).text
        except AttributeError:
            summary = None

        key_features = ", ".join(
            [
                feature.text
                for feature in soup.find_all(
                    "a", class_="jet-listing-dynamic-terms__link"
                )
                if feature.get("href").startswith("https://aitoptools.com/features/")
            ]
        )

        try:
            media = (
                soup.find("div", attrs={"data-id": "9debe3e"}).find("img").get("data-src")
            )
        except AttributeError:
            media = None

        rating = soup.find("div", class_="elementor-star-rating").get("title")

        tags = ", ".join(
            [
                tag.text
                for tag in soup.find(
                    "div",
                    class_="elementor-element elementor-element-d100745 elementor-widget__width-auto ob-has-background-overlay elementor-widget elementor-widget-jet-listing-dynamic-terms",
                ).find_all("a", class_="jet-listing-dynamic-terms__link")
            ]
        )
        
        try:
            pricing = (
                soup.find(
                    "div",
                    class_="elementor-element elementor-element-b0321b7 ob-has-background-overlay elementor-widget elementor-widget-jet-listing-dynamic-field",
                )
                .find("div", class_="jet-listing-dynamic-field__content")
                .text
            )
        except AttributeError:
            pricing = None

        Info.objects.get_or_create(
            name=name.replace(" REVIEW", ""),
            url=url,
            defaults={
                "description": description,
                "summary": summary,
                "key_features": key_features or None,
                "media": media,
                "rating": float(rating.split("/")[0]),
                "tags": tags or None,
                "pricing": pricing,
            },
        )


if __name__ == "__main__":
    parser = InfoParser()
    links = Link.objects.filter(parsed=False)
    for link in links:
        time.sleep(0.2)
        parser.parse(link.url)
        link.parsed = True
        link.save()
        print(f"Link {link.url} parsed successfully")
