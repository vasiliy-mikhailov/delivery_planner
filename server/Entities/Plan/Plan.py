import datetime
from Entities.Assignment.AssignmentEntry import AssignmentEntry, quantize_resource_spent_hours
from Entities.Resource.Calendar.Calendar import generate_date_range
from Entities.Skill.Skill import Skill
from Entities.Task.Task import Task
from Entities.Team.Member import Member
from Entities.Team.Team import Team


class Plan:

    def __init__(self, start_date: datetime.date, end_date: datetime.date):
        self.start_date: datetime.date = start_date
        self.end_date: datetime.date = end_date
        self.tasks: [Task] = []
        self.resources: [Resource] = []
        self.teams: [Team] = []

    def calculate_task_effort_decrease_hours_and_member_spent_hours_for_date(
            self,
            member: Member,
            task: Task,
            date: datetime.date,
    ):
        resource = member.get_picked_resource()
        skill = member.get_skill()

        resource_remaining_work_hours_for_date = resource.get_remaining_work_hours_for_date(date=date)

        efficiency = resource.get_efficiency_for_date_and_skill(
            date=date,
            skill=skill
        )

        resource_task_effort_decrease_equivalent_work_hours_for_date = resource_remaining_work_hours_for_date * efficiency

        task_remaining_effort_hours = task.get_remaining_efforts_hours_for_skill_ignoring_sub_tasks(
            skill=skill
        )

        task_effort_decrease = min([resource_task_effort_decrease_equivalent_work_hours_for_date, task_remaining_effort_hours])

        resource_spent_hours = task_effort_decrease / resource_task_effort_decrease_equivalent_work_hours_for_date * resource_remaining_work_hours_for_date if resource_task_effort_decrease_equivalent_work_hours_for_date else 0

        resource_spent_hours_quantized = quantize_resource_spent_hours(resource_spent_hours=resource_spent_hours)
        task_effort_decrease_quantized = resource_spent_hours_quantized * efficiency

        return task_effort_decrease_quantized, resource_spent_hours_quantized

    def get_member_spendable_hours_for_task_and_period(
            self,
            member: Member,
            task: Task,
            start_date: datetime.date,
            end_date: datetime.date
    ):
        result = []
        resource = member.get_picked_resource()
        skill = member.get_skill()
        for date in generate_date_range(start_date, end_date):
            efficiency = resource.get_efficiency_for_date_and_skill(
                date=date,
                skill=skill
            )

            task_effort_decrease = resource.get_task_effort_decrease_for_task_and_date_and_skill(
                task=task,
                date=date,
                skill=skill
            )

            resource_spent_hours = task_effort_decrease / efficiency if efficiency else 0

            possible_additional_resource_spendable_hours = resource.get_remaining_work_hours_for_date(date=date)

            total_resource_spendable_hours = resource_spent_hours + possible_additional_resource_spendable_hours

            result.append({
                'date': date,
                'resource_spent_hours': resource_spent_hours,
                'possible_additional_resource_spendable_hours': possible_additional_resource_spendable_hours,
                'total_resource_spendable_hours': total_resource_spendable_hours,
                'efficiency': efficiency
            })

        result.sort(key=lambda x: x['total_resource_spendable_hours'])

        return result

    def level_member_effort_on_task_for_period(
            self,
            member: Member,
            task: Task,
            start_date: datetime.date,
            end_date: datetime.date
    ):
        resource = member.get_picked_resource()
        skill = member.get_skill()
        effort_hours_spent_on_task = sum([assignment.task_effort_decrease_hours for assignment in resource.get_assignment_entries_for_task_and_skill(
            task=task,
            skill=skill
        )])

        if effort_hours_spent_on_task > 0:
            resource_spendable_hours = self.get_member_spendable_hours_for_task_and_period(
                member=member,
                task=task,
                start_date=start_date,
                end_date=end_date
            )

            total_number_of_days_in_period = (end_date - start_date).days + 1

            remaining_task_effort_hours = effort_hours_spent_on_task
            remaining_number_of_days_in_period = total_number_of_days_in_period

            for rsh in resource_spendable_hours:
                rsh_date = rsh['date']
                rsh_total_resource_spendable_hours = rsh['total_resource_spendable_hours']
                rsh_efficiency = rsh['efficiency']
                rsh_resource_spent_hours = rsh['resource_spent_hours']
                rsh_resource_reduced_task_effort = rsh_resource_spent_hours * rsh_efficiency

                can_redistribute_time_in_current_day = rsh_total_resource_spendable_hours >= AssignmentEntry.MINIMAL_SPENDABLE_RESOURCE_HOURS

                if can_redistribute_time_in_current_day:
                    average_task_effort_hours_per_day = remaining_task_effort_hours / remaining_number_of_days_in_period
                    rsh_task_decrease_effort = rsh_total_resource_spendable_hours * rsh_efficiency
                    new_assignment_effort_hours = min(average_task_effort_hours_per_day, rsh_task_decrease_effort)
                    resource_spent_hours = new_assignment_effort_hours / rsh_efficiency
                    resource_spent_hours_quantized = quantize_resource_spent_hours(resource_spent_hours=resource_spent_hours)
                    task_effort_decrease_hours_quantized = resource_spent_hours_quantized * rsh_efficiency

                    if resource_spent_hours_quantized > AssignmentEntry.MINIMAL_SPENDABLE_RESOURCE_HOURS:
                        new_assignment = AssignmentEntry(
                            task=task,
                            resource=resource,
                            date=rsh_date,
                            skill=skill,
                            task_effort_decrease_hours=task_effort_decrease_hours_quantized,
                            resource_spent_hours=resource_spent_hours_quantized
                        )
                        task.remove_assignments_by_resource_and_date_and_skill(
                            resource=resource,
                            date=rsh_date,
                            skill=skill)
                        task.accept_assignment(assignment=new_assignment)

                        resource.remove_assignments_by_task_and_date_and_skill(
                            task=task,
                            date=rsh_date,
                            skill=skill
                        )
                        resource.accept_assignment(assignment=new_assignment)

                        remaining_task_effort_hours = remaining_task_effort_hours - new_assignment.task_effort_decrease_hours
                    else:
                        remaining_task_effort_hours = remaining_task_effort_hours - rsh_resource_reduced_task_effort
                else:
                    remaining_task_effort_hours = remaining_task_effort_hours - rsh_resource_reduced_task_effort

                remaining_number_of_days_in_period = remaining_number_of_days_in_period - 1

    def level_resources_effort_on_task_if_possible(self, task: Task):
        if task.has_start_date() and task.has_end_date():
            start_date = task.get_start_date()
            end_date = task.get_end_date()
            team = task.get_team()
            members = team.get_members()

            for member in members:
                if member.has_picked_resource():
                    self.level_member_effort_on_task_for_period(
                        member=member,
                        task=task,
                        start_date=start_date,
                        end_date=end_date
                    )


    def mark_bottleneck_group_for_task_if_effort_left(self, task: Task):
        team = task.get_team()

        for group in team.groups:
            is_task_done = task.get_remaining_efforts_hours_for_skill_ignoring_sub_tasks(skill=group.skill) == 0
            if not is_task_done:
                group.is_bottleneck = True

    def mark_bottleneck_groups_for_task_if_has_latest_assignment(self, task: Task):
        team = task.get_team()

        has_latest_assignment = False
        latest_assignment_date = None
        latest_assignment_group = None

        for group in team.groups:
            if group.has_assignment_end_date_for_task(task=task):
                group_assignment_end_date = group.get_assignment_end_date_for_task(task=task)
                if not has_latest_assignment or latest_assignment_date < group_assignment_end_date:
                    has_latest_assignment = True
                    latest_assignment_date = group_assignment_end_date
                    latest_assignment_group = group

        if has_latest_assignment:
            latest_assignment_group.is_bottleneck = True


    def mark_bottleneck_groups_for_task(self, task: Task):
        self.mark_bottleneck_group_for_task_if_effort_left(task=task)
        self.mark_bottleneck_groups_for_task_if_has_latest_assignment(task=task)

    def plan_leveled_recursive(self, tasks: [Task], start_date: datetime.date, end_date: datetime.date):
        for task in tasks:
            team = task.get_team()
            team.pick_resources_for_task(task=task, start_date=start_date, end_date=end_date)

            self.plan_leveled_recursive(
                tasks=task.get_direct_sub_tasks(),
                start_date=start_date,
                end_date=end_date
            )

            for date in generate_date_range(start_date, end_date):
                task_members = team.get_members()
                for member in task_members:
                    if member.has_picked_resource():
                        resource = member.get_picked_resource()
                        resource_remaining_work_hours_for_date = resource.get_remaining_work_hours_for_date(date=date)
                        resource_has_time_to_work_on_task = resource_remaining_work_hours_for_date >= AssignmentEntry.MINIMAL_SPENDABLE_RESOURCE_HOURS
                        if resource_has_time_to_work_on_task:
                            self.simulate_member_worked_on_task_for_day_ignoring_sub_tasks(
                                member=member,
                                task=task,
                                date=date
                            )

            self.mark_bottleneck_groups_for_task(task=task)

            self.level_resources_effort_on_task_if_possible(task=task)

    def plan_leveled(self):
        self.plan_leveled_recursive(
            tasks=self.tasks,
            start_date=self.start_date,
            end_date=self.end_date
        )


    def simulate_member_worked_on_task_for_day_ignoring_sub_tasks(
            self,
            member: Member,
            task: Task,
            date: datetime.date
    ):
        resource = member.get_picked_resource()
        member_skill = member.get_skill()
        if resource.is_helpful_in_performing_task_for_date(task=task, date=date) and task.can_be_worked_on_date(date=date):
            member_capacity = resource.capacities.get_capacity_for_skill(skill=member_skill)
            if member_capacity.is_helpful_in_performing_task_ignoring_children(task=task):
                skill = member_capacity.skill
                task_effort_decrease_hours, resource_spent_hours = self.calculate_task_effort_decrease_hours_and_member_spent_hours_for_date(
                    task=task,
                    member=member,
                    date=date
                )

                if resource_spent_hours >= AssignmentEntry.MINIMAL_SPENDABLE_RESOURCE_HOURS:
                    assignment_entry = AssignmentEntry(
                        task=task,
                        resource=resource,
                        date=date,
                        skill=skill,
                        task_effort_decrease_hours=task_effort_decrease_hours,
                        resource_spent_hours=resource_spent_hours
                    )
                    task.accept_assignment(assignment=assignment_entry)
                    resource.accept_assignment(assignment=assignment_entry)

    def simulate_member_worked_on_task_for_day_for_sub_tasks(self, member: Member, task: Task, date: datetime.date):
        for sub_task in task.get_direct_sub_tasks():
            self.simulate_member_worked_on_task_for_day(member=member, task=sub_task, date=date)

    def simulate_member_worked_on_task_for_day(self, member: Member, task: Task, date: datetime.date):
        self.simulate_member_worked_on_task_for_day_ignoring_sub_tasks(member=member, task=task, date=date)
        self.simulate_member_worked_on_task_for_day_for_sub_tasks(member=member, task=task, date=date)

    def simulate_member_worked_on_task_ignoring_sub_tasks(self, member: Member, task: Task):
        resource = member.get_picked_resource()
        days_with_remaining_hours = [day for day, hours in resource.remaining_work_hours_for_date.items() if hours > 0]

        for day in days_with_remaining_hours:
            self.simulate_member_worked_on_task_for_day_ignoring_sub_tasks(member=member, task=task, date=day)

    def simulate_member_worked_on_task_sub_tasks(self, member: Member, task: Task):
        for sub_task in task.sub_tasks:
            self.simulate_member_worked_on_task(member=member, task=sub_task)

    def simulate_member_worked_on_task(self, member: Member, task: Task):
        self.simulate_member_worked_on_task_ignoring_sub_tasks(member=member, task=task)
        self.simulate_member_worked_on_task_sub_tasks(member=member, task=task)

