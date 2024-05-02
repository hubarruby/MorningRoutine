import random


class RandomMorningRoutine:
    def __init__(self, tasks, num_tasks, required_tasks=None):
        self.tasks = tasks
        self.num_tasks = num_tasks
        self.required_tasks = required_tasks if required_tasks else []
        self.selected_tasks = []
        self.index = 0
        self._reset_tasks()

    def _reset_tasks(self):
        if len(self.required_tasks) > self.num_tasks:
            raise ValueError("Number of required tasks exceeds the total number of tasks allowed")
        available_tasks = [task for task in self.tasks if task not in self.required_tasks]
        num_additional_tasks = self.num_tasks - len(self.required_tasks)

        if num_additional_tasks > len(available_tasks):
            raise ValueError("Not enough available tasks to meet the desired number of tasks")
        additional_tasks = random.sample(available_tasks, num_additional_tasks)
        self.selected_tasks = self.required_tasks + additional_tasks
        random.shuffle(self.selected_tasks)
        self.index = 0

    def get_next_task(self):
        if self.index >= len(self.selected_tasks):
            # If all tasks have been given, reset for a new round
            self._reset_tasks()
        task = self.selected_tasks[self.index]
        self.index += 1
        return task

    def get_undone_tasks(self):
        if self.index < len(self.selected_tasks):
            remaining_tasks = self.selected_tasks[self.index:]
        else:
            remaining_tasks = []
        not_selected_tasks = [task for task in self.tasks if task not in self.selected_tasks]
        return {'remaining_tasks': remaining_tasks, 'not_selected_tasks': not_selected_tasks}

    def to_dict(self):
        return {
            'tasks': self.tasks,
            'num_tasks': self.num_tasks,
            'required_tasks': self.required_tasks,
            'selected_tasks': self.selected_tasks,
            'index': self.index
        }

    @staticmethod
    def from_dict(data):
        routine = RandomMorningRoutine(data['tasks'], data['num_tasks'], data['required_tasks'])
        routine.selected_tasks = data['selected_tasks']
        routine.index = data['index']
        return routine