from django.contrib import admin

from .models import Version


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ("id", "urn", "name", "metadata")
