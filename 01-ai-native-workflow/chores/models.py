from django.db import models


class Chore(models.Model):
    class Status(models.TextChoices):
        UNCLAIMED = "Unclaimed", "Unclaimed"
        CLAIMED = "Claimed", "Claimed"
        COMPLETED = "Completed", "Completed"

    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.UNCLAIMED,
    )
    claimed_by = models.CharField(max_length=100, blank=True, null=True)
    claimed_at = models.DateTimeField(blank=True, null=True)
    completed_by = models.CharField(max_length=100, blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title
