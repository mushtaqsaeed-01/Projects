'use client';

import { useState } from 'react';

interface AddTaskFormProps {
  onAdd: (description: string) => Promise<void>;
}

export default function AddTaskForm({ onAdd }: AddTaskFormProps) {
  const [description, setDescription] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!description.trim()) {
      setError('Task description cannot be empty');
      return;
    }

    setIsSubmitting(true);
    try {
      await onAdd(description.trim());
      setDescription('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to add task');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form className="add-task-form" onSubmit={handleSubmit}>
      {error && <div className="error-message">{error}</div>}
      <input
        type="text"
        className="add-task-input"
        placeholder="Enter a new task..."
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        disabled={isSubmitting}
        aria-label="New task description"
      />
      <button
        type="submit"
        className="add-task-button"
        disabled={isSubmitting || !description.trim()}
      >
        {isSubmitting ? 'Adding...' : 'Add Task'}
      </button>
    </form>
  );
}
