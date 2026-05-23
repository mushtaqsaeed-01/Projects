'use client';

import { Task } from '../types/task';
import TaskItem from './TaskItem';

interface TaskListProps {
  tasks: Task[];
  onComplete?: (taskId: number) => void;
  onUpdate?: (taskId: number, description: string) => void;
  onDelete?: (taskId: number) => void;
}

export default function TaskList({ tasks, onComplete, onUpdate, onDelete }: TaskListProps) {
  if (tasks.length === 0) {
    return (
      <div className="task-list">
        <div className="empty-state">No tasks found. Add a task to get started!</div>
      </div>
    );
  }

  return (
    <div className="task-list">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onComplete={onComplete}
          onUpdate={onUpdate}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}
