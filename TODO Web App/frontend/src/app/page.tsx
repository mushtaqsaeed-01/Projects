'use client';

import { useEffect, useState } from 'react';
import { Task } from '../types/task';
import { api } from '../services/api';
import TaskList from '../components/TaskList';
import AddTaskForm from '../components/AddTaskForm';

export default function Home() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load tasks on mount
  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      const fetchedTasks = await api.getTasks();
      setTasks(fetchedTasks);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleAddTask = async (description: string) => {
    const newTask = await api.createTask({ description });
    setTasks([...tasks, newTask]);
  };

  const handleCompleteTask = async (taskId: number) => {
    try {
      const updatedTask = await api.completeTask(taskId);
      setTasks(tasks.map((task) => (task.id === taskId ? updatedTask : task)));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to complete task');
    }
  };

  const handleUpdateTask = async (taskId: number, description: string) => {
    try {
      const updatedTask = await api.updateTask(taskId, { description });
      setTasks(tasks.map((task) => (task.id === taskId ? updatedTask : task)));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update task');
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    try {
      await api.deleteTask(taskId);
      setTasks(tasks.filter((task) => task.id !== taskId));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete task');
    }
  };

  if (loading) {
    return <div className="loading-spinner">Loading tasks...</div>;
  }

  return (
    <>
      {error && <div className="error-message">{error}</div>}
      <AddTaskForm onAdd={handleAddTask} />
      <TaskList
        tasks={tasks}
        onComplete={handleCompleteTask}
        onUpdate={handleUpdateTask}
        onDelete={handleDeleteTask}
      />
    </>
  );
}
