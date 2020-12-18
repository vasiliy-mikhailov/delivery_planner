from Inputs.TaskIdInput import TaskIdInput


class FakeTaskIdInputReader:
    def read(self) -> [TaskIdInput]:
        task_id_input_1 = TaskIdInput('CR-1')
        task_id_input_2 = TaskIdInput('CR-4')
        return [task_id_input_1, task_id_input_2]