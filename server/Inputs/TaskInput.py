from Inputs.EffortInput import EffortInput
from Inputs.TeamMemberInput import TeamMemberInput


class TaskInput:

    def __init__(self, id: str, name: str, system: str, business_line: str):
        if not isinstance(id, str):
            raise ValueError('TaskInput __init__ parameter "id" must be str.')

        if not isinstance(name, str):
            raise ValueError('TaskInput __init__ parameter "name" must be str.')

        if not isinstance(system, str):
            raise ValueError('TaskInput __init__ parameter "system" must be str.')

        if not isinstance(business_line, str):
            raise ValueError('TaskInput __init__ parameter "business_line" must be str.')

        self.id: str = id
        self.name: str = name
        self.system: str = system
        self.business_line: str = business_line
        self.efforts: [EffortInput] = []
        self.sub_tasks: [TaskInput] = []
        self.predecessors: [TaskInput] = []
        self.team_members: [TeamMemberInput] = []
