"""
Task model representing a single TODO item.
"""

from datetime import datetime
from typing import Dict, Any


class Task:
    """Represents a single TODO item in the user's task list."""

    def __init__(self, task_id: int, description: str, completed: bool = False, created_date: str = None):
        """
        Initialize a Task instance.

        Args:
            task_id: Unique identifier for the task
            description: The text description of the task
            completed: Whether the task has been completed (default: False)
            created_date: ISO 8601 formatted timestamp of when task was created (default: current time)
        """
        self.id = task_id
        self.description = description
        self.completed = completed

        if created_date is None:
            self.created_date = datetime.now().isoformat()
        else:
            self.created_date = created_date

    def to_dict(self) -> Dict[str, Any]:
        """Convert the Task instance to a dictionary representation."""
        return {
            "id": self.id,
            "description": self.description,
            "completed": self.completed,
            "created_date": self.created_date
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Create a Task instance from a dictionary representation."""
        return cls(
            task_id=data["id"],
            description=data["description"],
            completed=data.get("completed", False),
            created_date=data.get("created_date")
        )

    def __repr__(self) -> str:
        """Return a string representation of the Task instance."""
        status = "✓" if self.completed else "○"
        return f"[{status}] #{self.id}: {self.description}"
