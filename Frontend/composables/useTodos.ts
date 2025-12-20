import { reactive } from 'vue';
import { INITIAL_TODOS } from '../data/todos';
import { NewTodoInput, Todo, TodoStatus } from '../types';

const state = reactive<{ todos: Todo[] }>({
  todos: [...INITIAL_TODOS],
});

const votes = reactive<Record<string, boolean>>({});

const addTodo = (input: NewTodoInput) => {
  const todo: Todo = {
    id: Math.random().toString(36).substr(2, 9),
    title: input.title,
    content: input.content,
    status: TodoStatus.PENDING,
    createdAt: Date.now(),
    author: input.author,
    heat: 0,
  };

  state.todos.unshift(todo);
};

const isVoted = (id: string) => !!votes[id];

const toggleVote = (id: string) => {
  const match = state.todos.find((item) => item.id === id);
  if (match) {
    if (votes[id]) {
      delete votes[id];
      match.heat = Math.max(0, match.heat - 1);
    } else {
      votes[id] = true;
      match.heat += 1;
    }
  }
};

export const useTodos = () => ({
  todos: state.todos,
  addTodo,
  toggleVote,
  isVoted,
});
