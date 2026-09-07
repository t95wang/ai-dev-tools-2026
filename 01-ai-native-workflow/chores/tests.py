from datetime import date

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Chore


class ChoreLifecycleTests(TestCase):
    def create_chore(self, **overrides):
        values = {
            "title": "Wash dishes",
            "description": "Clean and put away the dinner dishes.",
            "due_date": date(2027, 1, 15),
        }
        values.update(overrides)
        return Chore.objects.create(**values)

    def test_create_chore_successfully(self):
        response = self.client.post(
            reverse("chores:create"),
            {
                "title": "Take out recycling",
                "description": "Move the blue bin to the curb.",
                "due_date": "2027-02-01",
            },
        )

        self.assertRedirects(response, reverse("chores:list"))
        chore = Chore.objects.get(title="Take out recycling")
        self.assertEqual(chore.description, "Move the blue bin to the curb.")
        self.assertEqual(chore.due_date, date(2027, 2, 1))
        self.assertEqual(chore.status, Chore.Status.UNCLAIMED)
        self.assertIsNone(chore.claimed_by)
        self.assertIsNone(chore.claimed_at)
        self.assertIsNone(chore.completed_by)
        self.assertIsNone(chore.completed_at)

    def test_reject_invalid_chore_creation(self):
        response = self.client.post(
            reverse("chores:create"),
            {
                "title": "Take out recycling",
                "description": "Move the blue bin to the curb.",
                "due_date": "not-a-date",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "due_date",
            "Enter a valid date.",
        )
        self.assertEqual(Chore.objects.count(), 0)

    def test_list_displays_chore_details_and_creation_link(self):
        self.create_chore()

        response = self.client.get(reverse("chores:list"))

        self.assertContains(response, "Wash dishes")
        self.assertContains(response, "Clean and put away the dinner dishes.")
        self.assertContains(response, "Jan. 15, 2027")
        self.assertContains(response, "Status: Unclaimed")
        self.assertContains(response, "Available to claim")
        self.assertContains(response, reverse("chores:create"))

    def test_claim_unclaimed_chore(self):
        chore = self.create_chore()
        before_claim = timezone.now()

        response = self.client.post(
            reverse("chores:claim", args=[chore.pk]),
            {"name": "Alex"},
        )

        self.assertRedirects(response, reverse("chores:list"))
        chore.refresh_from_db()
        self.assertEqual(chore.status, Chore.Status.CLAIMED)
        self.assertEqual(chore.claimed_by, "Alex")
        self.assertIsNotNone(chore.claimed_at)
        self.assertGreaterEqual(chore.claimed_at, before_claim)
        self.assertIsNone(chore.completed_by)
        self.assertIsNone(chore.completed_at)

    def test_reject_invalid_claim_form(self):
        chore = self.create_chore()

        response = self.client.post(
            reverse("chores:claim", args=[chore.pk]),
            {"name": ""},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "name", "This field is required.")
        chore.refresh_from_db()
        self.assertEqual(chore.status, Chore.Status.UNCLAIMED)
        self.assertIsNone(chore.claimed_by)
        self.assertIsNone(chore.claimed_at)

    def test_reject_repeated_and_completed_chore_claims(self):
        claimed_at = timezone.now()
        claimed = self.create_chore(
            title="Vacuum",
            status=Chore.Status.CLAIMED,
            claimed_by="Alex",
            claimed_at=claimed_at,
        )
        completed = self.create_chore(
            title="Mop floor",
            status=Chore.Status.COMPLETED,
            claimed_by="Blair",
            claimed_at=claimed_at,
            completed_by="Casey",
            completed_at=timezone.now(),
        )

        for chore in (claimed, completed):
            response = self.client.post(
                reverse("chores:claim", args=[chore.pk]),
                {"name": "Someone else"},
            )
            self.assertRedirects(response, reverse("chores:list"))

        claimed.refresh_from_db()
        completed.refresh_from_db()
        self.assertEqual(claimed.status, Chore.Status.CLAIMED)
        self.assertEqual(claimed.claimed_by, "Alex")
        self.assertEqual(claimed.claimed_at, claimed_at)
        self.assertEqual(completed.status, Chore.Status.COMPLETED)
        self.assertEqual(completed.claimed_by, "Blair")
        self.assertEqual(completed.claimed_at, claimed_at)

    def test_complete_claimed_chore(self):
        claimed_at = timezone.now()
        chore = self.create_chore(
            status=Chore.Status.CLAIMED,
            claimed_by="Alex",
            claimed_at=claimed_at,
        )
        before_completion = timezone.now()

        response = self.client.post(
            reverse("chores:complete", args=[chore.pk]),
            {"name": "Blair"},
        )

        self.assertRedirects(response, reverse("chores:list"))
        chore.refresh_from_db()
        self.assertEqual(chore.status, Chore.Status.COMPLETED)
        self.assertEqual(chore.completed_by, "Blair")
        self.assertIsNotNone(chore.completed_at)
        self.assertGreaterEqual(chore.completed_at, before_completion)
        self.assertEqual(chore.claimed_by, "Alex")
        self.assertEqual(chore.claimed_at, claimed_at)

    def test_reject_invalid_completion_form(self):
        chore = self.create_chore(
            status=Chore.Status.CLAIMED,
            claimed_by="Alex",
            claimed_at=timezone.now(),
        )

        response = self.client.post(
            reverse("chores:complete", args=[chore.pk]),
            {"name": ""},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "name", "This field is required.")
        chore.refresh_from_db()
        self.assertEqual(chore.status, Chore.Status.CLAIMED)
        self.assertIsNone(chore.completed_by)
        self.assertIsNone(chore.completed_at)

    def test_reject_unclaimed_and_repeated_completions(self):
        unclaimed = self.create_chore(title="Dust shelves")
        completed_at = timezone.now()
        completed = self.create_chore(
            title="Clean bathroom",
            status=Chore.Status.COMPLETED,
            claimed_by="Alex",
            claimed_at=timezone.now(),
            completed_by="Blair",
            completed_at=completed_at,
        )

        for chore in (unclaimed, completed):
            response = self.client.post(
                reverse("chores:complete", args=[chore.pk]),
                {"name": "Someone else"},
            )
            self.assertRedirects(response, reverse("chores:list"))

        unclaimed.refresh_from_db()
        completed.refresh_from_db()
        self.assertEqual(unclaimed.status, Chore.Status.UNCLAIMED)
        self.assertIsNone(unclaimed.completed_by)
        self.assertIsNone(unclaimed.completed_at)
        self.assertEqual(completed.status, Chore.Status.COMPLETED)
        self.assertEqual(completed.completed_by, "Blair")
        self.assertEqual(completed.completed_at, completed_at)

    def test_list_shows_only_state_appropriate_actions(self):
        unclaimed = self.create_chore(title="Unclaimed chore")
        claimed = self.create_chore(
            title="Claimed chore",
            status=Chore.Status.CLAIMED,
            claimed_by="Alex",
            claimed_at=timezone.now(),
        )
        completed = self.create_chore(
            title="Completed chore",
            status=Chore.Status.COMPLETED,
            claimed_by="Alex",
            claimed_at=timezone.now(),
            completed_by="Blair",
            completed_at=timezone.now(),
        )

        response = self.client.get(reverse("chores:list"))

        self.assertContains(response, reverse("chores:claim", args=[unclaimed.pk]))
        self.assertNotContains(response, reverse("chores:complete", args=[unclaimed.pk]))
        self.assertNotContains(response, reverse("chores:claim", args=[claimed.pk]))
        self.assertContains(response, reverse("chores:complete", args=[claimed.pk]))
        self.assertNotContains(response, reverse("chores:claim", args=[completed.pk]))
        self.assertNotContains(response, reverse("chores:complete", args=[completed.pk]))
