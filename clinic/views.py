from django.shortcuts import render

from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import QueueEntryForm
from .models import QueueEntry


def dashboard(request):
	today = timezone.localdate()
	todays_entries = QueueEntry.objects.filter(created_at__date=today)
	status_filter = request.GET.get("status", "active")

	if status_filter == "active":
		entries = todays_entries.exclude(status=QueueEntry.Status.COMPLETED)
	elif status_filter in QueueEntry.Status.values:
		entries = todays_entries.filter(status=status_filter)
	else:
		status_filter = "active"
		entries = todays_entries.exclude(status=QueueEntry.Status.COMPLETED)

	waiting_count = todays_entries.filter(status=QueueEntry.Status.WAITING).count()
	in_service_count = todays_entries.filter(status=QueueEntry.Status.CALLED).count()
	completed_count = todays_entries.filter(status=QueueEntry.Status.COMPLETED).count()
	next_patient = todays_entries.filter(status=QueueEntry.Status.WAITING).first()

	return render(request, "clinic/dashboard.html", {
		"entries": entries,
		"status_filter": status_filter,
		"waiting_count": waiting_count,
		"in_service_count": in_service_count,
		"completed_count": completed_count,
		"total_count": todays_entries.count(),
		"next_patient": next_patient,
		"today": today,
		"form": QueueEntryForm(),
	})


@require_POST
def add_patient(request):
	form = QueueEntryForm(request.POST)
	if form.is_valid():
		entry = form.save()
		messages.success(request, f"{entry.name} added to the queue.")
	else:
		messages.error(request, "Please check the patient details and try again.")
	return redirect("clinic:dashboard")


@require_POST
def update_status(request, entry_id, action):
	transitions = {
		"call": (QueueEntry.Status.WAITING, QueueEntry.Status.CALLED),
		"complete": ((QueueEntry.Status.WAITING, QueueEntry.Status.CALLED), QueueEntry.Status.COMPLETED),
		"return": (QueueEntry.Status.CALLED, QueueEntry.Status.WAITING),
	}
	if action not in transitions:
		return redirect("clinic:dashboard")

	entry = get_object_or_404(QueueEntry, pk=entry_id)
	allowed_statuses, new_status = transitions[action]
	if entry.status not in (allowed_statuses if isinstance(allowed_statuses, tuple) else (allowed_statuses,)):
		messages.warning(request, "That patient's status has already changed.")
		return redirect("clinic:dashboard")

	entry.status = new_status
	update_fields = ["status"]
	if new_status == QueueEntry.Status.CALLED:
		entry.called_at = timezone.now()
		update_fields.append("called_at")
	elif new_status == QueueEntry.Status.COMPLETED:
		entry.completed_at = timezone.now()
		update_fields.append("completed_at")
	entry.save(update_fields=update_fields)
	return redirect("clinic:dashboard")


@require_POST
def call_next(request):
	with transaction.atomic():
		entry = QueueEntry.objects.select_for_update().filter(
			created_at__date=timezone.localdate(),
			status=QueueEntry.Status.WAITING,
		).first()
		if entry:
			entry.status = QueueEntry.Status.CALLED
			entry.called_at = timezone.now()
			entry.save(update_fields=("status", "called_at"))
			messages.success(request, f"Now calling {entry.name}.")
		else:
			messages.info(request, "There are no patients waiting right now.")
	return redirect("clinic:dashboard")
