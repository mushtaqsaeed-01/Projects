/**
 * API client for backend communication.
 */

import { Task, TaskCreate, TaskUpdate, TaskListResponse } from '../types/task';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Handle API response and throw error if not ok.
 */
async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
    throw new Error(error.detail || `HTTP ${response.status}: ${response.statusText}`);
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return {} as T;
  }

  return response.json();
}

/**
 * API client functions.
 */
export const api = {
  /**
   * Get all tasks.
   */
  async getTasks(): Promise<Task[]> {
    const response = await fetch(`${API_BASE_URL}/api/tasks`);
    const data = await handleResponse<TaskListResponse>(response);
    return data.tasks;
  },

  /**
   * Create a new task.
   */
  async createTask(taskData: TaskCreate): Promise<Task> {
    const response = await fetch(`${API_BASE_URL}/api/tasks`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(taskData),
    });
    return handleResponse<Task>(response);
  },

  /**
   * Update a task.
   */
  async updateTask(taskId: number, taskData: TaskUpdate): Promise<Task> {
    const response = await fetch(`${API_BASE_URL}/api/tasks/${taskId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(taskData),
    });
    return handleResponse<Task>(response);
  },

  /**
   * Toggle a task's completion status.
   */
  async completeTask(taskId: number): Promise<Task> {
    const response = await fetch(`${API_BASE_URL}/api/tasks/${taskId}/complete`, {
      method: 'PATCH',
    });
    return handleResponse<Task>(response);
  },

  /**
   * Delete a task.
   */
  async deleteTask(taskId: number): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/api/tasks/${taskId}`, {
      method: 'DELETE',
    });
    return handleResponse<void>(response);
  },
};
