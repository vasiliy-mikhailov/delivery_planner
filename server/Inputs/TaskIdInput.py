class TaskIdInput:

    def __init__(self, id: str):
        if not isinstance(id, str):
            raise ValueError('TaskInput __init__ parameter "id" must be str.')

        self.id: str = id
