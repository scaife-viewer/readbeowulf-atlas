from django.contrib import admin

from .models import Fitt, HalfLine, Line, Paragraph, Token, Version


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ("id", "urn", "name", "metadata")


@admin.register(Fitt)
class Fitt(admin.ModelAdmin):
    list_display = ("id", "position", "idx", "version",)
    list_filter = ("version",)


@admin.register(Paragraph)
class ParagraphAdmin(admin.ModelAdmin):
    list_display = ("id", "position", "idx", "fitt", "version",)
    list_filter = ("fitt", "version",)


@admin.register(Line)
class LineAdmin(admin.ModelAdmin):
    list_display = ("id", "position", "idx", "paragraph", "fitt", "version",)
    list_filter = ("paragraph", "fitt", "version",)


@admin.register(HalfLine)
class HalfLineAdmin(admin.ModelAdmin):
    list_display = ("id", "position", "idx", "line", "paragraph", "fitt", "version",)
    list_filter = ("line", "paragraph", "fitt", "version",)


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "position",
        "idx",
        "pre_punctuation",
        "text_content",
        "post_punctuation",
        "syntax",
        "parse",
        "lemma",
        "part_of_speech",
        "o",
        "gloss",
        "with_length",
        "first_in_paragraph",
        "non_verse",
        "caesura_boundary",
        "halfline",
        "line",
        "paragraph",
        "fitt",
        "version",
    )
    list_filter = ("halfline", "line", "paragraph", "fitt", "version",)
