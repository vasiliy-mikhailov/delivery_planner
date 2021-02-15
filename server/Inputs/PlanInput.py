from datetime import date
from Inputs.TaskInput import TaskInput
from Inputs.ExistingResourceInput import ExistingResourceInput
from Inputs.PlannedResourceInput import PlannedResourceInput
from Inputs.TemporaryResourceInput import TemporaryResourceInput
from Inputs.VacationInput import VacationInput


class PlanInput:
    def __init__(self, start_date: date, end_date: date):
        self.start_date: date = start_date
        self.end_date: date = end_date
        self.tasks: [TaskInput] = []
        self.existing_resources: [ExistingResourceInput] = []
        self.vacations: [VacationInput] = []
        self.planned_resources: [PlannedResourceInput] = []
        self.temporary_resources: [TemporaryResourceInput] = []
        self.task_ids_to_add: [TaskInput] = []

