from django.contrib import admin
from .models import QueueEntry


@admin.register(QueueEntry)
class QueueEntryAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "service", "status", "created_at")
	list_filter = ("status", "service", "created_at")
	search_fields = ("name", "phone")
