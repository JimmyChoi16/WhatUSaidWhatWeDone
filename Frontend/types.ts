
export enum TodoStatus {
  PENDING = 'Pending',
  IN_PROGRESS = 'In Progress',
  COMPLETED = 'Completed'
}

export interface Todo {
  id: string;
  title: string;
  content: string;
  status: TodoStatus;
  createdAt: number;
  updatedAt?: number;
  author: string;
  heat: number;
  userId?: number;
}

export interface NewTodoInput {
  title: string;
  content: string;
}

export interface TodoUpdateInput {
  title?: string;
  content?: string;
  status?: TodoStatus;
}
