import { Todo, TodoStatus } from '../types';

export const INITIAL_TODOS: Todo[] = [
  {
    id: '1',
    title: 'Integrate page transition animations',
    content: 'Introduce smooth, high-end motion for page transitions that feels consistent with the Apple-inspired aesthetic.',
    status: TodoStatus.COMPLETED,
    createdAt: Date.now() - 86400000,
    author: 'Design Lead',
    heat: 18,
  },
  {
    id: '2',
    title: 'Add dark mode toggle',
    content: 'Give users a quick toggle in settings to switch between light and dark experiences, honoring contrast and readability.',
    status: TodoStatus.IN_PROGRESS,
    createdAt: Date.now() - 43200000,
    author: 'Sarah',
    heat: 12,
  },
  {
    id: '3',
    title: 'Collaborative real-time editing',
    content: 'Enable multiple teammates to edit ideas simultaneously with presence indicators and live cursors.',
    status: TodoStatus.PENDING,
    createdAt: Date.now() - 10000,
    author: 'Alex',
    heat: 8,
  },
];
