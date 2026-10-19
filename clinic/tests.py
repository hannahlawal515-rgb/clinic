from django.test import TestCase

from django.test import TestCase
from django.urls import reverse

from .models import QueueEntry


class QueueDashboardTests(TestCase):
	def test_dashboard_shows_queue_counts(self):
		QueueEntry.objects.create(name="Waiting Patient")
		QueueEntry.objects.create(name="Patient In Service", status=QueueEntry.Status.CALLED)

		response = self.client.get(reverse("clinic:dashboard"))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Waiting Patient")
		self.assertContains(response, "Patient In Service")
		self.assertEqual(response.context["waiting_count"], 1)
		self.assertEqual(response.context["in_service_count"], 1)

	def test_call_next_calls_oldest_waiting_patient(self):
		first = QueueEntry.objects.create(name="First")
		second = QueueEntry.objects.create(name="Second")

		response = self.client.post(reverse("clinic:call_next"))

		first.refresh_from_db()
		second.refresh_from_db()
		self.assertRedirects(response, reverse("clinic:dashboard"))
		self.assertEqual(first.status, QueueEntry.Status.CALLED)
		self.assertEqual(second.status, QueueEntry.Status.WAITING)
		self.assertIsNotNone(first.called_at)

	def test_completed_patient_is_removed_from_active_queue(self):
		entry = QueueEntry.objects.create(name="Finished Patient", status=QueueEntry.Status.CALLED)

		self.client.post(reverse("clinic:update_status", args=(entry.pk, "complete")))

		entry.refresh_from_db()
		self.assertEqual(entry.status, QueueEntry.Status.COMPLETED)
		self.assertIsNotNone(entry.completed_at)
		self.assertNotContains(self.client.get(reverse("clinic:dashboard")), "Finished Patient")
		self.assertContains(self.client.get(reverse("clinic:dashboard") + "?status=completed"), "Finished Patient")

	def test_called_patient_can_return_to_waiting(self):
		entry = QueueEntry.objects.create(name="Returned Patient", status=QueueEntry.Status.CALLED)

		self.client.post(reverse("clinic:update_status", args=(entry.pk, "return")))

		entry.refresh_from_db()
		self.assertEqual(entry.status, QueueEntry.Status.WAITING)

	def test_add_patient_creates_queue_entry(self):
		response = self.client.post(reverse("clinic:add_patient"), {
			"name": "Taylor Morgan",
			"phone": "555-0100",
			"service": QueueEntry.Service.DENTAL,
		})

		self.assertRedirects(response, reverse("clinic:dashboard"))
		self.assertTrue(QueueEntry.objects.filter(name="Taylor Morgan", status=QueueEntry.Status.WAITING).exists())
