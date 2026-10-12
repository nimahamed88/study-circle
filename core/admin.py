from django.contrib import admin

from .models import Speaker, Subgroup, Session, SessionResource, Essay


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


class SessionResourceInline(admin.TabularInline):
    model = SessionResource
    extra = 1
    fields = ("title", "resource_type", "url", "file", "summary")

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("title", "start_time", "end_time", "session_type")
    list_filter = ("session_type",)
    ordering = ("start_time",)
    filter_horizontal = ("speakers", "subgroups")
    inlines = (SessionResourceInline,)
    exclude = ("pdf_file",)


@admin.register(Essay)
class EssayAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "status",
        "published_at",
        "updated_at",
    )

    list_filter = (
        "status",
        "subgroups",
        "published_at",
    )

    search_fields = (
        "title",
        "excerpt",
        "content",
        "author__name",
    )

    prepopulated_fields = {
        "slug": ("title",),
    }

    filter_horizontal = (
        "subgroups",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Essay details", {
            "fields": (
                "title",
                "slug",
                "author",
                "excerpt",
                "featured_image",
                "content",
            ),
        }),
        ("Organization", {
            "fields": (
                "subgroups",
                "status",
                "published_at",
            ),
        }),
        ("Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            ),
            "classes": ("collapse",),
        }),
    )

