from django.contrib import admin

from .models import Speaker, Subgroup, Session


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "title",
        "email",
    )

    search_fields = (
        "name",
        "title",
        "bio",
        "email",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }


@admin.register(Subgroup)
class SubgroupAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "head",
        "email",
    )

    search_fields = (
        "name",
        "description",
        "email",
    )

    filter_horizontal = (
        "members",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("title", "start_time", "end_time", "session_type")
    list_filter = ("session_type",)
    ordering = ("start_time",)
    filter_horizontal = ("speakers", "subgroups")

    ordering = (
        "start_time",
    )