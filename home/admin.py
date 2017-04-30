from django.contrib import admin
from .models import *


# Register your models here.

class PostModelAdmin(admin.ModelAdmin):
    list_display = ["pname", "created_at", "updated_at"]
    list_display_links = ["updated_at"]
    list_editable = ["pname"]
    list_filter = ["created_at", "updated_at"]

    search_fields = ["pname"]

    class Meta:
        model = Projects


admin.site.register(Projects)
