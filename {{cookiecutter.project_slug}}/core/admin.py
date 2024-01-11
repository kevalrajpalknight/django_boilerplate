from django.contrib import admin

from core.models import Media


class CustomModelAdmin(admin.ModelAdmin):
    actions = []


class MediaAdmin(CustomModelAdmin):
    list_display = ["title", "file_path", "media_type"]

    def has_add_permission(self, request):
        return super().has_add_permission(request)


admin.site.register(Media, MediaAdmin)
