from Repository.ExternalTaskReader.ExternalTaskRowsReader import ExternalTaskRowsReader


class FakeExternalTaskRowsReader(ExternalTaskRowsReader):

    def get_first_task_data(self):
        return [{'id': 'CR-1', 'name': 'Change Request 1', 'system': '', 'business_line': 'BL-1', 'solution_architecture_hours_left': 80.0, 'integration_testing_hours_left': 40.0, 'product_ownership_hours_left': 80.0}] \
             + [{'id': 'SYSCR-1.1', 'name': 'System Change Request 1.1', 'system': 'SYS-1', 'business_line': 'BL-1', 'system_analysis_hours_left': 80.0, 'developmen_hours_left': 40.0, 'system_testing_hours_left': 80.0, 'parent_id': 'CR-1'}] \
             + [{'id': 'SYSAN-1.1.1', 'name': 'System Analysis 1.1', 'system': 'SYS-1', 'business_line': 'BL-1', 'system_analysis_hours_left': 40.0, 'parent_id': 'SYSCR-1.1'}]\
             + [{'id': 'DEV-1.1.1', 'name': 'Development 1.1', 'system': 'SYS-1', 'business_line': 'BL-1', 'development_hours_left': 120.0, 'parent_id': 'SYSCR-1.1'}] \
             + [{'id': 'SYSTEST-1.1.1', 'name': 'System Testing 1.1', 'system': 'SYS-1', 'business_line': 'BL-1', 'system_testing_hours_left': 40.0, 'parent_id': 'SYSCR-1.1'}] \
             + [{'id': 'SYSCR-1.2', 'name': 'System Change Request 1.2', 'system': 'SYS-2', 'business_line': 'BL-1', 'system_analysis_hours_left': 400.0, 'development_hours_left': 1200.0, 'system_testing_hours_left': 400.0, 'parent_id': 'CR-1'}]

    def get_second_task_data(self):
        return [{'id': 'CR-4', 'name': 'Change Request 4', 'system': '', 'business_line': 'BL-2', 'solution_architecture_hours_left': 8.0, 'integration_testing_hours_left': 2.0, 'product_ownership_hours_left': 10.0}] \
             + [{'id': 'SYSCR-4.1', 'name': 'System Change Request 4.1', 'system': 'SYS-1', 'business_line': 'BL-2', 'system_analysis_hours_left': 40.0, 'development_hours_left': 120.0, 'system_testing_hours_left': 40.0, 'parent_id': 'CR-4'}]

    def read(self) -> [{}]:
        return self.get_first_task_data() + self.get_second_task_data()