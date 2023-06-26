from django.contrib import admin
from parser_app.models import Info, Link


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "parsed")
    list_filter = ("parsed",)
    search_fields = ("name", "url")


@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "url",
        "description",
        "summary",
        "key_features",
        "media",
        "rating",
        "tags",
        "pricing",
    )
    list_filter = ("rating",)
    search_fields = ("name", "tags")
