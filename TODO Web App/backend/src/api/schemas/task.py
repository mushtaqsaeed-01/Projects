"""
Pydantic schemas for task API request/response validation.
"""

from pydantic import BaseModel, Field
from typing import Optional


class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    description: str = Field(..., min_length=1, max_length=1000, description="Task description")

    class Config:
        json_schema_extra = {
            "example": {
                "description": "Buy groceries"
            }
        }


class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    description: str = Field(..., min_length=1, max_length=1000, description="New task description")

    class Config:
        json_schema_extra = {
            "example": {
                "description": "Buy groceries and cook dinner"
            }
        }


class TaskResponse(BaseModel):
    """Schema for task response."""
    id: int = Field(..., description="Unique task identifier")
    description: str = Field(..., description="Task description")
    completed: bool = Field(..., description="Completion status")
    created_date: str = Field(..., description="ISO 8601 timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "description": "Buy groceries",
                "completed": False,
                "created_date": "2026-02-17T10:00:00.000000"
            }
        }


class TaskListResponse(BaseModel):
    """Schema for task list response."""
    tasks: list[TaskResponse] = Field(..., description="List of tasks")

    class Config:
        json_schema_extra = {
            "example": {
                "tasks": [
                    {
                        "id": 1,
                        "description": "Buy groceries",
                        "completed": False,
                        "created_date": "2026-02-17T10:00:00.000000"
                    }
                ]
            }
        }
