from Entities.Skill.AbilityEnum import AbilityEnum
from Inputs.EffortInput import EffortInput
from Inputs.ExternalTaskInput import ExternalTaskInput
from Outputs.ExternalTaskOutput import ExternalTaskOutput
from Repository.ExternalTaskReader.ExternalTaskRowsReader import ExternalTaskRowsReader


class ExternalTaskRowsToExternalTaskInputsDataConverter:

    EFFORT_ABILITY_TO_ABILITY_ENUM_MAPPING = {
        'solution_architecture_hours_left': AbilityEnum.SOLUTION_ARCHITECTURE,
        'project_management_hours_left': AbilityEnum.PROJECT_MANAGEMENT,
        'system_analysis_hours_left': AbilityEnum.SYSTEM_ANALYSIS,
        'development_hours_left': AbilityEnum.DEVELOPMENT,
        'system_testing_hours_left': AbilityEnum.SYSTEM_TESTING,
        'integration_testing_hours_left': AbilityEnum.INTEGRATION_TESTING,
        'product_ownership_hours_left': AbilityEnum.PRODUCT_OWNERSHIP
    }

    def __init__(self, external_task_rows_reader: ExternalTaskRowsReader):
        self.external_task_rows_reader: ExternalTaskRowsReader = external_task_rows_reader
        self.external_task_rows: [{}] = self.external_task_rows_reader.read()
        self.parent_to_childs: {} = {}

        for external_task_row in self.external_task_rows:
            parent_id = external_task_row['parent_id'] if 'parent_id' in external_task_row else ''

            if not parent_id in self.parent_to_childs:
                self.parent_to_childs[parent_id] = []

            self.parent_to_childs[parent_id].append(external_task_row)

    def get_children(self, parent_id: str) -> [{}]:
        if parent_id in self.parent_to_childs:
            return self.parent_to_childs[parent_id]
        else:
            return []

    def convert_external_task_row_to_effort_inputs(self, external_task_row) -> [EffortInput]:
        result = []

        for ability_name in self.EFFORT_ABILITY_TO_ABILITY_ENUM_MAPPING.keys():
            if ability_name in external_task_row:
                hours = external_task_row[ability_name]
                ability = self.EFFORT_ABILITY_TO_ABILITY_ENUM_MAPPING[ability_name]
                effort = EffortInput(ability=ability, hours=hours)
                result.append(effort)

        return result

    def convert_external_task_row_to_external_task_input(self, external_task_row, level: int) -> ExternalTaskInput:
        id = external_task_row['id']
        name = external_task_row['name']
        system = external_task_row['system']
        business_line = external_task_row['business_line'] if 'business_line' in external_task_row else ''
        result = ExternalTaskInput(
            id=id,
            name=name,
            system=system,
            business_line=business_line
        )

        efforts = self.convert_external_task_row_to_effort_inputs(external_task_row=external_task_row)

        result.efforts = efforts

        if level < 3:
            sub_tasks = [self.convert_external_task_row_to_external_task_input(external_task_row=external_task_row, level=level+1) for external_task_row in self.get_children(parent_id=id)]
            result.sub_tasks = sub_tasks

        return result

    def convert(self) -> [ExternalTaskOutput]:
        result = [self.convert_external_task_row_to_external_task_input(external_task_row=external_task_row, level=1) for external_task_row in self.get_children(parent_id='')]

        return result

