from fastapi import HTTPException


class TaskNotFound(HTTPException):
    def __init__(self, task_id):
        msg = f"Task {task_id} was not found"
        super().__init__(status_code=404, detail=msg)

