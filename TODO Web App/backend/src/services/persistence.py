"""
Persistence service for handling task data storage and retrieval using JSON files.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from src.models.task import Task


class PersistenceService:
    """Handles loading and saving tasks to/from JSON file."""

    def __init__(self, data_file_path: str = "data/tasks.json"):
        """
        Initialize the persistence service.

        Args:
            data_file_path: Path to the JSON file for storing tasks
        """
        self.data_file_path = Path(data_file_path)
        self.ensure_data_directory()

    def ensure_data_directory(self):
        """Ensure the data directory exists."""
        self.data_file_path.parent.mkdir(parents=True, exist_ok=True)

    def load_tasks(self) -> List[Task]:
        """
        Load all tasks from the JSON file.

        Returns:
            List of Task instances
        """
        try:
            if not self.data_file_path.exists():
                # Create empty file if it doesn't exist
                self.save_tasks([])
                return []

            with open(self.data_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            tasks_data = data.get("tasks", [])
            tasks = []
            for task_data in tasks_data:
                tasks.append(Task.from_dict(task_data))
            return tasks

        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in {self.data_file_path}")
        except FileNotFoundError:
            # Create the file if it doesn't exist
            self.save_tasks([])
            return []
        except Exception as e:
            raise Exception(f"Error loading tasks from {self.data_file_path}: {str(e)}")

    def save_tasks(self, tasks: List[Task]) -> None:
        """
        Save all tasks to the JSON file atomically.

        Args:
            tasks: List of Task instances to save
        """
        temp_file_path = self.data_file_path.with_suffix('.tmp')

        try:
            # Prepare data for saving
            tasks_data = {
                "tasks": [task.to_dict() for task in tasks]
            }

            # Write to temporary file first
            with open(temp_file_path, 'w', encoding='utf-8') as file:
                json.dump(tasks_data, file, indent=2, ensure_ascii=False)

            # Atomically move the temporary file to the actual file
            temp_file_path.replace(self.data_file_path)

        except Exception as e:
            # Clean up temp file if something goes wrong
            if temp_file_path.exists():
                temp_file_path.unlink()
            raise Exception(f"Error saving tasks to {self.data_file_path}: {str(e)}")

    def get_next_id(self) -> int:
        """
        Get the next available ID for a new task.

        Returns:
            Next available task ID
        """
        tasks = self.load_tasks()
        if not tasks:
            return 1
        # Return the highest current ID + 1
        return max(task.id for task in tasks) + 1

    def add_task(self, description: str) -> Task:
        """
        Add a new task with auto-generated ID.

        Args:
            description: The task description

        Returns:
            The newly created Task instance
        """
        if not description.strip():
            raise ValueError("Task description cannot be empty")

        next_id = self.get_next_id()
        new_task = Task(
            task_id=next_id,
            description=description.strip(),
            completed=False
        )

        tasks = self.load_tasks()
        tasks.append(new_task)
        self.save_tasks(tasks)

        return new_task

    def update_task(self, task_id: int, new_description: str) -> Optional[Task]:
        """
        Update a task's description.

        Args:
            task_id: ID of the task to update
            new_description: New description for the task

        Returns:
            Updated Task instance, or None if task not found
        """
        if not new_description.strip():
            raise ValueError("Task description cannot be empty")

        tasks = self.load_tasks()
        for i, task in enumerate(tasks):
            if task.id == task_id:
                updated_task = Task(
                    task_id=task.id,
                    description=new_description.strip(),
                    completed=task.completed,
                    created_date=task.created_date
                )
                tasks[i] = updated_task
                self.save_tasks(tasks)
                return updated_task

        return None

    def mark_complete(self, task_id: int) -> Optional[Task]:
        """
        Mark a task as complete.

        Args:
            task_id: ID of the task to mark complete

        Returns:
            Updated Task instance, or None if task not found
        """
        tasks = self.load_tasks()
        for i, task in enumerate(tasks):
            if task.id == task_id:
                updated_task = Task(
                    task_id=task.id,
                    description=task.description,
                    completed=True,
                    created_date=task.created_date
                )
                tasks[i] = updated_task
                self.save_tasks(tasks)
                return updated_task

        return None

    def toggle_complete(self, task_id: int) -> Optional[Task]:
        """
        Toggle a task's completion status.

        Args:
            task_id: ID of the task to toggle

        Returns:
            Updated Task instance, or None if task not found
        """
        tasks = self.load_tasks()
        for i, task in enumerate(tasks):
            if task.id == task_id:
                updated_task = Task(
                    task_id=task.id,
                    description=task.description,
                    completed=not task.completed,
                    created_date=task.created_date
                )
                tasks[i] = updated_task
                self.save_tasks(tasks)
                return updated_task

        return None

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: ID of the task to delete

        Returns:
            True if task was deleted, False if task not found
        """
        tasks = self.load_tasks()
        original_length = len(tasks)

        # Filter out the task with the given ID
        filtered_tasks = [task for task in tasks if task.id != task_id]

        if len(filtered_tasks) == original_length:
            # Task not found
            return False

        self.save_tasks(filtered_tasks)
        return True

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Get a task by its ID.

        Args:
            task_id: ID of the task to retrieve

        Returns:
            Task instance if found, None otherwise
        """
        tasks = self.load_tasks()
        for task in tasks:
            if task.id == task_id:
                return task
        return None
