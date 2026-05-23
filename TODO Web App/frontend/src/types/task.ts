/**
 * Task interface matching backend schema.
 */
export interface Task {
  id: number;
  description: string;
  completed: boolean;
  created_date: string;
}

/**
 * Task creation request payload.
 */
export interface TaskCreate {
  description: string;
}

/**
 * Task update request payload.
 */
export interface TaskUpdate {
  description: string;
}

/**
 * Task list response.
 */
export interface TaskListResponse {
  tasks: Task[];
}
