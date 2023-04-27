

class TaskNotFound(Exception):
    def __init__(self, task_id):
        msg = f"Task {task_id} was not found"
        super().__init__(msg)

