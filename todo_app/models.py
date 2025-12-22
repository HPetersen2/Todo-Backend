from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Todo(models.Model):
    """
    Represents a todo item with status, priority, scheduling, and ownership metadata.
    """

    class Status(models.TextChoices):
        """
        Defines the available lifecycle states for a todo item.
        """
        OPEN = "open", "Open"
        IN_PROGRESS = "in_progress", "In Progress"
        DONE = "done", "Done"

    class Priority(models.IntegerChoices):
        """
        Defines the priority levels that can be assigned to a todo item.
        """
        LOW = 1, "Low"
        MEDIUM = 2, "Medium"
        HIGH = 3, "High"

    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN
    )

    priority = models.IntegerField(
        choices=Priority.choices,
        default=Priority.MEDIUM
    )

    due_date = models.DateField(null=True, blank=True)
    completed_at = models.DateField(null=True, blank=True)

    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="todos"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns a human-readable representation including status, title, and creator.
        """
        return f"[{self.get_status_display()}] {self.title} – {self.creator.username}"

