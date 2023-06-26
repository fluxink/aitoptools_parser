import requests
from bs4 import BeautifulSoup

from load_django import *
from parser_app.models import Info, Link

class InfoParser:
    def __init__(self):
        pass

    def parse(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        name = soup.find("h2", class_="elementor-heading-title elementor-size-default").text
        url = soup.find("a", class_="jet-listing-dynamic-link__link").get("href")
        description = soup.find("p").text
        summary = soup.find("section", 
            class_="ob-is-breaking-bad elementor-section elementor-top-section elementor-element elementor-element-b3035da elementor-section-stretched elementor-section-boxed elementor-section-height-default elementor-section-height-default"
            ).find("div", class_="elementor-element elementor-element-ad4fb4c ob-harakiri-inherit ob-has-background-overlay elementor-widget elementor-widget-text-editor ob-harakiri").text
        key_features = ", ".join(
            [
                feature.text
                for feature in soup.find_all(
                    "a", class_="jet-listing-dynamic-terms__link"
                    ) if feature.get("href").startswith("https://aitoptools.com/features/")
            ]
        )
        media = soup.find("div", class_="jet-listing jet-listing-dynamic-image").find("img").get("src")
        rating = soup.find("div", class_="elementor-star-rating").get("title")
        tags = ", ".join(
            [
                tag.text
                for tag in soup.find(
                    "div", class_="elementor-element elementor-element-d100745 elementor-widget__width-auto ob-has-background-overlay elementor-widget elementor-widget-jet-listing-dynamic-terms"
                ).find_all("a", class_="jet-listing-dynamic-terms__link")
            ]
        )
        pricing = soup.find("div", class_="elementor-element elementor-element-b0321b7 ob-has-background-overlay elementor-widget elementor-widget-jet-listing-dynamic-field"
            ).find("div", class_="jet-listing-dynamic-field__content").text

        Info.objects.get_or_create(
            name=name,
            url=url,
            defaults={
                "description": description,
                "summary": summary,
                "key_features": key_features,
                "media": media,
                "rating": float(rating.split("/")[0]),
                "tags": tags,
                "pricing": pricing,
            },
        )


if __name__ == "__main__":
    parser = InfoParser()
    links = Link.objects.filter(parsed=False)
    for link in links:
        parser.parse(link.url)
        link.parsed = True
        link.save()
        print(f"Link {link.url} parsed successfully")
