from django.contrib import admin
from . import models


@admin.register(models.Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "description",
    )


@admin.register(models.Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "content_id",
        "user_id",
    )
