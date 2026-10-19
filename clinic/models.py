from django.db import models
from django.utils import timezone


class QueueEntry(models.Model):
	class Service(models.TextChoices):
		GENERAL = "general", "General care"
		PEDIATRICS = "pediatrics", "Pediatrics"
		DENTAL = "dental", "Dental"
		WOMENS_HEALTH = "womens_health", "Women's health"
		FOLLOW_UP = "follow_up", "Follow-up"

	class Status(models.TextChoices):
		WAITING = "waiting", "Waiting"
		CALLED = "called", "In service"
		COMPLETED = "completed", "Completed"

	name = models.CharField(max_length=120)
	phone = models.CharField(max_length=32, blank=True)
	service = models.CharField(max_length=24, choices=Service.choices, default=Service.GENERAL)
	status = models.CharField(max_length=12, choices=Status.choices, default=Status.WAITING)
	created_at = models.DateTimeField(default=timezone.now, editable=False)
	called_at = models.DateTimeField(null=True, blank=True, editable=False)
	completed_at = models.DateTimeField(null=True, blank=True, editable=False)

	class Meta:
		ordering = ("created_at", "id")

	def __str__(self):
		return f"#{self.pk or 'new'} {self.name}"

# Create your models here.
