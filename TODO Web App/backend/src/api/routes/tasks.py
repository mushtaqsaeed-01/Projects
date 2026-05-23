"""
Task API routes.
"""

from fastapi import APIRouter, HTTPException, status
from typing import List
from src.services.persistence import PersistenceService
from src.api.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=TaskListResponse)
async def get_tasks():
    """
    Get all tasks.

    Returns:
        TaskListResponse: List of all tasks
    """
    try:
        persistence = PersistenceService()
        tasks = persistence.load_tasks()

        task_responses = [
            TaskResponse(
                id=task.id,
                description=task.description,
                completed=task.completed,
                created_date=task.created_date
            )
            for task in tasks
        ]

        return TaskListResponse(tasks=task_responses)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error loading tasks: {str(e)}"
        )


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task_data: TaskCreate):
    """
    Create a new task.

    Args:
        task_data: Task creation data

    Returns:
        TaskResponse: Created task
    """
    try:
        persistence = PersistenceService()
        task = persistence.add_task(task_data.description)

        return TaskResponse(
            id=task.id,
            description=task.description,
            completed=task.completed,
            created_date=task.created_date
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating task: {str(e)}"
        )


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_data: TaskUpdate):
    """
    Update a task's description.

    Args:
        task_id: ID of the task to update
        task_data: Task update data

    Returns:
        TaskResponse: Updated task
    """
    try:
        persistence = PersistenceService()
        task = persistence.update_task(task_id, task_data.description)

        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} not found"
            )

        return TaskResponse(
            id=task.id,
            description=task.description,
            completed=task.completed,
            created_date=task.created_date
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating task: {str(e)}"
        )


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def complete_task(task_id: int):
    """
    Toggle a task's completion status.

    Args:
        task_id: ID of the task to toggle

    Returns:
        TaskResponse: Updated task
    """
    try:
        persistence = PersistenceService()
        task = persistence.toggle_complete(task_id)

        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} not found"
            )

        return TaskResponse(
            id=task.id,
            description=task.description,
            completed=task.completed,
            created_date=task.created_date
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error toggling task completion: {str(e)}"
        )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int):
    """
    Delete a task.

    Args:
        task_id: ID of the task to delete
    """
    try:
        persistence = PersistenceService()
        deleted = persistence.delete_task(task_id)

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting task: {str(e)}"
        )
