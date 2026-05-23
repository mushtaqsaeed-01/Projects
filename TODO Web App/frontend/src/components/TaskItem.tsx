'use client';

import { Task } from '../types/task';

interface TaskItemProps {
  task: Task;
  onComplete?: (taskId: number) => void;
  onUpdate?: (taskId: number, description: string) => void;
  onDelete?: (taskId: number) => void;
}

export default function TaskItem({ task, onComplete, onUpdate, onDelete }: TaskItemProps) {
  return (
    <div className={`task-item ${task.completed ? 'completed' : ''}`}>
      <input
        type="checkbox"
        className="task-checkbox"
        checked={task.completed}
        onChange={() => onComplete?.(task.id)}
        aria-label={`Mark "${task.description}" as ${task.completed ? 'incomplete' : 'complete'}`}
      />
      <span className="task-description">{task.description}</span>
      <div className="task-actions">
        <button
          className="task-button edit"
          onClick={() => {
            const newDescription = prompt('Edit task:', task.description);
            if (newDescription && newDescription.trim()) {
              onUpdate?.(task.id, newDescription.trim());
            }
          }}
          aria-label={`Edit "${task.description}"`}
        >
          Edit
        </button>
        <button
          className="task-button delete"
          onClick={() => {
            if (confirm(`Delete task: "${task.description}"?`)) {
              onDelete?.(task.id);
            }
          }}
          aria-label={`Delete "${task.description}"`}
        >
          Delete
        </button>
      </div>
    </div>
  );
}
